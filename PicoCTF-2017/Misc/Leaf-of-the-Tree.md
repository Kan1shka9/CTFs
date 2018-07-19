#### Leaf of the Tree

```sh
shell-web login: kan1shka9                                         
Enter your password:                                               
kan1shka9@shell-web:~$ pwd                                         
/home/kan1shka9                                                    
kan1shka9@shell-web:~$ cd /problems/                 
kan1shka9@shell-web:/problems$ cd 10f7c1d3e9fa2d4fc95555530ea97ec5 
kan1shka9@shell-web:/problems/10f7c1d3e9fa2d4fc95555530ea97ec5$ ls -lah
total 48K                                                          
drwxr-xr-x   3 root root 4.0K Mar 31  2017 .
drwxr-x--x 573 root root  36K Apr 16  2017 ..
drwxr-xr-x   3 root root 4.0K Mar 31  2017 trunk
kan1shka9@shell-web:/problems/10f7c1d3e9fa2d4fc95555530ea97ec5$
kan1shka9@shell-web:/problems/10f7c1d3e9fa2d4fc95555530ea97ec5$ cd 
trunk/
kan1shka9@shell-web:/problems/10f7c1d3e9fa2d4fc95555530ea97ec5/trunk$ ls -lah                                                         
total 12K                                                          
drwxr-xr-x 3 root root 4.0K Mar 31  2017 .
drwxr-xr-x 3 root root 4.0K Mar 31  2017 ..
drwxr-xr-x 3 root root 4.0K Mar 31  2017 trunkd091
kan1shka9@shell-web:/problems/10f7c1d3e9fa2d4fc95555530ea97ec5/trunk$ cd trunkd091/                                                   
kan1shka9@shell-web:/problems/10f7c1d3e9fa2d4fc95555530ea97ec5/trunk/trunkd091$ ls -lah                                               
total 12K                                                          
drwxr-xr-x 3 root root 4.0K Mar 31  2017 .
drwxr-xr-x 3 root root 4.0K Mar 31  2017 ..
drwxr-xr-x 4 root root 4.0K Mar 31  2017 trunkbf10
kan1shka9@shell-web:/problems/10f7c1d3e9fa2d4fc95555530ea97ec5/trunk/trunkd091$   
```

```sh
kan1shka9@shell-web:/problems/10f7c1d3e9fa2d4fc95555530ea97ec5/trunk/trunkd091/trunkbf10/trunk4b0b/trunkb4d6/trunk5ba3/trunkd86e/trunka326$ cat flag                                                     
88636e09e72bafb444e7f6a8105dbc5ds
kan1shka9@shell-web:/problems/10f7c1d3e9fa2d4fc95555530ea97ec5/trunk/trunkd091/trunkbf10/trunk4b0b/trunkb4d6/trunk5ba3/trunkd86e/trunka326$ 
```

```sh
kan1shka9@shell-web:/problems/10f7c1d3e9fa2d4fc95555530ea97ec5$ find . -name flag                                                     
./trunk/trunkd091/trunkbf10/trunk4b0b/trunkb4d6/trunk5ba3/trunkd86e/trunka326/flag                                                    
kan1shka9@shell-web:/problems/10f7c1d3e9fa2d4fc95555530ea97ec5$    
```

Flag &rarr; `88636e09e72bafb444e7f6a8105dbc5ds`