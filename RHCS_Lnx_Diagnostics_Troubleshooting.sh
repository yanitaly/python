#!/bin/bash  

############################################################################################
###  Red Hat Certified Specialist in Linux Diagnostics and Troubleshooting (EX342)       ###
###  ACG training notes            22.03.2023                                            ###
############################################################################################
 

# 1. Sys info and docs: Troubleshoot a Permissions Problem By Leveraging Systems Information and Documentation
# issue: can not load websites like google in browser. 
Identify: 
    uptime  # determine if load issues
    free -h # check the memory
    df -h # disk space 
    top # top to check for issues
    systemctl status httpd -l # check status,  points to config 
    vi /etc/httpd/sites-enabled/booksite.conf # error points virtualhost conf
Solve: 
    man -k httpd
    man httpd 
    man httpd.conf  # good example 
    vi /usr/share/local/doc/httpd-vhosts.conf  # correct format using good example 
    systemctl restart httpd 
    systemctl status httpd

# 2. Performance co-pilot(PCP): Use Performance Co-Pilot to Monitor Systems
# issue: CPU spikes 
First try: 
    pminfo | grep cpu  # CPU metrics:
    pmrep -a /var/log/pcp/pmlogger/app/20220211.19.50.0 -S "@Feb 11 00:00:00 2022" -T "@Feb 12 00:00:00 2022" -t 10s kernel.cpu.util.sys | less
    pmrep kernel.cpu.util.sys # check if issue still happens
    pcp atop  # return high cpu usage app pid 
    kill -9 <PROCESS_ID>
    kill -9 <PROCESS_ID>
See if the issue has been solved:
    pmrep kernel.cpu.util.sys -T 1m  # See if the issue has been solved:
    ps axjf | less  # search for /yes > parent processes points to /opt/scripts/logger.sh
    cat /opt/scripts/logger.sh
    pcp atop # u > shows root uses most user 
    crontab -e # shows root not using crontab 
    systemctl list-units --type=service --state=running # shows strange logger.service 
    cat /etc/systemd/system/logger.service # shows restart the script every 10s
    systemctl stop logger
    systemctl disable logger

# 3. Remote logging: Troubleshooting a Remote Logging Configuration
# issue: APP server can't no longer log to LOG server
LOG server: 
    systemctl status rsyslog  # shows two issues 1. /etc/rsyslog.conf on ServerName  2. perm denied for tcp sockets
    systemctl status firewalld # firewalld not found > OK > check sestatus 
    sestatus  # enforcing mode > this causes problem
    semanage port -a -t syslogd_port_t -p tcp 30514 # 
    vim /etc/rsyslog.conf  # *.error;crit;alert;emerg.  /ServerName  > -?ServerName
    systemctl restart rsyslog
    systemctl status rsyslog
    ss -lpt # check on LOG server if syslog is listening correctly > YES
APP server: 
    logger blabla -p user.emerg  # from APP server, sent a test message 
    cd /var/log/hosts/app # no logs
    ss -lpt # check on APP server if syslog is listening correctly > NO 
    vi /etc/rsyslog.d/remotelogging.conf  # shows wrong port, correct it to 30514
    semanage port -a -t syslogd_port_t -p tcp 30514
    systemctl restart rsyslog
    systemctl status rsyslog
LOG server: 
    cat /var/log/hosts/app.log | grep blabla

# 4. Manage Kernel Modules and Parameters
modinfo -p iscsi_tcp
cat /sys/module/iscsi_tcp # not available 
lsmod | grep iscsi_tcp  # no iscsci_tcp 
modprobe iscsi_tcp debug_iscsi_tcp=1
lsmod | grep iscsi_tcp  # iscsci_tcp 
cat /sys/module/iscsi_tcp/parameters/debug_iscsci_tcp  # return 1 

# 5. Service: Troubleshooting Service Failures Upon Boot

# 6. FS: Recover a Corrupted File System

# 7. LVM: Troubleshoot a Broken LVM Configuration

# 8. Encrypted: Recover Data From an Encrypted File System

# 9. iSCSI: Troubleshoot an iSCSI Issue

# 10. Pkg dependency: Fix Package Dependency Issues

# 11. RPM: Recover a Corrupted RPM Database

# 12. Restore: Restore Changed System Files
