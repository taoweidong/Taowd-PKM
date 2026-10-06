---
source: "https://vps.do/best-self-hosted-apps-to-run-on-your-vps-in-2025-nextcloud-gitea-bitwarden-more"
title: "Best Self-Hosted Apps to Run on Your VPS in 2025: Nextcloud, Gitea, Bitwarden & More - VPS.DO"
fetched_at: "2026-10-06 12:50"
---

### Best Self-Hosted Apps to Run on Your VPS in 2025: Nextcloud, Gitea, Bitwarden & More

  * By [VPS.DO](https://vps.do/author/ytedarnge/)
  * [June 8, 2026](https://vps.do/best-self-hosted-apps-to-run-on-your-vps-in-2025-nextcloud-gitea-bitwarden-more/)



Self-hosting applications on your own VPS lets you replace expensive SaaS subscriptions, maintain complete ownership of your data, and customize tools to your exact needs. The self-hosted software ecosystem has matured significantly — many open-source alternatives now match or exceed their commercial counterparts in features and usability. This guide covers the best self-hosted applications for a VPS in 2025, organized by category, with deployment notes for each.

## Why Self-Host on a VPS?

  * **Data sovereignty** : Your files, passwords, and analytics stay on hardware you control — not in a third party’s data center under their terms of service.
  * **Cost savings** : A single $10–$20/month VPS can replace hundreds of dollars in monthly SaaS subscriptions for teams that self-host multiple tools.
  * **Customization** : Open-source software can be modified, extended, and integrated with other tools in ways SaaS products do not permit.
  * **Privacy** : No telemetry, no usage analytics sent to vendors, no risk of your data being used for AI training or marketing purposes.



## File Storage and Collaboration

### Nextcloud — Self-Hosted Cloud Storage

Nextcloud is the most feature-complete Dropbox/Google Drive alternative available. It provides file storage and sync, calendar, contacts, video conferencing, document collaboration, and an extensive app ecosystem.

  * **VPS requirements** : 2 vCPU / 2 GB RAM minimum; 4 GB recommended for teams
  * **Storage** : Depends on data volume — use a VPS with expandable storage or mount object storage
  * **Stack** : Nginx + PHP-FPM + MariaDB + Redis (for file locking and caching)



Quick deploy with Docker:
    
    
    version: '3'
    services:
      nextcloud:
        image: nextcloud:stable
        restart: always
        ports:
          - "127.0.0.1:8080:80"
        volumes:
          - nextcloud_data:/var/www/html
        environment:
          - MYSQL_HOST=db
          - MYSQL_DATABASE=nextcloud
          - MYSQL_USER=nextcloud
          - MYSQL_PASSWORD=${DB_PASSWORD}
      db:
        image: mariadb:11
        restart: always
        volumes:
          - db_data:/var/lib/mysql
        environment:
          - MYSQL_ROOT_PASSWORD=${DB_ROOT_PASSWORD}
          - MYSQL_DATABASE=nextcloud
          - MYSQL_USER=nextcloud
          - MYSQL_PASSWORD=${DB_PASSWORD}

## Password Management

### Vaultwarden — Self-Hosted Bitwarden Server

Vaultwarden is a lightweight, unofficial Bitwarden server implementation written in Rust. It is compatible with all official Bitwarden clients (browser extensions, mobile apps, desktop apps) and requires a fraction of the resources of the official Bitwarden server.

  * **VPS requirements** : As little as 256 MB RAM — runs on the smallest VPS plans
  * **Why it matters** : Password managers are high-trust applications. Self-hosting ensures your password vault is never accessible to a third party, even in the event of a provider breach.


    
    
    docker run -d --name vaultwarden \
      -e DOMAIN=https://vault.yourdomain.com \
      -e SIGNUPS_ALLOWED=false \
      -v /vw-data/:/data/ \
      -p 127.0.0.1:8081:80 \
      --restart always \
      vaultwarden/server:latest

## Code Hosting and DevOps

### Gitea — Self-Hosted Git Service

Gitea is a lightweight, self-hosted GitHub alternative that provides git repository hosting, issues, pull requests, code review, CI/CD (with Gitea Actions), and package registries. It uses significantly less RAM than GitLab, making it practical on modest VPS plans.

  * **VPS requirements** : 1 vCPU / 512 MB RAM minimum; 1–2 GB recommended for teams
  * **Best for** : Development teams who want private git hosting without GitHub’s subscription costs or dependency on external infrastructure


    
    
    docker run -d --name=gitea \
      -e USER_UID=1000 -e USER_GID=1000 \
      -v gitea_data:/data \
      -p 127.0.0.1:3000:3000 \
      -p 2222:22 \
      --restart always \
      gitea/gitea:latest

### Woodpecker CI — Lightweight CI/CD Pipeline

Woodpecker CI integrates with Gitea (and GitHub/GitLab) to provide automated testing and deployment pipelines. Its YAML-based pipeline definition is simpler than GitHub Actions and runs entirely on your infrastructure.

## Monitoring and Uptime

### Uptime Kuma — Self-Hosted Status Page and Monitoring

Uptime Kuma monitors your websites, APIs, DNS, and TCP ports, and sends alerts via email, Slack, Discord, Telegram, and dozens of other integrations. It also generates a public status page for your services.

  * **VPS requirements** : 256 MB RAM
  * **Best feature** : Beautiful status pages that you control — no third-party branding


    
    
    docker run -d --restart=always \
      -p 127.0.0.1:3001:3001 \
      -v uptime-kuma:/app/data \
      --name uptime-kuma \
      louislam/uptime-kuma:1

### Netdata — Real-Time Server Metrics

Netdata provides beautiful, real-time monitoring of your VPS — CPU, RAM, disk I/O, network, Docker containers, databases, web servers, and more. It ships with hundreds of auto-detected collectors and a web interface accessible at port 19999.
    
    
    wget -O /tmp/netdata-install.sh https://my-netdata.io/kickstart.sh
    bash /tmp/netdata-install.sh

## Analytics

### Plausible Analytics — Privacy-First Web Analytics

Plausible is a lightweight, privacy-focused Google Analytics alternative that does not use cookies and is fully GDPR compliant out of the box. The self-hosted version gives you unlimited sites and data retention without a subscription fee.

  * **VPS requirements** : 1 vCPU / 1 GB RAM; uses ClickHouse for analytics storage (requires more RAM for high-traffic sites)
  * **Best for** : Publishers and businesses who need traffic analytics without compromising visitor privacy



### Umami — Simpler Analytics Alternative

Umami is a simpler analytics tool than Plausible, with lower resource requirements (uses PostgreSQL or MySQL instead of ClickHouse). It tracks pageviews, unique visitors, session duration, and referrers with a clean, minimal interface.
    
    
    docker run -d \
      -e DATABASE_URL=postgresql://umami:password@db:5432/umami \
      -p 127.0.0.1:3002:3000 \
      --name umami \
      ghcr.io/umami-software/umami:postgresql-latest

## Communication

### Matrix/Element — Self-Hosted Team Chat

Matrix is a decentralized, open communication protocol. Running a Synapse (Matrix homeserver) instance gives your team a Slack alternative with end-to-end encryption, file sharing, video calls, and bridges to other chat platforms.

  * **VPS requirements** : 2 vCPU / 2 GB RAM minimum; 4 GB RAM for active teams
  * **Note** : Matrix federation allows your users to communicate with users on other Matrix servers, creating a decentralized network.



### Mattermost — Enterprise Team Chat

Mattermost is a Slack-compatible open-source team chat platform with threads, channels, file sharing, integrations, and a rich app ecosystem. The self-hosted Community edition is free and supports unlimited users.

## Project Management and Knowledge Base

### Plane — Open-Source Jira Alternative

Plane provides issue tracking, project management, cycles (sprints), and modules with a clean interface that rivals commercial project management tools. The self-hosted version removes all per-seat pricing.

### Outline — Self-Hosted Team Wiki

Outline is a beautiful, Notion-inspired wiki and knowledge management tool. It supports Markdown, nested documents, search, and integrations with Slack and GitHub. The self-hosted version requires Node.js, PostgreSQL, and Redis.

## Recommended VPS Specifications by Use Case

Self-Hosted Stack | Minimum VPS | Comfortable VPS  
---|---|---  
Vaultwarden + Uptime Kuma | 1 vCPU / 512 MB RAM | 1 vCPU / 1 GB RAM  
Gitea + Woodpecker CI | 1 vCPU / 1 GB RAM | 2 vCPU / 2 GB RAM  
Nextcloud (personal) | 2 vCPU / 2 GB RAM | 2 vCPU / 4 GB RAM  
Nextcloud + Gitea + Uptime Kuma | 2 vCPU / 4 GB RAM | 4 vCPU / 8 GB RAM  
Full stack (all above) | 4 vCPU / 8 GB RAM | 8 vCPU / 16 GB RAM  
  
## Deployment Strategy: Docker Compose for All Services

The most maintainable approach for running multiple self-hosted applications is a single Docker Compose file that orchestrates all services with shared networks and a central Nginx reverse proxy handling SSL termination. Each service runs in its own container, accessible at a different subdomain (e.g., `files.yourdomain.com`, `git.yourdomain.com`, `vault.yourdomain.com`).

This architecture runs all these applications comfortably on a 4 vCPU / 4 GB RAM VPS with NVMe storage. See our [Docker and Docker Compose production setup guide](https://vps.do/blog/) for the reverse proxy and SSL configuration details.

## Getting Started

For a self-hosted application stack, a KVM VPS with at least 2 GB RAM and NVMe storage is the practical starting point. [KVM VPS plans at VPS.DO](https://vps.do/kvm/) provide the kernel-level access required for Docker, with NVMe storage for fast container I/O and root access for complete configuration control.

## Conclusion

The self-hosted software ecosystem in 2025 offers mature, polished alternatives to virtually every major SaaS category. A single KVM VPS running Docker Compose can replace cloud file storage, password management, git hosting, CI/CD, monitoring, analytics, and team communication tools — often for less than the cost of a single SaaS subscription. The combination of cost savings, data control, and customization makes self-hosting on a VPS one of the highest-value uses of cloud infrastructure for technically capable individuals and teams.
