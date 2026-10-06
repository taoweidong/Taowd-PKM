---
source: "https://www.devfieldguide.com/blog/systemd-linux-services-explained"
title: "systemd and Linux Services Explained: Managing Background Processes | DevFieldGuide"
fetched_at: "2026-10-06 12:37"
---

### 

Nearly every modern Linux distribution uses systemd to manage background services — understanding it directly replaces a lot of "restart it and hope" troubleshooting with actually reading what went wrong.

## The core commands

bash
    
    
    systemctl start nginx        # start now (this session only)
    systemctl stop nginx          # stop now
    systemctl restart nginx       # stop then start
    systemctl status nginx        # current state + recent log lines
    systemctl enable nginx        # start automatically on future boots
    systemctl disable nginx       # don't start automatically anymore
    systemctl enable --now nginx  # enable AND start in one command

The `enable` vs. `start` distinction is the single most common point of confusion — `start` alone doesn't survive a reboot, and `enable` alone doesn't affect the current session.

## A minimal unit file

A **unit file** defines a service — what command to run, when to start it, and how to restart it on failure:

ini
    
    
    # /etc/systemd/system/my-app.service
    [Unit]
    Description=My background application
    After=network.target
     
    [Service]
    ExecStart=/usr/bin/node /opt/my-app/server.js
    Restart=on-failure
    RestartSec=5
    User=myappuser
    Environment=NODE_ENV=production
     
    [Install]
    WantedBy=multi-user.target

After creating or editing a unit file, systemd needs to be told to re-read it:

bash
    
    
    systemctl daemon-reload
    systemctl enable --now my-app

## The three sections, briefly

  * **`[Unit]`** — metadata and ordering: a description, and `After=`/`Requires=` to control what this service should start after (or depend on).
  * **`[Service]`** — the actual behavior: what command runs (`ExecStart`), what to do on failure (`Restart=on-failure`), which user runs it, and environment variables.
  * **`[Install]`** — how this unit integrates with `enable` — `WantedBy=multi-user.target` is the standard choice for a normal background service that should start at boot.



## Reading logs with journalctl

systemd captures a service's stdout/stderr automatically — `journalctl` is how you read it, and it's almost always the actual answer to "why did my service fail":

bash
    
    
    journalctl -u my-app                # all logs for this unit
    journalctl -u my-app -f              # follow in real time, like tail -f
    journalctl -u my-app --since "1 hour ago"
    journalctl -u my-app -n 50           # last 50 lines

`systemctl status` shows a truncated preview of recent log lines — when that's not enough context, `journalctl -u <service>` shows the complete picture.

## Automatic restart on failure

`Restart=on-failure` (in the unit file above) is what keeps a crashed service running without manual intervention — but it's worth pairing with limits, since an unbounded restart loop on a genuinely broken service just burns CPU repeatedly failing:

ini
    
    
    [Service]
    Restart=on-failure
    RestartSec=5
    StartLimitIntervalSec=60
    StartLimitBurst=3

`StartLimitBurst=3` within `StartLimitIntervalSec=60` means systemd gives up (rather than looping forever) after 3 failed restarts within 60 seconds — a genuinely broken service fails loudly and stays stopped, rather than consuming resources in an infinite crash loop.

## Timers: systemd's alternative to cron

systemd can also schedule recurring jobs, as a modern alternative to a crontab entry — pairing a `.service` unit (what to run) with a `.timer` unit (when to run it):

ini
    
    
    # /etc/systemd/system/backup.timer
    [Timer]
    OnCalendar=daily
    Persistent=true
     
    [Install]
    WantedBy=timers.target

bash
    
    
    systemctl enable --now backup.timer
    systemctl list-timers  # see all scheduled timers and their next run

`Persistent=true` means a missed run (the machine was off at the scheduled time) executes as soon as the system is back up — a real advantage over plain cron, which simply skips a run the machine wasn't on for.

## Checking why a service failed to start

`systemctl status` reports the immediate failure reason, but for a genuinely unclear failure, checking the exit code and the full log together usually explains it:

bash
    
    
    systemctl status my-app
    # Look for: "Active: failed (Result: exit-code)" and the "Main PID" exit status
     
    journalctl -u my-app -n 100 --no-pager

A service failing immediately on every start attempt (rather than running for a while first) is very often a configuration or permissions issue — a wrong path in `ExecStart`, a `User=` that doesn't have permission to bind the configured port, or a missing environment variable the application expects.

