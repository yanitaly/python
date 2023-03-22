#!/bin/bash  

############################################################################################
###  Red Hat Certified Specialist in Linux Diagnostics and Troubleshooting (EX342)       ###
###  ACG training notes            22.03.2023                                            ###
############################################################################################
 
## ch2. General Troubleshooting Methods ===========================================
# 2.1. Sys info and docs: Troubleshoot a Permissions Problem By Leveraging Systems Information and Documentation
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

# 2.2. Performance co-pilot(PCP): Use Performance Co-Pilot to Monitor Systems
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

# 2.3. Remote logging: Troubleshooting a Remote Logging Configuration
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

## ch3. System Startup Issues  ===============================================================
# 3.1. Manage Kernel Modules and Parameters
modinfo -p iscsi_tcp # show module is off
cat /sys/module/iscsi_tcp # not available 
lsmod | grep iscsi_tcp  # no iscsci_tcp 
modprobe iscsi_tcp debug_iscsi_tcp=1
lsmod | grep iscsi_tcp  # iscsci_tcp 
cat /sys/module/iscsi_tcp/parameters/debug_iscsci_tcp  # return 1 

# 3.2. Service: Troubleshooting Service Failures Upon Boot
# issue:  pmcd service wont start, service dependency issue that is causing problems
Confirm the Issue:
    systemctl status pmcd
    systemctl start pmcd # shows cycle dependency: depends.conf
Resolve the Problem:
    vim /etc/systemd/system/pmcd.service.d/depends.conf  # shows 'requres' and after' grafana.service at the same time > remove it 
    systemctl start grafana-server
    systemctl status grafana-server
    vim /etc/systemd/system/grafana-server.service.d/depends.conf # same, remove cycle dependence 
Start the Services
    systemctl status pmcd
    systemctl start pmcd
    systemctl status grafana-server

## ch4. File System Issues =============================================================
## 4.1 FS: Recover a Corrupted File System
#  issue: XFS and EXT file systems offer tools to aid in the repair and recovery of a broken file system.
# Discover and Attempt to Mount the File Systems
    cat /etc/fstab 
    mount /images/ # shows wrong fs type 
    mount /videos/ # shows wrong fs type 
# Repair the File Systems
    xfs_repair /dev/nvme1n1p1
    e2fsck -p /dev/nvme1n1p2  # still error showing you need to locate a valid superblock
    mkfs.ext4 -n /dev/nvme1n1p2 # return superblock 221185 
    e2fsck -p /dev/nvme1n1p2 -b 221185
# Mount the File Systems
    mount /images/ # shows wrong fs type 
    mount /videos/ # shows wrong fs type 
    ls /images/
    ls /videos/

# 4.2 restore LVM: Troubleshoot a Broken LVM Configuration
# Attempt to Mount the File System
    cat /etc/fstab
    mount /data/
# Recover the File System
    vgcfgrestore -l vgdata # get <BACKUP LOCATION>
    vgcfgrestore -f <BACKUP LOCATION> vgdata
    lvchange -an /dev/vgdata/lvdata
    lvchange -ay /dev/vgdata/lvdata
# Mount the File System
    cat /etc/fstab
    ls /data/

# 4.3 Encrypted LUKs: Recover Data From an Encrypted File System
mount /data  # device /dev/mapper/vgdata-lvdata luks-vgdata-lvdata not exist 
lsblk 
ls /dev/mapper
cat /etc/fstab 
cat /etc/crypttab  # /root/secret.key 
cryptsetup luksOpen /dev/mapper/vgdata-lvdata luks-vgdata-lvdata --key-file /root/secret.key  # no useable key available 
ls /root/backups/vgdata-lvdata.header  # OK 
cryptsetup luksHeaderRestore /dev/mapper/vgdata-lvdata --header-backup-file /root/backups/vgdata-lvdata.header
cryptsetup luksOpen /dev/mapper/vgdata-lvdata luks-vgdata-lvdata --key-file /root/secret.key
mount /data

# 4.4 iSCSI: Troubleshoot an iSCSI Issue
# issue: (Storage/Target server vs APP server):
Target: 
    systemctl status target
    ss -lpt 
    targetcli    # can retrieve initiator name 
APP: 
    telnet 10.0.1.101 3260  # run on App server, iscsi port 3260 > return OK 
    cat /etc/iscsi/initiatorname.iscsi # return initiator name, matches above
    iscsiadm -m discovery -t sendtargets -p 10.0.1.101 # OK, returns iqn.xxx
    iscsiadm -m node -T iqn.2003-01.org.linux-iscsi.ip-10-0-1-10.x8664:sn.a3776832068c -l # auth failure 
Target: 
    iscsi/iqn.2003-01.org.linux-iscsi.ip-10-0-1-10.x8664:sn.a3776832068c/tpg1
    get auth
