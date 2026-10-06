---
source: "https://linuxserverlab.com/?p=419/"
title: "The Ultimate Docker Compose Homelab Stack: 15 Self-Hosted Apps In Minutes"
fetched_at: "2026-10-06 12:40"
---

[Server Administration](https://linuxserverlab.com/category/server-administration/)

August 1, 2026

# The Ultimate Docker Compose Homelab Stack: 15 Self-Hosted Apps in Minutes

Running a homelab shouldn’t mean manually configuring twenty different services across twenty different servers. 

Running a homelab shouldn’t mean manually configuring twenty different services across twenty different servers. A well-planned **docker compose homelab stack** lets you deploy an entire self-hosted ecosystem with a single command — from media streaming and file sync to monitoring and automated backups. **Why Docker Compose?** Docker Compose is the simplest way to define, configure, and run multi-container applications. Instead of installing each service natively and fighting dependency conflicts, you describe your entire **homelab stack** in one YAML file. This makes your setup portable, reproducible, and dead simple to maintain or migrate to new hardware. **The Complete Stack** Here’s a production-ready **docker compose homelab stack** covering the most useful categories for 2026: **Reverse Proxy & SSL**
    
    
    YAMLnginx-proxy-manager:
      image: jc21/nginx-proxy-manager
      ports: ["80:80", "443:443", "81:81"]
      volumes:
        - ./npm:/data
    

**Media Server**
    
    
    YAMLjellyfin:
      image: jellyfin/jellyfin:latest
      volumes:
        - /mnt/media:/media
        - ./jellyfin:/config
    

**File Sync**
    
    
    YAMLnextcloud:
      image: nextcloud:latest
      volumes:
        - ./nextcloud:/var/www/html
    

**Password Manager**
    
    
    YAMLvaultwarden:
      image: vaultwarden/server:latest
      volumes:
        - ./vaultwarden:/data
    

**Monitoring**
    
    
    YAMLprometheus:
      image: prom/prometheus:latest
    grafana:
      image: grafana/grafana:latest
    

**Backup**
    
    
    YAMLrestic:
      image: restic/restic:latest
      volumes:
        - ./backup:/backup
    

**Deployment Steps** 1\. Create a `docker-compose.yml` file with the stack above 2. Run `docker compose up -d` from the directory 3. Access each service through your reverse proxy domain **Why This Works Better** Most homelab guides scatter setup instructions across separate articles. This **docker compose homelab stack** gives you a single, copy-paste foundation that works out of the box. You can add or remove services without breaking the rest of your infrastructure. **Final Thoughts** A solid **self-hosted stack** is the backbone of every great homelab. Start with this **homelab docker compose** template, then expand it with apps like Immich, Paperless-ngx, or Home Assistant as your needs grow. —

## Related Posts

  * [Docker vs Podman: Which Container Tool Should You Use?](https://linuxserverlab.com/docker-vs-podman-which-container-tool-should-you-use/)
  * [How to Monitor Server Health with Netdata](https://linuxserverlab.com/how-to-monitor-server-health-with-netdata/)
  * [How to Automate Linux Server Updates with Unattended-Upgrades](https://linuxserverlab.com/how-to-automate-linux-server-updates-unattended-upgrade/)



## Comments
