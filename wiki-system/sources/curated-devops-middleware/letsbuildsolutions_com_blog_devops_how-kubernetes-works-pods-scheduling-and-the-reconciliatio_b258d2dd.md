---
source: "https://letsbuildsolutions.com/blog/devops/how-kubernetes-works-pods-scheduling-and-the-reconciliation-loop"
title: "How Kubernetes Works: Pods, Scheduling, and the Reconciliation Loop — Let's Build"
fetched_at: "2026-10-06 12:34"
---

Kubernetes coordinates hundreds of processes across dozens of machines, yet the core mechanism is simple: a set of control loops continuously compare what you asked for against what actually exists, and drive the cluster toward agreement. Every component, from the scheduler to the kubelet, participates in this loop. Understanding how each component plays its role turns Kubernetes from a pile of YAML into a coherent system you can reason about and debug.

This article walks through the control plane, the data plane, the path a pod travels from `kubectl apply` to a running container, and the networking and storage abstractions that sit above it all.

## The Control Plane: Four Components, One Invariant

The Kubernetes control plane is the brain of the cluster. It stores state, makes decisions, and communicates those decisions to the nodes that do the actual work. Four components handle this, each with a narrow responsibility.

### The API Server: Single Gateway

Every read and write to the cluster goes through `kube-apiserver`. It is stateless: it receives requests, validates them against JSON Schema and admission controllers, and persists accepted state to etcd. Nothing in the cluster talks directly to etcd except the API server.

This single-gateway design has important implications. The API server is the only component that needs to know etcd’s topology. If you add etcd members, nothing else changes. The API server also enforces all access control (RBAC), runs admission webhooks, and translates between storage format versions (Kubernetes supports multiple API versions for the same resource concurrently).

The API server serves requests through a versioned REST interface. A `kubectl apply` of a Deployment sends a `PATCH` or `PUT` to `/apis/apps/v1/namespaces/default/deployments/my-app`. The server validates the object, runs admission, and writes it to etcd.
    
    
    # See the raw API call kubectl makes
    kubectl apply -f deployment.yaml -v 8 2>&1 | grep -E "(PUT|PATCH|POST) "
    # Output: I0521 ... PUT https://api.cluster.internal/apis/apps/v1/namespaces/default/deployments/my-app

### etcd: Source of Truth with Watch Semantics

etcd is a distributed key-value store built on the Raft consensus algorithm. Kubernetes stores all cluster state here: pods, deployments, services, configmaps, secrets, node registrations, everything.

The critical feature for Kubernetes is not storage but **watch**. etcd allows clients to watch a key or key prefix and receive a stream of change notifications: `ADDED`, `MODIFIED`, `DELETED`. Every Kubernetes controller, the scheduler, and every kubelet watches the API server (which proxies etcd watches) rather than polling. The result is that components react to changes within milliseconds without anyone burning CPU on polling loops.

Each object in etcd has a `resourceVersion`: a monotonically increasing integer that etcd increments on every write. Watch clients provide the last `resourceVersion` they saw. If the API server’s watch cache has the events since that version, the client catches up without hitting etcd. This is how Kubernetes can serve thousands of concurrent watchers from a small etcd cluster.
    
    
    // Kubernetes informer pattern: the TypeScript equivalent of a controller watching resources
    import * as k8s from "@kubernetes/client-node";
    
    const kc = new k8s.KubeConfig();
    kc.loadFromDefault();
    
    const watch = new k8s.Watch(kc);
    
    interface PodEvent {
      type: "ADDED" | "MODIFIED" | "DELETED";
      object: k8s.V1Pod;
    }
    
    async function watchPods(namespace: string): Promise<void> {
      const req = await watch.watch(
        `/api/v1/namespaces/${namespace}/pods`,
        {},
        (type: string, obj: k8s.V1Pod) => {
          const event: PodEvent = { type: type as PodEvent["type"], object: obj };
          console.log(`${event.type} pod/${event.object.metadata?.name}`);
    
          if (event.type === "MODIFIED") {
            const phase = event.object.status?.phase;
            const conditions = event.object.status?.conditions ?? [];
            const ready = conditions.find((c) => c.type === "Ready")?.status === "True";
            console.log(`  phase=${phase} ready=${ready}`);
          }
        },
        (err: unknown) => {
          if (err) console.error("Watch error:", err);
        }
      );
    
      // req is an http.ClientRequest; abort to stop watching
      process.on("SIGTERM", () => req.abort());
    }
    
    watchPods("default");

