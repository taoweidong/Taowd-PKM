---
source: "https://arfin.dev/blog/docker-mastery-production-systems"
title: "Docker Best Practices: Multi-stage Builds & Security | Arfin Nasir"
fetched_at: "2026-10-06 12:33"
---

* * *

The phrase "It works on my machine" used to be a punchline. Today, with containerization, it should be a relic of the past. Yet, I still audit codebases where Docker is treated as a magical black box—a tool that simply "packages stuff" without a deeper understanding of the underlying mechanics.

True expertise in **Docker** isn't about memorizing CLI flags. It's about understanding reproducibility, immutability, and isolation. It's about realizing that a container is not a lightweight VM; it is a **process with boundaries**.

In this deep dive, we move beyond the `docker run hello-world` tutorial phase. We will dissect the architecture of efficient images, the necessity of healthchecks, and the security baselines required to ship code you can actually trust.

> "Containers are not a deployment strategy; they are a unit of deployment. The strategy lies in how you build, secure, and orchestrate them."

* * *

## 1\. The Mental Model: Isolation vs. Virtualization

Before optimizing, we must visualize. The most common mistake teams make is treating containers like _mini-virtual machines_. They are not. A VM virtualizes the **hardware** ; a container virtualizes the **operating system**.

### Architecture Comparison: VM vs. Container

**Key Insight:** Notice the absence of a "Guest OS" in the container stack. Containers share the host kernel, which is why they boot in milliseconds and consume a fraction of the RAM. However, this also means _security isolation is softer_ than in VMs. 

Understanding this distinction is critical for security. Because you share the kernel, a breakout in a container can potentially impact the host. This is why running containers as `root` is a cardinal sin in production environments.

* * *

## 2\. The Architecture of Efficiency: Multi-Stage Builds

If your production image is 1GB for a 50MB Go binary, you are doing it wrong. Bloated images slow down CI/CD pipelines, increase attack surfaces, and waste storage.

The solution is the **Multi-Stage Build**. This pattern allows you to use a heavy image to _compile_ your code, and a lightweight image to _run_ it.

### The Multi-Stage Pipeline

**Why this matters:** The final image only contains what is explicitly copied from the previous stage. Build tools, compilers, and source code are left behind in the ephemeral builder layer. 

### Implementation Checklist for Slim Images

  * **Base Image:** Always start with `-alpine` or `-slim` variants unless you have a specific glibc dependency.
  * **Layer Caching:** Copy `package.json` or `go.mod` _before_ copying source code to leverage Docker's layer caching.
  * **Non-Root User:** Create a specific user (e.g., `appuser`) and switch to it using `USER appuser`.
  * **.dockerignore:** Ensure `node_modules`, `.git`, and local env files are excluded from the build context.



* * *

## 3\. Orchestrating Chaos with Docker Compose

Running a single container is easy. Running a stack of interconnected services (API, Database, Redis, Worker) via command line flags is a nightmare. `docker-compose` is the declarative standard for defining these relationships.

However, a common anti-pattern is using Compose for _everything_ , including production. While Compose is excellent for local development and small-scale staging, it lacks the self-healing and scaling capabilities of Kubernetes or Swarm.

> "Use Docker Compose to define the **local developer experience**. Use Kubernetes or ECS to define the **production resilience**."

### The "Healthcheck" Gap

The most critical missing piece in most Compose files is the `healthcheck`. By default, Docker considers a container "healthy" if the main process is running. But what if your database is accepting connections but deadlocking? Or your API is returning 500 errors?

You must define a logical check that proves the service is actually working.

### Logic Flow: Docker Healthcheck

**Implementation:** Define a `curl` or `pg_isready` command in your YAML. If this fails 3 times, Docker marks the container as unhealthy, allowing orchestrators to restart it automatically. 

* * *

## 4\. Security Baselines: Don't Ship Vulnerabilities

Security in Docker is not a plugin; it's a configuration habit. The default Docker setup is convenient, not secure.

#### ⚠️ Critical Security Risks to Avoid

  * **Running as Root:** If an attacker escapes your app, they have root on the container. If the kernel is vulnerable, they own the host. _Always use a non-root user._
  * **Hardcoded Secrets:** Never put API keys in your `Dockerfile`. Use `--secret` flags during build or inject via environment variables at runtime.
  * **Latest Tags:** Using `node:latest` is unpredictable. Pin specific versions (e.g., `node:18.4.0-alpine`) to ensure reproducible builds and known security patches.



When building your images, scan them. Tools like `trivy` or Docker's own `scout` can analyze your layers for known CVEs (Common Vulnerabilities and Exposures) before you ever push to a registry.

* * *

## Final Thoughts: Engineering Over Convenience

Docker democratized deployment, but it also created a generation of developers who copy-paste configurations without understanding the _why_. By focusing on multi-stage builds, explicit healthchecks, and strict security baselines, you move from simply "using Docker" to **engineering resilient systems**.

The goal isn't just to make it run. The goal is to make it run _forever_ , safely, and efficiently.

### Ready to optimize your infrastructure?

I help teams build production systems with Docker. Explore my portfolio or get in touch for consulting.

[Get in Touch](/contact)

* * *

## Frequently Asked Questions

### Should I use Docker in production?

Yes, but typically orchestrated by Kubernetes, ECS, or Nomad. Using raw `docker run` in production is risky due to lack of self-healing and load balancing capabilities.

### What is the difference between CMD and ENTRYPOINT?

`ENTRYPOINT` defines the main executable of the container. `CMD` provides default arguments to that executable. Use `ENTRYPOINT` for the binary you always want to run, and `CMD` for configurable flags.

### How do I persist data in Docker?

Containers are ephemeral; their filesystem disappears when they stop. To persist data (like databases), you must use **Volumes** which mount a directory from the host (or a managed volume) into the container.
