---
source: "https://pkg.jenkins.io/redhat-stable/"
title: "Rpm Jenkins Packages"
fetched_at: "2026-10-05 15:30:06"
---

# Jenkins Rpm Packages

## Red Hat and derivatives

To install Jenkins on Red Hat Enterprise Linux, AlmaLinux, Rocky Linux, Oracle Linux, or another Red Hat based distribution, you can utilize the instructions provided in our [Red Hat Enterprise Linux installation guide.](https://www.jenkins.io/doc/book/installing/linux/#red-hat-centos)

To install Jenkins on Fedora, use the instructions provided in our [Fedora installation guide](https://www.jenkins.io/doc/book/installing/linux/#fedora). 

## openSUSE

To use this repository with openSUSE, start by adding the requirements with the following command: 
    
    
    
        zypper install dejavu-fonts fontconfig java-21-openjdk wget
      

Then add the repository with run the following command: 
    
    
    
        wget -O /etc/zypp/repos.d/jenkins.repo \
          https://pkg.jenkins.io/rpm-stable/jenkins.repo
      

With that set up, the Jenkins package can be installed with: 
    
    
    
        zypper install jenkins
      

You will need to explicitly install a supported Java runtime environment (JRE), either from your distribution (as described above) or another Java vendor (e.g., [Adoptium](https://adoptium.net/)). 

To determine the Java version that is supported for your Jenkins environment, please refer to the [Java support policy.](https://www.jenkins.io/doc/book/platform-information/support-policy-java/#running-jenkins-system)

See [the installation guide](https://www.jenkins.io/doc/book/installing/) for more information, including how Jenkins is run and where the configuration is stored, etc. 