### The Scheduler: Filtering Then Scoring

`kube-scheduler` watches for pods that have no `nodeName` set in their spec. When one appears, the scheduler runs its placement algorithm to pick a node, then writes `nodeName` back to the pod object via the API server. The scheduler never launches anything. It only assigns nodes.

The algorithm has two phases:

**Filtering (Predicates)** : Remove nodes that cannot run the pod. Filters include: the node has enough CPU and memory for the pod’s `requests`, the node’s taints are tolerated by the pod, node affinity rules are satisfied, the pod’s volume claims can be satisfied on this node, and the node is in a `Ready` condition. The result is a list of feasible nodes.

**Scoring (Priorities)** : Rank the feasible nodes. Default scoring factors include: how much of the pod’s requested resources the node already has allocated (spreading pods across nodes with spare capacity), whether the pod has images already pulled on the node, and node affinity weights. Each factor contributes a score from 0 to 100. The node with the highest weighted sum wins.
    
    
    # Pod spec with scheduling constraints
    apiVersion: v1
    kind: Pod
    metadata:
      name: api-server
    spec:
      containers:
        - name: app
          image: my-app:v2.3.1
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "1000m"
              memory: "512Mi"
      # Required: spread across different availability zones
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: topology.kubernetes.io/zone
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: api-server
      # Soft preference: avoid nodes already running an api-server pod
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app: api-server
                topologyKey: kubernetes.io/hostname

Scheduling is a snapshot decision. The scheduler chooses a node based on state at the moment of scheduling. It does not continuously re-evaluate pod placements. Moving a running pod to a better node requires evicting and rescheduling it, which is what the Descheduler project handles as a separate, optional component.

### The Controller Manager: Reconciliation Loops

`kube-controller-manager` runs dozens of controllers as goroutines in a single binary. Each controller owns one resource type and is responsible for making the world match what that resource describes.

The Deployment controller is the clearest example. It watches Deployment objects and ReplicaSet objects. When you update a Deployment (change the image, for instance), the controller creates a new ReplicaSet for the new version and begins scaling it up while scaling the old ReplicaSet down, honoring `maxSurge` and `maxUnavailable`. It does this by repeatedly reading current state from the API server, computing the delta, and writing changes back.

Every controller follows the same pattern:
    
    
    observe current state (from informer cache)
    compute desired state (from the owned resource spec)
    if current != desired:
        make one or more API calls to close the gap

Controllers are optimistic. They write to the API server, which may reject the write if another writer updated the object concurrently (etcd uses compare-and-swap under the hood). A rejected write causes the controller to re-queue the item and re-reconcile. This is why controllers are idempotent: they should produce the same outcome whether they run once or ten times on the same state.

## The Data Plane: Nodes Running Pods

The data plane is every node in the cluster. Nodes run kubelet, kube-proxy, and a container runtime, plus whatever CNI plugin handles networking.

### kubelet: The Node Agent

kubelet is the only component that runs directly on every node (not in a pod). It watches the API server for pods assigned to its node (via the `nodeName` field set by the scheduler). When a pod appears, kubelet ensures the containers in that pod are running. When a pod is deleted, kubelet terminates the containers.