## Reloading config without a full restart

Some services support reloading their configuration without dropping active connections — `systemctl reload` sends the service a signal (typically `SIGHUP`) it can handle to re-read config, rather than the harder stop-then-start of a full restart:

bash
    
    
    systemctl reload nginx        # nginx re-reads config, no dropped connections
    systemctl reload-or-restart my-app  # reload if supported, else restart

Not every service supports this — it depends on the application itself handling the reload signal — but for ones that do (nginx being the canonical example), it's meaningfully less disruptive than a full restart for a routine config change.

## Sockets: starting a service on demand

systemd can also start a service lazily, the first time something connects to its configured socket, rather than always running in the background:

ini
    
    
    # my-app.socket
    [Socket]
    ListenStream=8080
     
    [Install]
    WantedBy=sockets.target

bash
    
    
    systemctl enable --now my-app.socket

The service itself only starts when the first connection actually arrives on port 8080 — useful for infrequently-used services where running constantly in the background would be wasted resources, at the cost of a small startup delay on that first connection.

## Common mistakes

Common mistakes

  * Editing a unit file and forgetting `systemctl daemon-reload` afterward. systemd caches unit definitions in memory — an edited file has no effect until systemd is told to re-read it.
  * Running `systemctl start` without `enable` and assuming the service will survive a reboot. It won't — `start` alone is scoped to the current boot session only.
  * Debugging a failed service from `systemctl status`'s truncated log preview alone, instead of the full `journalctl -u <service>` output, which usually contains the actual error the preview cut off.
  * Setting `Restart=on-failure` with no `StartLimitBurst`, letting a genuinely broken service loop restart attempts indefinitely instead of failing loudly and staying stopped after a reasonable number of attempts.



  * [Essential Linux Commands Every Developer Should Know](/docs/essential-linux-commands-every-developer/) — shares tags: linux, devops (same category).
  * [Understanding File Permissions in Linux (chmod, chown Explained)](/docs/linux-file-permissions-chmod-chown-explained/) — shares tags: linux.
  * [Docker Compose for Local Development Environments](/blog/docker-compose-local-development/) — shares tags: devops.
  * [CI/CD Pipelines Explained: From Commit to Production](/blog/cicd-pipelines-explained/) — shares tags: devops.
  * [Infrastructure as Code: Why Terraform Won](/blog/infrastructure-as-code-why-terraform-won/) — shares tags: devops.



[#linux](/tags/linux/)[#devops](/tags/devops/)

Advertisement

## Go deeper

[Command ReferenceLinux syntax & examples](/commands/linux/)[Cheat SheetOne page, searchable, copy-ready](/cheatsheets/linux/)[Learning PathA structured roadmap through this topic](/learning-paths/linux/)

## Frequently Asked Questions

### 

### 

Advertisement

[DevFieldGuide](/about/)

Editorial Team

Practical tutorials and developer tools, written and maintained by the DevFieldGuide team.

[](https://twitter.com/devfieldguide)[](https://github.com/devfieldguide)[](https://linkedin.com/company/devfieldguide)

### Enjoyed this article?

Get the next one straight to your inbox, along with the best of what we publish each week.

## Related Articles

[LinuxdocsUnderstanding File Permissions in Linux (chmod, chown Explained)How Linux's read/write/execute permission model actually works, what chmod's numeric codes mean, and when to reach for chown instead.DevFieldGuideJul 20, 20266 min read](/docs/linux-file-permissions-chmod-chown-explained/)[LinuxdocsEssential Linux Commands Every Developer Should KnowA practical reference for the Linux commands you'll actually reach for day to day — file navigation, process management, and text processing.DevFieldGuideJun 22, 20266 min read](/docs/essential-linux-commands-every-developer/)[ClouddocsAWS vs. Azure vs. GCP: Choosing the Right Cloud for Your ProjectA practical comparison of the three major cloud providers — where each genuinely differentiates, and the factors that should actually drive the decision.DevFieldGuideJul 29, 20266 min read](/docs/aws-vs-azure-vs-gcp-choosing/)

## More in Linux

[View all ](/categories/linux/)

  * [Understanding File Permissions in Linux (chmod, chown Explained)](/docs/linux-file-permissions-chmod-chown-explained/)
  * [Essential Linux Commands Every Developer Should Know](/docs/essential-linux-commands-every-developer/)


