#### 4. Tcpv4connect: Log Analysis

----

- Performance monitoring and tracking tools can provide a wealth of information about a running system. In some cases, they can help identify anomalies which could have been caused by a security incident.

----

- In this lab, we are given [`Tcpv4connect script's`](https://github.com/iovisor/bcc/blob/master/examples/tracing/tcpv4connect.py) trace logs of a server. We have to unearth suspicious activity by analyzing these logs. 

----

Please start the lab, analyze these logs to answer the questions given below and submit the flags to verify:

- Identify the port on which telnet is running on the server.

```sh
root@attackdefense:~# grep telnet logs
25955  telnet       127.0.0.1        127.0.0.1        336
25961  telnet       192.168.161.139  192.168.241.111  35608
28702  telnet       127.0.0.1        127.0.0.1        336
28722  telnet       127.0.0.1        127.0.0.1        336
28953  telnet       192.168.161.139  192.168.241.111  35610
28953  telnet       192.168.161.139  192.168.241.111  35716
root@attackdefense:~#
```

```
336
```

- What the IP address of the remote machine which connected to the server using telnet?

```sh
# grep telnet logs
192.168.241.111
```

- The server has downloaded data files over HTTP using a different network interface. What is the IP address of that interface?

```sh
root@attackdefense:~# grep http logs
25985  http         10.10.13.139     192.168.91.26     80
27143  http         10.10.13.139     192.168.91.26     80
27588  http         10.10.13.139     192.168.91.26     80
root@attackdefense:~#
```

```sh
root@attackdefense:~# grep 80 logs
25523  Socket Threa 192.168.161.139  172.217.167.163  80
25523  Socket Threa 192.168.161.139  172.217.167.163  80
25523  Socket Threa 192.168.161.139  117.18.237.29    80
25523  Socket Threa 192.168.161.139  117.18.237.29    80
25523  Socket Threa 192.168.161.139  117.18.237.29    80
25523  Socket Threa 192.168.161.139  172.217.167.163  80
25523  Socket Threa 192.168.161.139  172.217.167.163  80
25523  Socket Threa 192.168.161.139  172.217.167.163  80
25523  Socket Threa 192.168.161.139  151.139.128.14   80
25523  Socket Threa 192.168.161.139  151.139.128.14   80
25523  Socket Threa 192.168.161.139  35.196.248.27    80
25523  Socket Threa 192.168.161.139  35.196.248.27    80
25523  Socket Threa 192.168.161.139  151.139.128.14   80
25523  Socket Threa 192.168.161.139  151.139.128.14   80
25523  Socket Threa 192.168.161.139  13.35.190.225    80
25523  Socket Threa 192.168.161.139  13.35.190.225    80
25985  http         10.10.13.139     192.168.91.26     80
27143  http         10.10.13.139     192.168.91.26     80
27588  http         10.10.13.139     192.168.91.26     80
25523  Socket Threa 192.168.161.139  151.139.128.14   80
25523  Socket Threa 192.168.161.139  151.139.128.14   80
25523  Socket Threa 192.168.161.139  117.18.237.29    80
25523  Socket Threa 192.168.161.139  117.18.237.29    80
25523  Socket Threa 192.168.161.139  117.18.237.29    80
25523  Socket Threa 192.168.161.139  151.139.128.14   80
root@attackdefense:~#
```

```
10.10.13.139 
```

- What is the IP address of the remote machine from which the packages were downloaded?

```sh
# grep http logs
192.168.91.26
```

----

###### References

- [`Tcpv4connect script`](https://github.com/iovisor/bcc/blob/master/examples/tracing/tcpv4connect.py)
- [`Tcpv4connect Examples`](https://github.com/iovisor/bcc/blob/master/examples/tracing/tcpv4connect_example.txt)
- [`BCC Tools`](https://github.com/iovisor/bcc)

----

EOF