kubelet does not talk directly to Docker or containerd. It uses the **Container Runtime Interface (CRI)** , a gRPC API that standardizes the contract between the kubelet and any container runtime. The runtime implements two services: `RuntimeService` (manage pod sandboxes and containers) and `ImageService` (pull and list images). containerd ships a built-in CRI plugin. Docker requires the `cri-dockerd` shim.
    
    
    # crictl: the CRI-aware CLI, bypasses the Docker daemon entirely
    crictl --runtime-endpoint unix:///run/containerd/containerd.sock pods
    crictl ps
    crictl logs <container-id>
    crictl inspect <container-id> | jq .status.resources

kubelet also runs the **liveness probe** and **readiness probe** loops for every container it manages. A failed liveness probe results in a container restart (respecting `restartPolicy`). A failed readiness probe removes the pod’s IP from the Endpoints object for its Services, stopping new traffic from reaching it. These two probes have different semantics and different consequences.

### kube-proxy: Services as Kernel Rules

`kube-proxy` watches Service and Endpoints objects. When a Service is created or its endpoints change, kube-proxy updates the node’s packet-routing rules to implement the Service’s virtual IP.

In iptables mode (the default on most distributions), kube-proxy writes `DNAT` rules that intercept packets addressed to the Service’s ClusterIP and randomly forward them to one of the healthy pod IPs. The selection is stateless per-packet and weighted by endpoint count.

In IPVS mode, kube-proxy creates a virtual server using the Linux kernel’s IP Virtual Server subsystem. IPVS uses hash tables rather than linear iptables chain traversal, which makes it significantly faster for clusters with thousands of Services.
    
    
    # Inspect iptables rules for a Service's ClusterIP
    SERVICE_IP=$(kubectl get svc my-svc -o jsonpath='{.spec.clusterIP}')
    iptables-save | grep "$SERVICE_IP"
    # Output: -A KUBE-SERVICES -d 10.96.14.7/32 -p tcp --dport 8080 -j KUBE-SVC-XXXXX
    # Then: -A KUBE-SVC-XXXXX -m statistic --mode random --probability 0.33 -j KUBE-SEP-AAAA
    #       -A KUBE-SVC-XXXXX -m statistic --mode random --probability 0.50 -j KUBE-SEP-BBBB
    #       -A KUBE-SVC-XXXXX -j KUBE-SEP-CCCC

## Pod Lifecycle: From kubectl apply to Running Container

The full path a pod travels involves every component described above, in sequence:

  1. `kubectl apply -f pod.yaml` sends a `POST` or `PATCH` to the API server
  2. The API server runs admission controllers: mutating webhooks first (add sidecar containers, inject environment variables, set defaults), then validating webhooks (reject if policy is violated)
  3. The API server writes the pod to etcd with `phase: Pending` and no `nodeName`
  4. The scheduler’s informer detects the new unscheduled pod, runs filter and score, and sends a binding request that sets `nodeName`
  5. The kubelet on the selected node detects its new pod assignment via its watch on the API server
  6. kubelet calls the container runtime via CRI: create a pause (sandbox) container, set up the network namespace, pull images for each container, create and start each container
  7. The CNI plugin configures the network: creates a `veth` pair, places one end in the pod’s network namespace, connects the other to the node bridge, and programs routes so the pod IP is reachable cluster-wide
  8. kubelet begins running liveness and readiness probes
  9. Once the readiness probe passes, kubelet updates the pod’s `Ready` condition to `True`
  10. The Endpoints controller detects the ready pod and adds its IP to the Endpoints object for any matching Services
  11. kube-proxy detects the updated Endpoints and rewrites iptables or IPVS rules to include the new pod IP



The entire sequence, from `kubectl apply` to traffic reaching the pod, typically completes in under 5 seconds on a well-sized cluster with pre-pulled images. Image pull time dominates when images are not cached on the node.

## Networking: Flat Pods, Stable Services, External Ingress

Kubernetes mandates a specific networking model: every pod gets a unique IP address, and any pod can reach any other pod’s IP directly without NAT. This flat network is not built into Kubernetes itself. It is implemented by a **CNI (Container Network Interface)** plugin.

