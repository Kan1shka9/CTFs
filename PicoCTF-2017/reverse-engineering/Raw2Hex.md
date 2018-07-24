#### Raw2Hex

```sh
kan1shka9@shell-web:~$ cd /problems/854399173cf870506ff3a4397adfefc1
kan1shka9@shell-web:/problems/854399173cf870506ff3a4397adfefc1$ ls -l
total 12
-r--r----- 1 hacksports raw2hex_7   33 Mar 31  2017 flag
-rwxr-sr-x 1 hacksports raw2hex_7 7848 Mar 31  2017 raw2hex
kan1shka9@shell-web:/problems/854399173cf870506ff3a4397adfefc1$ ./raw2hex
The flag is::�ϱ��,=B�2�{kan1shka9@shell-web:/problems/854399173cf870506ff3a4397adfefc1$
kan1shka9@shell-web:/problems/854399173cf870506ff3a4397adfefc1$
```

```sh
kan1shka9@shell-web:/problems/854399173cf870506ff3a4397adfefc1$ ./raw2hex | xxd
0000000: 5468 6520 666c 6167 2069 733a 0e3a b3cf  The flag is:.:..
0000010: b1a7 db2c 3d18 4285 32c9 7b05            ...,=.B.2.{.
kan1shka9@shell-web:/problems/854399173cf870506ff3a4397adfefc1$
```

Flag &rarr; `71c28db77578a80e38aae0d626d853a5`