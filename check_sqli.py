import re

mysql_log_file = "/var/log/mysql/mysql.log"
pattern_mysql = re.compile("[\'][%]?\w+\'[%]?[\']")

for i, line in enumerate(open(mysql_log_file)):
    for match in re.finditer(pattern_mysql, line):    
        print('Found on line %s: %s' % (i+1, match.group()))

pattern_mysql = re.compile("[\"][%]?\w+\"[%]?[\"]")

for i, line in enumerate(open(mysql_log_file)):
    for match in re.finditer(pattern_mysql, line):    
        print('Found on line %s: %s' % (i+1, match.group()))

