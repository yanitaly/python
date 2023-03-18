#!/usr/bin/env python3.6 
### ACG online training: Python 3 Scripting for System Administrators
### 17.03.2023 

"""
Notes:
1. quotes  
- use double quotes around strings that are used for interpolation or that are natural language messages, 
- single quotes for small symbol-like strings, but will break the rules if the strings contain quotes, or if I forget. 
- triple double quotes for docstrings and raw string literals for regular expressions even if they aren't needed.
"""    

## Intermediate Scriptiong: 8.1 parsing command line params ======================
import sys 
print(f"First sys arguement: {sys.argv[0]}") # First sys arguement: c:/Users/xiaon/Desktop/python_for_adm/python_ansible/temp_python3_for_SysAdmin.py
print(f"Positional arguements: {sys.argv[1:]}") 
# temp_python3_for_SysAdmin.py test1 test2 'another argument'
# Positional arguements: ['test1', 'test2', 'another argument']

## Intermediate Scriptiong: 8.1 robust CLIs with argparse  ======================
import argparse
# e.g.1 build parser
parser = argparse.ArgumentParser()
parser.add_argument('filename', help='file to read')
args = parser.parse_args()
print(args) # Namespace(filename='.\\io_file.txt')

# e.g.2 build parser
parser = argparse.ArgumentParser(description='Read a file in reverse')
parser.add_argument('filename', help='file to read')
parser.add_argument('--limit', '-l', type=int, help='The number of lines to read')
args = parser.parse_args()
print(args) # Namespace(filename='.\\io_file.txt', limit=None)

# e.g.3 build parser
import argparse
parser = argparse.ArgumentParser(description='Read a file in reverse')
parser.add_argument('--version', '-v', action='version', version='%(prog)s 1.0')
parser.add_argument('filename', help='file to read')
parser.add_argument('--limit', '-l', type=int, help='The number of lines to read')
# parse arguments
args = parser.parse_args()
print(args)  # -v > temp_python3_for_SysAdmin.py 1.0

# read file, and reverse content and print
with open(args.filename) as f:
    lines = f.readlines()
    lines.reverse()
    if args.limit:
        lines = lines[:args.limit]
    for line in lines:
        print(line.strip()[::-1])
#   temp_python3_for_SysAdmin.py  io_file.txt     
#   3enil si siht
#   2enil si siht
#   1enil si siht
#   temp_python3_for_SysAdmin.py  io_file.txt  -l 2  
#   3enil si siht
#   2enil si siht

## Intermediate Scriptiong: 8.2 Error handling try/except/else/finally  ======================
# e.g. open a file not existing without exec Traceback errors. 
import argparse
parser = argparse.ArgumentParser(description='Read a file in reverse')
parser.add_argument('--version', '-v', action='version', version='%(prog)s 1.0')
parser.add_argument('filename', help='file to read')
parser.add_argument('--limit', '-l', type=int, help='The number of lines to read')
# parse arguments
args = parser.parse_args()
# read file, and reverse content and print
try:
    f = open(args.filename)
    limit = args.limit
except FileNotFoundError as err:
    print(f"Error: {err}")
else: 
    with f:
        lines = f.readlines()
        lines.reverse()
        if args.limit:
            lines = lines[:args.limit]
        for line in lines:
            print(line.strip()[::-1])
finally:
        print("Finally")  # this always runs
#   Error: [Errno 2] No such file or directory: 'fake.txt'

## Intermediate Scriptiong: 8.3 Exit statuses  ======================
# sys.exit(1) # add this to EXCEPT

## Intermediate Scripting: 8.4 Exe external program  ======================
import subprocess 
proc = subprocess.run(["ls"])
proc = subprocess.run(["ls"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(proc.stdout) # redirect output, returns string
print(proc.stdout.decode()) # returns byte object (raw, non decoded info)
proc = subprocess.run(['cat', 'fake.txt'], check=True) # check=True creates traceback, allows us using Except
# subprocess.run > popen

## Intermediate Scripting: 8.5 advanced iteration with List Comprehensions ======================
import argparse 
parser = argparse.ArgumentParser(description="Search for words including partial word")
parser.add_argument('snippet', help='partial or complete string to search for in words')
args = parser.parse_args()
snippet = args.snippet.lower()
# option1
with open('/usr/share/dict/words') as f:
    words = f.readlines()
matches = []
for word in words:
    if snippet in word.lower():
        matches.append(word)
print(matches) # script.py Keith > ['Keith\n', 'Keithley\n', 'Keithsburg\n', 'Keithville\n']

# option2 list comprehension
matches = [word for word in words if snippet in word.lower()] # [item for item in my_list]
print(matches)  # script.py Keith > ['Keith\n', 'Keithley\n', 'Keithsburg\n', 'Keithville\n']
matches = [word.strip() for word in words if snippet in word.lower()]
print(matches) #  script.py Keith > ['Keith', 'Keithley', 'Keithsburg', 'Keithville']
