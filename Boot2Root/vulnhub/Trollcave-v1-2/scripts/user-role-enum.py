import requests
import re

def GetUserByID(id):
	response = (requests.get('http://192.168.1.30/users/' + str(id)).text).strip()
	# Match <a href="/send_pm?recipient_name=King">PM</a>
	username = re.search('recipient_name=(.*?)"', response).group(1)
	return username

def GetRoleByID(id):
	response = (requests.get('http://192.168.1.30/users/' + str(id)).text).strip()
	"""
	<div class='user-info'>
	<b>
	Superadmin
	</b>
	"""
	role = re.search('>\x0A<b>\x0A(.*?)\x0A</b>', response).group(1)
	return role

for i in range(0,20):
	try:
            print(str(i) + " : " + GetUserByID(i) + " : " + GetRoleByID(i))
	except:
		None