CNI plugins range from the simple (Flannel, which uses VXLAN tunnels or host-gateway routing to forward traffic between nodes) to the complex (Cilium, which uses eBPF to implement routing, load balancing, and network policy in the kernel without iptables at all). The plugin is called by kubelet at pod creation time with a JSON configuration, and it must make the pod’s IP reachable from any node in the cluster.

**Services** add a stable virtual IP in front of a set of pods. The Service’s ClusterIP does not change even as pods are replaced. Endpoints are automatically updated by the Endpoints controller as pods become ready or are removed. This decoupling is the core reliability mechanism for inter-service communication: clients address the Service, not individual pods.

**Ingress and the Gateway API** handle external traffic. An Ingress resource defines rules (host-based or path-based routing) and an Ingress controller (nginx, Envoy, Traefik) implements them by configuring a load balancer or reverse proxy. The Gateway API is the newer, more expressive standard that separates infrastructure configuration (Gateway) from routing rules (HTTPRoute), enabling better multi-team access control over routing.
    
    
    # Gateway API: infrastructure owner configures the Gateway
    apiVersion: gateway.networking.k8s.io/v1
    kind: Gateway
    metadata:
      name: prod-gateway
      namespace: infra
    spec:
      gatewayClassName: nginx
      listeners:
        - name: https
          protocol: HTTPS
          port: 443
          tls:
            mode: Terminate
            certificateRefs:
              - name: prod-tls
    ---
    # App team configures their route without touching the Gateway
    apiVersion: gateway.networking.k8s.io/v1
    kind: HTTPRoute
    metadata:
      name: api-route
      namespace: my-app
    spec:
      parentRefs:
        - name: prod-gateway
          namespace: infra
      hostnames:
        - api.example.com
      rules:
        - matches:
            - path:
                type: PathPrefix
                value: /v2
          backendRefs:
            - name: api-svc
              port: 8080

## Storage: PV, PVC, and CSI Drivers

Kubernetes separates storage provisioning from consumption with three abstractions:

**PersistentVolume (PV)** : a piece of storage provisioned by an administrator or a StorageClass, with specific capacity, access modes, and a driver-specific configuration (an EBS volume ID, an NFS mount path, etc.).

**PersistentVolumeClaim (PVC)** : a request from a pod for storage matching certain criteria (minimum size, access mode). The PVC binds to a PV that satisfies the claim. Once bound, the pod mounts the PVC as a volume.

**CSI Driver** : the Container Storage Interface plugin that handles the actual provisioning, attaching, and mounting of storage. EBS, GCS, Ceph, Longhorn, and dozens of others implement CSI. kubelet calls the CSI driver via gRPC to mount the volume into the pod before starting its containers.
    
    
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: postgres-data
    spec:
      accessModes:
        - ReadWriteOnce
      storageClassName: gp3
      resources:
        requests:
          storage: 100Gi
    ---
    apiVersion: apps/v1
    kind: StatefulSet
    metadata:
      name: postgres
    spec:
      serviceName: postgres
      replicas: 1
      selector:
        matchLabels:
          app: postgres
      template:
        spec:
          containers:
            - name: postgres
              image: postgres:16-alpine
              volumeMounts:
                - name: data
                  mountPath: /var/lib/postgresql/data
      volumeClaimTemplates:
        - metadata:
            name: data
          spec:
            accessModes: ["ReadWriteOnce"]
            storageClassName: gp3
            resources:
              requests:
                storage: 100Gi

## Orchestrator Tradeoffs

