#### Hex2raw

```sh
kan1shka9@shell-web:~$ cd /problems/bee57af2b16368039c96edaa1bd95826
kan1shka9@shell-web:/problems/bee57af2b16368039c96edaa1bd95826$ ls -l
total 20
-r--r----- 1 hacksports hex2raw_5   33 Mar 31  2017 flag
-rwxr-sr-x 1 hacksports hex2raw_5 9656 Mar 31  2017 hex2raw
-r--r----- 1 hacksports hex2raw_5   33 Mar 31  2017 input
kan1shka9@shell-web:/problems/bee57af2b16368039c96edaa1bd95826$ cat flag
cat: flag: Permission denied
kan1shka9@shell-web:/problems/bee57af2b16368039c96edaa1bd95826$ cat input
cat: input: Permission denied
kan1shka9@shell-web:/problems/bee57af2b16368039c96edaa1bd95826$ ./hex2raw
Give me this in raw form (0x41 -> 'A'):
6a5c6fa9602a2d0f439953bcb6f4a611

You gave me:
ABCD
414243440a^C
kan1shka9@shell-web:/problems/bee57af2b16368039c96edaa1bd95826$
```

```sh
kan1shka9@shell-web:/problems/bee57af2b16368039c96edaa1bd95826$ python -c "print '6a5c6fa9602a2d0f439953bcb6f4a611'.decode('hex')" | ./hex2raw
Give me this in raw form (0x41 -> 'A'):
6a5c6fa9602a2d0f439953bcb6f4a611

You gave me:
6a5c6fa9602a2d0f439953bcb6f4a611
Yay! That's what I wanted! Here be the flag:
d2ee728e47348dffdd9b654d3733a40a

kan1shka9@shell-web:/problems/bee57af2b16368039c96edaa1bd95826$
```

Flag &rarr; `d2ee728e47348dffdd9b654d3733a40a`