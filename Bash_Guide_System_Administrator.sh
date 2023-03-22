#!/bin/bash

#######################################################################
##  The System Administrator’s Guide to Bash Scripting - NEW 2020    ##
##   Study notes    22.03.2023                                       ##
#######################################################################

# ch2 Basics of Bash Scripting ===============================
# 1. special characters 
echo "This is $PATH"  # always substitution 
echo 'This is $PATH'  # print as it is,no substitution 

# 2. and / or  
echo "Hello world" && echo 'this will print'   # with && next cmd is only executed only when previous cmd exit with O 
echo "Hello world" || echo 'this will NOT print'   # with || next cmd is only executed only when previous cmd exit with 1 
cp /usr/bin/fake /usr/ && echo 'this will NOT print'  # With && next cmd is only executed only when previous cmd exit with 1 
cp /usr/bin/fake /usr/ || echo 'this will print'  # with || next cmd is only executed only when previous cmd exit with 1 

# 3. redirection I/O
sort < unsorted_list.txt > sorted_list.txt 
file describer: 
    0 input
    1 stdout
    2 stderr 
cmd > file 2>&1  # e.g. both stdout and stderr to a file

# utility cmds
sort, uniq, grep fmt, tr, head/tail, sed, awk 

# pipes
cmd1 | cmd2 # cmd1 output is input for cmd2 

# Demoggification / UUOC 
cat /etc/passwd | grep rob # wrong 
grep rob /etc/passwd  # right 

# ch2 Basics of Bash Scripting ===============================