| Kubernetes| AWS ECS| HashiCorp Nomad| Cloud Run  
---|---|---|---|---  
**Operational complexity**|  High: control plane, etcd, CNI, add-ons| Low on Fargate, medium on EC2| Medium: single binary, no etcd| Very low: fully managed  
**Scaling model**|  HPA, VPA, KEDA, Cluster Autoscaler| Service auto-scaling, capacity providers| Job scaling, Nomad Autoscaler| Request-per-container, instant scale-to-zero  
**Networking flexibility**|  Full control via CNI, network policy| VPC-native, limited egress control per task| Consul Connect for service mesh| Cloud NAT, VPC connector  
**Ecosystem maturity**|  Very large: Helm, Argo, Crossplane, Tekton, Flux| AWS ecosystem only| Smaller, growing| GCP ecosystem only  
**Cost at small scale**|  Expensive: 3 control plane nodes, 3+ workers| Fargate is pay-per-task, no idle control plane cost| Low: control plane is a single process| Very low: pay only for requests  
**Multi-cloud portability**|  High: same manifests across any conformant cluster| None: ECS API is proprietary| High: HCL jobs run on any provider| None: GCP-specific  
  
Kubernetes earns its complexity only at sufficient scale or when you need what it uniquely provides: declarative multi-workload orchestration, a rich ecosystem of GitOps tooling, custom resource extensibility, and true multi-cloud portability. For a two-service startup, ECS Fargate or Cloud Run will deliver the same outcome at a fraction of the operational overhead.

## Production Considerations

### Resource Requests and Limits

Requests are the scheduler’s input. The scheduler sums requests across all pods on a node and only places a pod if the node’s allocatable capacity exceeds the sum. If you omit requests, the scheduler sees zero resource consumption for your pod and may place it on an already-overloaded node.

Limits are enforcement at runtime by the cgroup. A container that exceeds its memory limit is OOMKilled immediately. A container that exceeds its CPU limit is throttled, not killed. An OOMKilled pod that restarts repeatedly enters `CrashLoopBackOff` with exponential backoff.

A common mistake: setting CPU limits aggressively causes throttling even when the node has spare CPU capacity, because cgroup CPU limits enforce a quota within a fixed period (100ms by default) regardless of what else is running. For CPU-sensitive workloads, set requests but omit limits. For memory, always set both, because memory pressure without limits causes the kernel’s OOM killer to terminate arbitrary processes.
    
    
    resources:
      requests:
        cpu: "250m"    # Scheduler uses this; 250 millicores
        memory: "256Mi"
      limits:
        # cpu: omitted intentionally for low-latency services
        memory: "512Mi"  # OOMKilled if exceeded, better than swap thrash

### Pod Disruption Budgets

A PodDisruptionBudget (PDB) constrains voluntary disruptions: node drains, cluster upgrades, Descheduler evictions. Without a PDB, a node drain can evict all pods of a Deployment simultaneously.
    
    
    apiVersion: policy/v1
    kind: PodDisruptionBudget
    metadata:
      name: api-pdb
    spec:
      minAvailable: 2
      selector:
        matchLabels:
          app: api-server

`minAvailable: 2` means at least 2 pods must be running and ready at all times during voluntary disruption. If only 2 pods are scheduled and a drain tries to evict both, the drain blocks until the disrupted pod is rescheduled and healthy elsewhere. This is the correct mechanism for ensuring rolling cluster upgrades do not cause downtime.

### Readiness vs. Liveness Probes

These two probes have different failure responses and should be configured independently.

A **readiness probe** failure removes the pod from Service endpoints. Traffic stops reaching the pod. The pod is not restarted. This is appropriate for temporary overload: when a pod signals unready, the Service routes around it until it recovers.

A **liveness probe** failure kills and restarts the container. This is appropriate only when the process is deadlocked or otherwise unable to recover without a restart. Configuring a liveness probe that is too aggressive (short `failureThreshold`, tight `timeoutSeconds`) causes restart loops for transient slowness that the process would have recovered from on its own.
    
    
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
      initialDelaySeconds: 30   # Give the process time to start
      periodSeconds: 10
      failureThreshold: 3       # 30 seconds of failure before restart
      timeoutSeconds: 5
    readinessProbe:
      httpGet:
        path: /ready
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 5
      failureThreshold: 2       # 10 seconds before removing from endpoints
      timeoutSeconds: 3

