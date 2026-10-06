---
source: "https://swiftorial.com/tutorials/operating_systems/linux/security/implementing_selinux/"
title: "Implementing Selinux | Security | Linux Tutorial"
fetched_at: "2026-10-06 12:37"
---

# Implementing SELinux

## Introduction to SELinux

SELinux (Security-Enhanced Linux) is a security module integrated into the Linux kernel that provides a mechanism for supporting access control security policies. It is used to enforce the separation of information based on confidentiality and integrity requirements.

## Checking SELinux Status

Before making any changes, it's essential to check the current status of SELinux on your system. You can do this using the following command:

$ sestatus

SELinux status: enabled  
SELinuxfs mount: /sys/fs/selinux  
SELinux root directory: /etc/selinux  
Loaded policy name: targeted  
Current mode: enforcing  
Mode from config file: enforcing  
Policy MLS status: enabled  
Policy deny_unknown status: allowed  
Max kernel policy version: 31 

## Configuring SELinux Modes

SELinux operates in three modes:

  * **Enforcing:** SELinux policy is enforced.
  * **Permissive:** SELinux prints warnings instead of enforcing.
  * **Disabled:** No SELinux policy is loaded.



To change the SELinux mode, edit the `/etc/selinux/config` file:

$ sudo nano /etc/selinux/config

Modify the `SELINUX` line to one of the following:

SELINUX=enforcing  
SELINUX=permissive  
SELINUX=disabled

After making changes, reboot your system to apply the new SELinux mode:

$ sudo reboot

## Managing SELinux Policies

SELinux policies define how processes and users can interact with each other and with the system's resources. To list all installed SELinux policies:

$ sudo semanage policylist

To install a new policy module:

$ sudo semodule -i module_name.pp

To remove a policy module:

$ sudo semodule -r module_name

## Setting File Contexts

SELinux uses contexts to determine how files and processes interact. To view the current context of a file:

$ ls -Z /path/to/file

To change the context of a file:

$ sudo chcon -t type /path/to/file

For example, to change the type of a file to `httpd_sys_content_t`:

$ sudo chcon -t httpd_sys_content_t /var/www/html/index.html

To make these changes permanent, use the `semanage fcontext` command:

$ sudo semanage fcontext -a -t type /path/to/file

Then apply the changes with:

$ sudo restorecon -v /path/to/file

## Troubleshooting SELinux Issues

SELinux logs its activities and denials to `/var/log/audit/audit.log`. To search for SELinux denials:

$ sudo grep "SELinux is preventing" /var/log/audit/audit.log

You can use the `sealert` tool to get detailed information about SELinux denials:

$ sudo sealert -a /var/log/audit/audit.log

If you encounter an issue with a particular service, you can temporarily set SELinux to permissive mode for troubleshooting:

$ sudo setenforce 0

To re-enable enforcing mode:

$ sudo setenforce 1

## Conclusion

SELinux is a powerful tool for enhancing the security of your Linux system. By understanding how to check its status, configure its modes, manage policies, set file contexts, and troubleshoot issues, you can effectively implement SELinux to protect your system from unauthorized access and potential security threats.
