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


## Intermediate Scriptiong: 8.1 parsing cmd  ======================



## Others changes TBD
# loop through yaml nested data
# disks = ['disk%d' % i for i in range(yaml_file['parent_key']['a_key'])]
# for t_disk in disks 
  