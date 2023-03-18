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


## Basic Scriptiong: 7.1 user input ====================
# e.g.1
name = input("Your name? ")
birthday = input("Your birthday? ")
age = int(input("Your age? "))
print(f"Your name is: {name}, birthday is: {birthday}, Half of your age is: {age/2}")
#    Your name? Ning
#    Your birthday? Dec 02 
#    Your age? 34
#    Your name is: Ning, birthday is: Dec 02, Half of your age is: 17.0

## Basic Scriptiong: 7.2/7.3 functions ======================
# e.g.2 basic math
def add_two(num):
    return num + 2 
print (f" 11 add_two is: {add_two(11)}")
#    11 add_two is: 13

# e.g.3 bmi calculator 
# bmi = weight / hight by power 2, imperial = 703 * metric 
def gather_info():
    weight = float(input("Your weight (pounds or kilograms) is: "))
    height = float(input("Your height (inches or meters) is: "))
    system = input("system used is metric or imperial? ")
    return weight, height, system 
def caculate_bmi(weight, height, system='metric'):
    if system == 'metric':
        bmi = float(weight/height**2 )
    else:
        bmi = 703 * float(weight/height**2 )
    return bmi 
while True:
    weight, height, system = gather_info()
    if system.startswith('m'):
        bmi = caculate_bmi(weight, height, system='metri')
        print(f"Your BMI is: {bmi}")
        break 
    elif system.startswith("i"):
        bmi = caculate_bmi(weight, height, system='imperial')
        print(f"Your BMI is: {bmi}")
        break 
    else:
        print("Error: invalid measurement system. Please use metric or imperial")
#   Your weight is: 60
#   Your height is: 1.75
#   system used is metric or imperial? metric
#   Your BMI is: 19.591836734693878

## Basic Scriptiong: 7.4 std lib ======================
#!/usr/bin/env python3.6 
from time import localtime, strftime, mktime
starttime = localtime()
print(f"Timer started at {strftime('%X', starttime)}")
input("Press 'Enter' to stop timer ")
stoptime = localtime()
print(f"Timer stopped at {strftime('%X', starttime)}")
difference = mktime(stoptime) - mktime(starttime)
print(f"Total time: {difference} seconds")
#   Timer started at 10:54:34
#   Press 'Enter' to stop timer
#   Timer stopped at 10:54:34
#   Total time: 7.0 seconds

## Basic Scriptiong: 7.5 env variable ======================
import os 
stage = os.getenv('STAGE', default='dev').upper() # if STAGE is not set, set it to DEV
output = f"We are running in {stage}"
if stage.startswith("PROD"):
    output = f"Danger!!! - {output}"
print(stage) # dev

## Basic Scriptiong: 7.6 files  ======================
# method 1: open > close
io_file = open('io_file.txt', 'r' )
print (io_file)
print(io_file.read())
io_file.seek(0) # Change the stream position to the given offset (0=begining of file). otherwise next f.read()is empty 
print(io_file.read()) # whole content 
io_file.seek(12) # Change the stream position to the given offset(12th) 
print(io_file.read()) # content from 12th and on 

io_file.seek(12) # Change the stream position to the given offset(12th) 
new_io_file = open('new_io_file.txt', 'w')
new_io_file.write(io_file.read()) # content from 12th and on
new_io_file.close()
io_file.close()

# method 2: with open
with open('io_file.txt', 'a') as file1: 
    file1.write('\nNing') # append content

with open('io_file.txt', 'r') as file1:
    with open('new_io_file.txt', 'w') as file2:
        file2.write(file1.read()) # write whole file1 to file2

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


## Useful std lib pkgs 9.1 random / json ======================
# gen_receipts.py > create 100 json files
import random 
import json 
import os 
count = int(os.getenv("FILE_COUNT") or 100)
words = [word.strip() for word in open('/usr/share/dict/words').readlines()]
for identifier in range(count):
    amount = random.uniform(1.0, 1000)
    content = {
        'topic': random.choice(words),
        'value': '%.2f' % amount 
    }
    with open(f'./new/receipt-{identifier}.json', 'w') as f:
        json.dump(content, f) 

## Useful std lib pkgs 9.2 shutil / glob ======================
import os 
try: 
    os.mkdir('./processed')
except OSError:
    print("Dir 'processded'already exist!")
# e.g. ls new/receipt-[0-9]*.json > return all matched names from 0 to 9 > globbing 
import glob, shutil 
receipts = glob.glob('./new/receipt-[0-9]*.json')
subtotal = 0.0 
for path in receipts: 
    with open(path) as f:
        content = json.load(f)
        subtotal += float(content['value'])
    name = path.split("/")[-1] # "./new/receipt-1.json".split("/") >  ['.', 'new', 'receipt-1.json']
    destination = f"./processed/{name}"
    shutil.move(path, destination)  # corresponds to mv ./new/receipt-0.json ./processed/receipt-0.json
    print(f"moved '{path}' to '{destination}' ") # moved './new/receipt-0.json' './processed/receipt-0.json'
print("Receipt subtotal: $%.2f" % subtotal) # Receipt subtotal: $52338.06

## Useful std lib pkgs 9.3 re / math ======================
import re, math 
#  re is more specific than globbing, e.g. find receipt name with event number 
re.match('./new/receipt-[0-9]*[24680].json', './new/receipt-2.json') # retrun True
receipts = [f for f in glob.iglob('./new/receipt-[0-9]*.json') if re.match('./new/receipt-[0-9]*[24680].json', f)]  # find receipt name with event number

# e.g. same example above 
import glob, shutil 
subtotal = 0.0 
for path in glob.iglob('./new/receipt-[0-9]*.json'): 
    with open(path) as f:
        content = json.load(f)
        subtotal += float(content['value'])
    destination = path.replace('new', 'processed')
    shutil.move(path, destination)  # corresponds to mv ./new/receipt-0.json ./processed/receipt-0.json
    print(f"moved '{path}' to '{destination}' ") # moved './new/receipt-0.json' './processed/receipt-0.json'
import math 
print("Receipt subtotal: {math.ceil(subtotal)}") # Receipt subtotal: $ 50972
print("Receipt subtotal: {math.floor(subtotal)}") # Receipt subtotal: $ 50971
print("Receipt subtotal: {round(subtotal, 2)}") # Receipt subtotal: $ 50971.36



## Others changes TBD
# loop through yaml nested data
# disks = ['disk%d' % i for i in range(yaml_file['parent_key']['a_key'])]
# for t_disk in disks 
  