APP: 
    vim /etc/iscsi/iscsid.conf # /CHAP comment out, lines
    # node.session.auth.authmethod = CHAP
    # node.session.auth.username = server2
    # node.session.auth.password = secret
    systemctl restart iscsi
    iscsiadm -m node
    iscsiadm -m session
    iscsiadm -m node -T iqn.2003-01.org.linux-iscsi.ip-10-0-1-10.x8664:sn.a3776832068c -l # still return error, as discovery config still use previous config 
    iscsiadm -m node -o delete
    iscsiadm -m discovery -t sendtargets -p 10.0.1.101
    iscsiadm -m node -T iqn.2003-01.org.linux-iscsi.ip-10-0-1-10.x8664:sn.a3776832068c -l # OK 
    iscsiadm -m session # confirm 

## ch5. Pkg management  ==========================================================
# 5.1 Pkg dependency: Fix Package Dependency Issues
# issue: can't install rube 2.5.9
Reproduce the Issue
dnf update ruby # nothing  to do 
dnf install rube.2.5.9 # no match 
ruby -v # 2.5.3 
dnf list --showduplicates ruby  # 2.5.9 available 
dnf versionlock list  # return ruby 
dnf versionlock delete ruby 
dnf install rube.2.5.9 # OK 

# 5.2 RPM: Recover a Corrupted RPM Database
# issue: can't install rpm > rpm db corrupted? 
dnf install vim -y # errror
cd /var/lib/rpm
ls 
/usr/lib/rpm/rpmdb_verify Packages 
lsof | grep /var/lib/rpm # check open logs
rm -rf /var/lib/rpm/__db* # remore potential logs 
mv Packages Packages.bak
/usr/lib/rpm/rpmdb_dump Packages.bak | /usr/lib/rpm/rpmdb_load Packages # Dump the contents of the Packages.bak file and load a new Packages file
/usr/lib/rpm/rpmdb_verify Packages # OK 
rpm -vv --rebuilddb # rebuilt rpm db 
dnf install vim -y # return unable to detect release version 
echo "8" >> /etc/yum/vars/releasever
dnf clean all
dnf repolist -v
dnf install vim -y

# 5.3 Restore: Restore Changed System Files
# issue: can't start mysql
# attempt to start mysqld > discover and restore changed mysql files
systemctl status mysqld
systemctl start mysqld
rpm -V mysql-server  # shows user group change, perms change, files content change too
ls /etc/my.cnf.d # show owned by clouduser, should be root?
rpm --setperms mysql-server  #  verify with: rpm -V mysql-server  
rpm --setugids mysql-server #  verify with: rpm -V mysql-server > /usr/lib/systemd/system/mysqld.service
cat /usr/lib/systemd/system/mysqld.service # shows suspecious contents
dnf reinstall mysql-server #  verify with: rpm -V mysql-server  > return none > OK 
systemctl start mysqld

## ch6. Networking Issues =======================================================
# 6.1 Troubleshoot Network Connectivity
# issue: can't connect to mysql db
APP: 
    mysql -u <user> -h 10.0.1.105 -p <password> # can't connect 
    ping 10.0.1.105 # OK 
DB:
    systemctl stop mariadb # 
    nc -l 3306 # open port 
APP:
    nc 10.0.1.105 3306 #  no route 
DB: 
    systemctl enable --now mariadb
    firewall-cmd --list-all
    firewall-cmd --permanent --zone=public --add-service=mysql
    firewall-cmd --reload
APP:
    mysql -u remote -h 10.0.1.105 -pastrongpass
    show databases;
    create database purchases;
    show databases;
DB:
    mysql
    show databases;

# 6.2 Inspect Network Traffic
tshark -i eth0 'port 3306' # or tcpdump, show traffic 
tshark -i eth0 -c 50 -w /tmp/mysql.pcap 'port 3306' # save 50 samples of traffic to file 
tshark -r /tmp/mysql.pcap #  shows attempted connections to port 3306 as well as some responses 

## ch7. APP ===================================================================
# 7.1 Troubleshooting Library Dependency Issues
# issue: tcpdump not working 
# run cmd > check libs
tcpdump -c 5 -i eth0  # shows libpcap.so.1 issue 
ldd $(which tcpdump)  | grep libpcap 
dnf whatprovides */libpcap.so*
dnf reinstall -y libpcap
tcpdump -c 5 -i eth0 # OK 

# 7.2 Use Standard Application Debugging Tools on Linux
# 7.3 Resolving SELinux Issues

## ch8. Authentication ========================================================
# Troubleshoot an Issue with the Pluggable Authentication Module

## ch9. 3pp ====================================================================
# Troubleshoot Kernel Issues
