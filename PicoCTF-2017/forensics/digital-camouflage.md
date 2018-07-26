#### Digital Camouflage

```sh
dev@box:~/Desktop$ strings data.pcap | grep pass
            <td><input type="password" name="pswrd"/></td>
            <td><input type="password" name="pswrd"/></td>
dev@box:~/Desktop$ strings data.pcap | grep pswrd
            <td><input type="password" name="pswrd"/></td>
			document.login.pswrd.value = btoa(document.login.pswrd.value);
            <td><input type="password" name="pswrd"/></td>
			document.login.pswrd.value = btoa(document.login.pswrd.value);
VKuserid=stevensj&pswrd=UjZBS05oV3dvNw%3D%3Dd
dev@box:~/Desktop$ 
```

```sh
dev@box:~/Desktop$ python
Python 2.7.15rc1 (default, Apr 15 2018, 21:51:34) 
[GCC 7.3.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> "3D".decode('hex')
'='
>>> "UjZBS05oV3dvNw==d".decode('base64')
'R6AKNhWwo7'
>>> 
```

Flag &rarr; `R6AKNhWwo7`