The `/healthz` and `/ready` endpoints should check different things. `/healthz` checks only that the process is alive and responsive. `/ready` checks that the process can serve traffic: dependencies are reachable, internal queues are not backlogged, the database connection pool is healthy.

### Cluster Autoscaler Behavior

The Cluster Autoscaler watches for pods that are stuck in `Pending` because no node has capacity to schedule them. When it finds such pods, it simulates scheduling against each node group’s instance type and triggers a scale-out by increasing the node group’s desired count.

Scale-in is more conservative. The autoscaler periodically evaluates whether any node’s pods could be rescheduled onto other nodes with capacity to spare. If so, it drains and terminates the node. Two things block scale-in: a pod with no controller (bare pods are never evicted by the autoscaler), and a pod whose PDB would be violated by eviction.

The implication: if your PDBs are too strict relative to your replica count, the autoscaler will never scale in. A `minAvailable: 100%` PDB on a two-replica Deployment means neither pod can ever be evicted, so nodes hosting those pods are scale-in-blocked permanently. Match your PDBs to your actual availability requirements, not to the theoretical maximum.

## The Mental Model

Kubernetes is a distributed state machine. The only persistent state is in etcd. Every other component is stateless and works by reading desired state, observing actual state, and writing changes to close the gap. When something breaks, the question is always: which reconciliation loop is responsible, and why is it not converging?

A pod stuck in `Pending` means the scheduler cannot place it: check node capacity, taints, affinity rules. A pod in `CrashLoopBackOff` means the container is exiting: check liveness probes and the container logs. A Service that routes no traffic despite healthy pods means the readiness probe is failing or the Endpoints object is empty. In each case, the component that owns the reconciliation loop leaves evidence in its own log and in the state of the objects it manages.

The complexity is real, but it is organized complexity. Once you know which component owns which loop, debugging Kubernetes stops being guesswork.

## More in DevOps

[ DevOps  · Jun 3, 2026  How Terraform Works Internally: HCL Parsing, Dependency Graph Execution, and the Provider Protocol Behind Infrastructure as Code  A deep dive into Terraform's internal architecture covering HCL parsing, the expression evaluation engine, DAG-based dependency resolution, the gRPC provider plugin protocol, state mechanics, and the plan/apply lifecycle.  ](/blog/devops/how-terraform-works-internally-hcl-parsing-dependency-graph-execution-and-the-provider-protocol/)[ DevOps  · May 30, 2026  How Docker Works Internally: Namespaces, Cgroups, Union Filesystems, and the OCI Runtime Behind Every Container  A deep dive into what happens when you run docker run: Linux namespaces for process isolation, cgroups v2 for resource enforcement, overlay2 union filesystem for layered images, the OCI runtime spec and how runc spawns containers, content-addressable storage, the containerd shim architecture, and networking with veth pairs.  ](/blog/devops/how-docker-works-internally-namespaces-cgroups-union-filesystems-and-the-oci-runtime/)[ DevOps  · May 20, 2026  How Docker Works: Namespaces, Cgroups, Union Filesystems, and the Container Runtime from Build to Execution  A deep dive into Docker internals covering Linux namespace isolation, cgroup resource constraints, OverlayFS copy-on-write layer mechanics, Dockerfile build cache invalidation rules, the containerd and runc OCI runtime stack, and production considerations for image hardening and startup latency.  ](/blog/devops/how-docker-works-namespaces-cgroups-union-filesystems-and-the-container-runtime-from-build-to-execution/)[ DevOps  · May 15, 2026  How Containers Actually Work: Namespaces, Cgroups, and the Linux Primitives Behind Docker  A deep dive into the Linux kernel primitives that make containers possible: PID, network, and mount namespaces for isolation, cgroups v2 for resource enforcement, union filesystems for layered images, and how to debug resource limit failures in Kubernetes production workloads.  ](/blog/devops/how-containers-actually-work-namespaces-cgroups-and-the-linux-primitives-behind-docker/)

[ ← All articles ](/blog/) [ More DevOps → ](/blog/category/devops/)
