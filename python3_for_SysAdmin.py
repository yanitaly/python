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

## Use Pip and Virtualenv 10.1 install 3pp with PIP ======================
cat<< .config/pip 
[list]
format=columns 
EOF 
$ pip3.6 list 
$ python -m pip install --upgrade pip
$ pip3.6 freeze > requirement.txt
$ pip3.6 uninstall -y -r requirements.txt 
$ pip3.6 install --user -r requirements.txt 

## Use Pip and Virtualenv 10.2 virtualenv ======================
$ mkdir venvs 
$ python3.6 -m venv venvs/experiment # created ./bin/activate
$ source venvs/experiment/bin/activate #   actives venv python, which python > ~/venvs/experiment/bin/python 
$ deactivate  # back to system python

## Use Pip and Virtualenv 10.3 using 3pp in ur scripts ======================
# note PIP INSTALL uses PYPI under the hood
# steps: activate venv > pip install requests > vi ~/bin/weather (using openweathermap.org/OWN_API_KEY)
#!/home/user/venv/experiment/bin/python 
import os 
import requests
import sys 
from argparse import ArgumentParser
parser = ArgumentParser(description="weather api")
parser.add_argument('zip', help='zip code')
parser.add_argument('--country', default='us', help='country')
args = parser.parse_args()
api_key = os.genenv('OWN_API_KEY')
if not api_key:
    print('ERROR: no key provided')
    sys.exit(1)
url = f'http://api....'
res = requests.get(url)

if res.status_code != 200:
    print('ERROR: api get url failed')
    sys.exit(1)
print(res.json()) # returns weather info in json 

## ch11 Planning & project structure  ======================
11.1 exam work and prep work 
# setup database server PostgreDB 
# ssh to db server > download and run setup.sh > install postgre rpm / epel-release >   
# psql postgres://demo:password@<ip>:80/<db name> -c "SELECT count (id) FROM employees;"

11.2 planning through documentation (readme driven development)
mkdir pgbackup 
pip3.6 install --pipenv  # pipenv (Pipfile iso requirements.txt)
pipenv --python $(which python3.6) # creates virtual env and manages dependence, and Pipfile 
curl -o .gitignore  https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore
vi README.rst  # rst format of markdown  
    Pgbackup 
        CLI for backup remote PostgreSQL db eitehr locally or to S3
    Preparing the development 
        1. ensure pip and pipenv installed
        2. clone repo: git clone git@github.com:example/pgbackup 
        3. cd to repo
        4. fetch development dependencies: make install
        5. activate virtualenv: pipenv shell 
    Usage
        pass in a full database URL, stroage driver, destination
        e.g. pgbackup postgres://bob@example.com:/db_one --driver local /var/local/db_one/backups/dump.sql 
    Running tests
        run test locally using: make (if virtualenv is active)
        if virtualenv is not active: pipenv run make 
        
11.3 inital project layout 
mkdir -p src/pgbackup tests 
touch src/pgbackup/__init__.py tests/.keep 
vi setup.py # setuptool 
    from setuptools import setup, find_packages
    with open('README.rst', encoding='UTF-8') as f:
        readme = f.read()
    setup(
        name='pgbackup'
        version=
        description=
        log_description
        author=
        auther_email=
        istall_requires
        packages=find_packages('src'),
        package_dir={'':'src'}
    ) 
pipenv shell 
pip install -e .   # install pgbackup 

vi Makefile # create makefile
        .PHONY: install test 
        default: test
        
        install:
            pipenv install --dev --skip-lock
            
        test:
            PYTHONPATH=./src pytest 
make install 
            
   
## ch12 Implementing Features with Test Driven Development ======================
1. Intro to TDD and first tests
pipenv install --dev pytest # Pipfile 
We’re going to write three tests to start:
    A test that shows that the CLI fails if no driver is specified.
    A test that shows that the CLI fails if there is no destination value given.
    A test that shows, given a driver and a destination, that the CLI’s returned Na
    mespace has the proper values set

import pytest
from pgbackup import cli
url = "postgres://bob:password@example.com:5432/db_one"
def test_parser_without_driver():
     """
     Without a specified driver the parser will exit
     """
     with pytest.raises(SystemExit):
     parser = cli.create_parser()
     parser.parse_args([url])
def test_parser_with_driver():
     """
     The parser will exit if it receives a driver
     without a destination
     """
     parser = cli.create_parser()
     with pytest.raises(SystemExit):
     parser.parse_args([url, "--driver", "local"])
def test_parser_with_driver_and_destination():
     """
     The parser will not exit if it receives a driver
     with a destination
     """
    parser = cli.create_parser()
    args = parser.parse_args([url, "--driver","local","/some/path"])
    assert args.driver == "local"
    assert args.destination == "/some/path"

2. implementing CLI (approach: red > green > refactor )
touch src/pgbackup/cli.py

from argparse import Action, ArgumentParser
known_drivers = ['local', 's3']
class DriverAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        driver, destination = values
        if driver.lower() not in known_drivers:
            parser.error("Unknown driver. Available drivers are'local' & 's3'")
        namespace.driver = driver.lower()
        namespace.destination = destination
    def create_parser():
        parser = ArgumentParser(description="""
        Back up PostgreSQL databases locally or to AWS S3.
        """)
        parser.add_argument("url", help="URL of database to backup")
        parser.add_argument("--driver",help="how & where to store backup",nargs=2,action=DriverAction,required=True)
        return parser
        
