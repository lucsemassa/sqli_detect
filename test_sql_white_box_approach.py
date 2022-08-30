#find ATutor -type f -name "*.php" > /tmp/all_php_files.txt
#or
#grep -rwl ATutor -e "^.*user_location.*public.*" > /tmp/all_php_files.txt
import re
import os
import requests
import time
from colorama import Fore, Back, Style 
requests.packages.urllib3.\
disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def format_text(title,item):

    cr = '\r\n'

    section_break = cr + "*" * 20 + cr

    item = str(item)

    text = Style.BRIGHT + Fore.RED + title + Fore.RESET + section_break + item + section_break 
    return text


file1 = open('/tmp/all_php_files.txt', 'r')
Lines = file1.readlines()

public_files = []  

for line in Lines:
	public_files.append(line.strip())


pattern = re.compile("\$_(GET|POST|REQUEST|get|post|request)\[[\'\"](\w+)[\'\"]\]")

base_url = "http://192.168.10.134/ATutor/"
proxies = {"http" : "http://127.0.0.1:8080"}
user_agent = {'User-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}
s = requests.Session()


for current_file in public_files:
    get_var = {}
    post_var = {}

    get_var2 = {}
    post_var2 = {}

    print(current_file)
    complement=current_file.split("/")[len(current_file.split("/"))-1].split(".")[0]
    
    for i, line in enumerate(open(os.getcwd()+'/'+current_file)):
        for match in re.finditer(pattern, line):
            parameter_method = match.group(1)
            parameter_var = match.group(2)
            #print("hello " + current_file.split("/")[len(current_file.split("/"))-1].split(".")[0])
            #input()

            if (parameter_method.upper() == 'GET'):
                if not (parameter_var in get_var.keys()):
                    get_var.update({parameter_var:parameter_var+"_"+complement+"'"})
                    get_var2.update({parameter_var:parameter_var+'_'+complement+'"'})

            elif (parameter_method.upper() == 'POST' or parameter_method.upper() == 'REQUEST' ):
               if not (parameter_var in post_var.keys()):
                    post_var.update({parameter_var:parameter_var+"_"+complement+"'"})
                    post_var2.update({parameter_var:parameter_var+'_'+complement+'"'})

            
            print('Found on line %s: method: %s variable: %s' % (i+1, parameter_method, parameter_var))




    print("post var is ")
    print(post_var)

    r = s.post(base_url+current_file, params=post_var,  proxies=proxies)
    r = s.post(base_url+current_file, params=post_var2, proxies=proxies)


    print(format_text('r.status_code is: ',r.status_code))


    print("get var is ")
    print(get_var)

    r = s.get(base_url+current_file, params=get_var, proxies=proxies)
    r = s.get(base_url+current_file, params=get_var2,  proxies=proxies)