Removing Test Duplication Using pytest.fixture
Adding More Tests
Adding Driver Type Validation

test/test_cli.py (partial)
@pytest.fixture
def parser():
    return cli.create_parser()
 
def test_parser_with_unknown_drivers(parser):
     """
     The parser will exit if the driver name is unknown.
     """
     with pytest.raises(SystemExit):
     parser.parse_args([url, "--driver", "azure", "destination"])
def test_parser_with_known_drivers(parser):
     """
     The parser will not exit if the driver name is known.
     """
     for driver in ['local', 's3']:
     assert parser.parse_args([url, "--driver", driver,"destination"])

Final:
import pytest
from pgbackup import cli
url = "postgres://bob@example.com:5432/db_one"
@pytest.fixture
def parser():
    return cli.create_parser()
def test_parser_without_driver(parser):
     """
     Without a specified driver the parser will exit
     """
     with pytest.raises(SystemExit):
        parser.parse_args([url])
def test_parser_with_driver(parser):
     """
     The parser will exit if it receives a driver without a destination
     """
     with pytest.raises(SystemExit):
        parser.parse_args([url, "--driver", "local"])
def test_parser_with_unknown_driver(parser):
     """
     The parser will exit if the driver name is unknown.
     """
     with pytest.raises(SystemExit):
        parser.parse_args([url, "--driver", "azure", "destination"])
def test_parser_with_known_drivers(parser):
     """
     The parser will not exit if the driver name is known.
     """
     for driver in ['local', 's3']:
        assert parser.parse_args([url, "--driver", driver,"destination"])
def test_parser_with_driver_and_destination(parser):
     """
     The parser will not exit if it receives a driver with a destination
     """
     args = parser.parse_args([url, "--driver", "local", "/some/path"])
     assert args.url == url
     assert args.driver == "local"
     assert args.destination == "/some/path"
  
3. Mocking in tests 
note: pg_dump tool exists outside python, so we need mocking 
pipenv install --dev pytest-mock 

tests/test_pgdump.py
import pytest
import subprocess
from pgbackup import pgdump
url = "postgres://bob:password@example.com:5432/db_one"
def test_dump_calls_pg_dump(mocker):
     """
     Utilize pg_dump with the database URL
     """
     mocker.patch('subprocess.Popen')
     assert pgdump.dump(url)
     subprocess.Popen.assert_called_with(['pg_dump', url],stdout=subprocess.PIPE)

4. implementing postgreSQL interaction 

src/pgbackup/pgdump.py
import subprocess
def dump(url):
    return subprocess.Popen(['pg_dump', url],stdout=subprocess.PIPE)
 
def test_dump_handles_oserror(mocker):
     """
     pgdump.dump returns a reasonable error if pg_dump isn't
    installed.
     """
    mocker.patch('subprocess.Popen', side_effect=OSError("no such file"))
    with pytest.raises(SystemExit):
        pgdump.dump(url)
 
 src/pgbackup/pgdump.py
import sys
import subprocess
def dump(url):
     try:
     return subprocess.Popen(['pg_dump', url],stdout=subprocess.PIPE)
     except OSError as err:
     print(f"Error: {err}")
     sys.exit(1)
     
 5. implementing Local File Storage 

 _tests/test_storage.py_
 import tempfile
from pgbackup import storage
def test_storing_file_locally():
     """
     Writes content from one file-like to another
     """
     infile = tempfile.TemporaryFile('r+b')
     infile.write(b"Testing")
     infile.seek(0)
     outfile = tempfile.NamedTemporaryFile(delete=False)
     storage.local(infile, outfile)
     with open(outfile.name, 'rb') as f:
        assert f.read() == b"Testing"

src/pgbackup/storage.py
def local(infile, outfile):
     outfile.write(infile.read())
     outfile.close()
     infile.close()
 
  6. implementing aws interaction 
$ pipenv install boto3
$ exit
$ mkdir ~/.aws
$ pip3.6 install --user awscli
$ aws configure
$ exec $SHELL
 pipenv shell

tests/test_storage.py (partial)
def test_storing_file_on_s3(mocker, infile):
     """
     Writes content from one readable to S3
     """
     client = mocker.Mock()
     storage.s3(client, infile, "bucket", "file-name")
     client.upload_fileobj.assert_called_with( infile,"bucket", "file-name")
     
src/pgbackup/storage.py (partial)
def s3(client, infile, bucket, name):
    client.upload_fileobj(infile, bucket, name)
 
 ## ch13 Integrating Features and Distributing the Project =====================
 1. Add “console_script” to project 
 setup.py (partial)
 install_requires=['boto3'],
 entry_points={
     'console_scripts': [
     'pgbackup=pgbackup.cli:main',
     ],
 }
 
 src/pgbackup/cli.py
 def main():
     import boto3
     from pgbackup import pgdump, storage
     args = create_parser().parse_args()
     dump = pgdump.dump(args.url)
     if args.driver == 's3':
         client = boto3.client('s3')
         # TODO: create a better name based on the database name and the date
         storage.s3(client, dump.stdout, args.destination,'example.sql')
     else:
         outfile = open(args.destination, 'wb')
         storage.local(dump.stdout, outfile)
         
 2. Building and Sharing a Wheel Distribution
 setup.cfg
    [bdist_wheel]
    python-tag = py36
  $ python setup.py bdist_wheel  # > build our wheel 
  $ pip uninstall pgbackup
  $ pip install dist/pgbackup-0.1.0-py36-noneany.whl

FILE END ==================
