#### Bandit

----

- [`Link`](https://overthewire.org/wargames/bandit/)

----

###### Level 0

```sh
ctf@ctf-vm:~$ ssh bandit0@bandit.labs.overthewire.org -p 2220
bandit0@bandit.labs.overthewire.org's password: bandit0
bandit0@bandit:~$ 
```

----

###### Level 0 → Level 1

```sh
bandit0@bandit:~$ ls -l
total 4
-rw-r----- 1 bandit1 bandit0 33 Oct 16  2018 readme
andit0@bandit:~$ 
```

```sh
bandit0@bandit:~$ cat readme 
boJ9jbbUNNfktd78OOpsqOltutMc3MY1
bandit0@bandit:~$ 
```

----

###### Level 1 → Level 2

```sh
ctf@ctf-vm:~$ ssh bandit1@bandit.labs.overthewire.org -p 2220
bandit1@bandit.labs.overthewire.org's password: boJ9jbbUNNfktd78OOpsqOltutMc3MY1
bandit1@bandit:~$
```

```sh
bandit1@bandit:~$ ls -l
total 4
-rw-r----- 1 bandit2 bandit1 33 Oct 16  2018 -
bandit1@bandit:~$
```

```sh
bandit1@bandit:~$ cat ./-
CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9
bandit1@bandit:~$ 
```

```sh
bandit1@bandit:~$ cat <-
CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9
bandit1@bandit:~$
```

- [dashed filename](https://www.google.com/search?q=dashed+filenames)

----

###### Level 2 → Level 3

```sh
ctf@ctf-vm:~$ ssh bandit2@bandit.labs.overthewire.org -p 2220
bandit2@bandit.labs.overthewire.org's password: CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9
bandit2@bandit:~$ 
```

```sh
bandit2@bandit:~$ ls -l
total 4
-rw-r----- 1 bandit3 bandit2 33 Oct 16  2018 spaces in this filename
bandit2@bandit:~$ 
```

```sh
bandit2@bandit:~$ cat spaces\ in\ this\ filename 
UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK
bandit2@bandit:~$ 
```

```sh
bandit2@bandit:~$ cat "spaces in this filename" 
UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK
bandit2@bandit:~$ 
```

- [spaces in filename](https://www.google.com/search?q=spaces+in+filename)

----

###### Level 3 → Level 4

```sh
ctf@ctf-vm:~$ ssh bandit3@bandit.labs.overthewire.org -p 2220
bandit3@bandit.labs.overthewire.org's password: UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK
```

```sh
bandit3@bandit:~$ ls -l
total 4
drwxr-xr-x 2 root root 4096 Oct 16  2018 inhere
bandit3@bandit:~$ 
```

```sh
bandit3@bandit:~$ cd inhere/
bandit3@bandit:~/inhere$ 
```

```sh
bandit3@bandit:~/inhere$ ls -l
total 0
bandit3@bandit:~/inhere$ 
```

```sh
bandit3@bandit:~/inhere$ ls -lah
total 12K
drwxr-xr-x 2 root    root    4.0K Oct 16  2018 .
drwxr-xr-x 3 root    root    4.0K Oct 16  2018 ..
-rw-r----- 1 bandit4 bandit3   33 Oct 16  2018 .hidden
bandit3@bandit:~/inhere$ 
```

```sh
bandit3@bandit:~/inhere$ cat .hidden 
pIwrPrtPN36QITSp3EQaw936yaFoFgAB
bandit3@bandit:~/inhere$ 
```

----

###### Level 4 → Level 5

```sh
ctf@ctf-vm:~$ ssh bandit4@bandit.labs.overthewire.org -p 2220
bandit4@bandit.labs.overthewire.org's password: pIwrPrtPN36QITSp3EQaw936yaFoFgAB
bandit4@bandit:~$ 
```

```sh
bandit4@bandit:~$ ls -l
total 4
drwxr-xr-x 2 root root 4096 Oct 16  2018 inhere
bandit4@bandit:~$ 
```

```sh
bandit4@bandit:~$ cd inhere/
bandit4@bandit:~/inhere$ 
```

```sh
bandit4@bandit:~/inhere$ ls -l
total 40
-rw-r----- 1 bandit5 bandit4 33 Oct 16  2018 -file00
-rw-r----- 1 bandit5 bandit4 33 Oct 16  2018 -file01
-rw-r----- 1 bandit5 bandit4 33 Oct 16  2018 -file02
-rw-r----- 1 bandit5 bandit4 33 Oct 16  2018 -file03
-rw-r----- 1 bandit5 bandit4 33 Oct 16  2018 -file04
-rw-r----- 1 bandit5 bandit4 33 Oct 16  2018 -file05
-rw-r----- 1 bandit5 bandit4 33 Oct 16  2018 -file06
-rw-r----- 1 bandit5 bandit4 33 Oct 16  2018 -file07
-rw-r----- 1 bandit5 bandit4 33 Oct 16  2018 -file08
-rw-r----- 1 bandit5 bandit4 33 Oct 16  2018 -file09
bandit4@bandit:~/inhere$ 
```

```sh
bandit4@bandit:~/inhere$ file ./-file* 
./-file00: data
./-file01: data
./-file02: data
./-file03: data
./-file04: data
./-file05: data
./-file06: data
./-file07: ASCII text
./-file08: data
./-file09: data
bandit4@bandit:~/inhere$ 
```

```sh
bandit4@bandit:~/inhere$ cat ./-file07 
koReBOKuIDDepwhWk7jZC0RTdopnAYKh
bandit4@bandit:~/inhere$ 
```

----

###### Level 5 → Level 6

```sh
ctf@ctf-vm:~$ ssh bandit5@bandit.labs.overthewire.org -p 2220
bandit5@bandit.labs.overthewire.org's password: koReBOKuIDDepwhWk7jZC0RTdopnAYKh
```

```sh
bandit5@bandit:~$ ls -l
total 4
drwxr-x--- 22 root bandit5 4096 Oct 16  2018 inhere
bandit5@bandit:~$ 
```

```sh
bandit5@bandit:~$ cd inhere/
bandit5@bandit:~/inhere$ 
```

```sh
bandit5@bandit:~/inhere$ ls -l
total 80
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere00
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere01
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere02
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere03
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere04
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere05
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere06
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere07
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere08
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere09
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere10
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere11
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere12
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere13
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere14
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere15
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere16
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere17
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere18
drwxr-x--- 2 root bandit5 4096 Oct 16  2018 maybehere19
bandit5@bandit:~/inhere$ 
```

```sh
bandit5@bandit:~/inhere$ ls -lah *
maybehere00:
total 72K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 1.1K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5  551 Oct 16  2018 .file1
-rw-r-----  1 root bandit5 9.2K Oct 16  2018 -file2
-rw-r-----  1 root bandit5 7.7K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 7.3K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 4.7K Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 6.0K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 6.7K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 1.9K Oct 16  2018 spaces file3

maybehere01:
total 80K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 5.9K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 8.8K Oct 16  2018 .file1
-rw-r-----  1 root bandit5  288 Oct 16  2018 -file2
-rw-r-----  1 root bandit5 3.0K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 9.5K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 3.8K Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 4.1K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 4.5K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 8.7K Oct 16  2018 spaces file3

maybehere02:
total 68K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 3.8K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 6.3K Oct 16  2018 .file1
-rw-r-----  1 root bandit5 3.5K Oct 16  2018 -file2
-rw-r-----  1 root bandit5 2.6K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 4.9K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 7.8K Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 6.6K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 8.3K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 2.3K Oct 16  2018 spaces file3

maybehere03:
total 80K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5  315 Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 9.6K Oct 16  2018 .file1
-rw-r-----  1 root bandit5 6.5K Oct 16  2018 -file2
-rw-r-----  1 root bandit5 8.7K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 8.1K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 2.3K Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 2.2K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 3.4K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 9.1K Oct 16  2018 spaces file3

maybehere04:
total 60K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 4.4K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 2.4K Oct 16  2018 .file1
-rw-r-----  1 root bandit5 2.6K Oct 16  2018 -file2
-rw-r-----  1 root bandit5 6.0K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 2.1K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5  142 Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 5.5K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 2.5K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 5.9K Oct 16  2018 spaces file3

maybehere05:
total 64K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 2.3K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 3.2K Oct 16  2018 .file1
-rw-r-----  1 root bandit5 5.9K Oct 16  2018 -file2
-rw-r-----  1 root bandit5 5.8K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 2.6K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 4.5K Oct 16  2018 .file3
-rwxr-x---  1 root bandit5  880 Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 2.4K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 8.4K Oct 16  2018 spaces file3

maybehere06:
total 64K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 5.6K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 1.3K Oct 16  2018 .file1
-rw-r-----  1 root bandit5 1.1K Oct 16  2018 -file2
-rw-r-----  1 root bandit5 8.8K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 3.4K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 2.4K Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 4.0K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 4.2K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 7.9K Oct 16  2018 spaces file3

maybehere07:
total 56K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 3.6K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 3.0K Oct 16  2018 .file1
-rw-r-----  1 root bandit5 2.5K Oct 16  2018 -file2
-rw-r-----  1 root bandit5 1.1K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 3.3K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 2.0K Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 4.1K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 8.9K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 1022 Oct 16  2018 spaces file3

maybehere08:
total 56K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 1.1K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 8.0K Oct 16  2018 .file1
-rw-r-----  1 root bandit5 3.8K Oct 16  2018 -file2
-rw-r-----  1 root bandit5  747 Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 2.6K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 2.2K Oct 16  2018 .file3
-rwxr-x---  1 root bandit5  215 Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 3.7K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 9.0K Oct 16  2018 spaces file3

maybehere09:
total 76K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 3.6K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 6.7K Oct 16  2018 .file1
-rw-r-----  1 root bandit5  774 Oct 16  2018 -file2
-rw-r-----  1 root bandit5 8.4K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 7.8K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 3.8K Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 5.2K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 8.6K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 7.4K Oct 16  2018 spaces file3

maybehere10:
total 56K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 1.1K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 7.0K Oct 16  2018 .file1
-rw-r-----  1 root bandit5 2.0K Oct 16  2018 -file2
-rw-r-----  1 root bandit5   99 Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 1.3K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 2.9K Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 8.1K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 3.5K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 2.2K Oct 16  2018 spaces file3

maybehere11:
total 72K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 1.2K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5  452 Oct 16  2018 .file1
-rw-r-----  1 root bandit5 4.5K Oct 16  2018 -file2
-rw-r-----  1 root bandit5 2.5K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 8.7K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 8.1K Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 3.1K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5  503 Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 8.7K Oct 16  2018 spaces file3

maybehere12:
total 72K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 9.5K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 5.7K Oct 16  2018 .file1
-rw-r-----  1 root bandit5  251 Oct 16  2018 -file2
-rw-r-----  1 root bandit5 8.1K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 8.9K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 1022 Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 2.2K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 2.5K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 1.7K Oct 16  2018 spaces file3

maybehere13:
total 64K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 1.4K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 5.2K Oct 16  2018 .file1
-rw-r-----  1 root bandit5 1.4K Oct 16  2018 -file2
-rw-r-----  1 root bandit5 8.8K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 3.0K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 6.9K Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 3.9K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5  952 Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 4.3K Oct 16  2018 spaces file3

maybehere14:
total 60K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 4.2K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 3.4K Oct 16  2018 .file1
-rw-r-----  1 root bandit5 8.2K Oct 16  2018 -file2
-rw-r-----  1 root bandit5 1.5K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 3.7K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 4.8K Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 1.4K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5  871 Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5  376 Oct 16  2018 spaces file3

maybehere15:
total 64K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 8.6K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 2.2K Oct 16  2018 .file1
-rw-r-----  1 root bandit5 9.3K Oct 16  2018 -file2
-rw-r-----  1 root bandit5  279 Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 6.2K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5  742 Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 1.6K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5   51 Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 1.6K Oct 16  2018 spaces file3

maybehere16:
total 80K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 4.2K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 5.3K Oct 16  2018 .file1
-rw-r-----  1 root bandit5 5.2K Oct 16  2018 -file2
-rw-r-----  1 root bandit5 8.3K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 7.9K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 1.2K Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 9.6K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 3.1K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 7.4K Oct 16  2018 spaces file3

maybehere17:
total 72K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 1.2K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5  895 Oct 16  2018 .file1
-rw-r-----  1 root bandit5 1.8K Oct 16  2018 -file2
-rw-r-----  1 root bandit5 8.2K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 4.4K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5 5.0K Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 8.2K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 3.4K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 6.3K Oct 16  2018 spaces file3

maybehere18:
total 68K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 9.5K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 5.6K Oct 16  2018 .file1
-rw-r-----  1 root bandit5   77 Oct 16  2018 -file2
-rw-r-----  1 root bandit5 2.1K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 2.3K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5  154 Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 7.2K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 6.2K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 6.9K Oct 16  2018 spaces file3

maybehere19:
total 76K
drwxr-x---  2 root bandit5 4.0K Oct 16  2018 .
drwxr-x--- 22 root bandit5 4.0K Oct 16  2018 ..
-rwxr-x---  1 root bandit5 6.2K Oct 16  2018 -file1
-rwxr-x---  1 root bandit5 7.1K Oct 16  2018 .file1
-rw-r-----  1 root bandit5 5.5K Oct 16  2018 -file2
-rw-r-----  1 root bandit5 4.7K Oct 16  2018 .file2
-rwxr-x---  1 root bandit5 7.8K Oct 16  2018 -file3
-rwxr-x---  1 root bandit5  494 Oct 16  2018 .file3
-rwxr-x---  1 root bandit5 7.1K Oct 16  2018 spaces file1
-rw-r-----  1 root bandit5 8.6K Oct 16  2018 spaces file2
-rwxr-x---  1 root bandit5 2.3K Oct 16  2018 spaces file3
bandit5@bandit:~/inhere$ 
```

```sh
bandit5@bandit:~/inhere$ find . -type f -size 1033c ! -executable -exec file {} + | grep ASCII
./maybehere07/.file2: ASCII text, with very long lines
bandit5@bandit:~/inhere$ 
```

```sh
bandit5@bandit:~/inhere$ cat ./maybehere07/.file2
DXjZPULLxYr17uwoI01bNLQbtFemEgo7
bandit5@bandit:~/inhere$ 
```

- [Find human-readable files](https://unix.stackexchange.com/questions/313442/find-human-readable-files)

----

###### Level 6 → Level 7

```sh
ctf@ctf-vm:~$ ssh bandit6@bandit.labs.overthewire.org -p 2220
bandit6@bandit.labs.overthewire.org's password: DXjZPULLxYr17uwoI01bNLQbtFemEgo7
bandit6@bandit:~$ 
```

```sh
bandit6@bandit:~$ find / -user bandit7 -group bandit6 -size 33c 2>/dev/null
/var/lib/dpkg/info/bandit7.password
bandit6@bandit:~$ 
```

```sh
bandit6@bandit:~$ cat /var/lib/dpkg/info/bandit7.password
HKBPTKQnIay4Fw76bEy8PVxKEDQRKTzs
bandit6@bandit:~$ 
```

----

###### Level 7 → Level 8

```sh
ctf@ctf-vm:~$ ssh bandit7@bandit.labs.overthewire.org -p 2220
bandit7@bandit.labs.overthewire.org's password: HKBPTKQnIay4Fw76bEy8PVxKEDQRKTzs
bandit7@bandit:~$ 
```

```sh
bandit7@bandit:~$ ls -l
total 4088
-rw-r----- 1 bandit8 bandit7 4184396 Oct 16  2018 data.txt
bandit7@bandit:~$ 
```

```sh
bandit7@bandit:~$ head data.txt 
humiliation's	47r0YuNylaQ3k6HqGF5NsPPiGuolDCjn
malarkey's	0huyJeRwvtJaoyRmJjQFsRnQcYG4gDir
prioress	ocudTlq9CbpCw9aByrqGffAuoYvCmLNV
enlivened	a7zT1gFekL2pB54py3NmJkYluxdAscwO
bony	r5GbTRzr0dsAMEuiBO8sznt0v56nci5z
transatlantic	ttoxcePeynPXWS1fnQTBWtij9uQwbBfJ
earliness	ikmPFX39MF1mrIfRvTMIFnBGyZV3T2Fa
rump's	nFY7k2ua3xfV5oScoBQsPhrwKjeKVwam
rink's	vzsUxoBeDiy7wo7SW1CnXZUYEOIUuoiw
sierras	fUB5nuau8pLD55Wi4u6R8x4SDxqBUXfd
bandit7@bandit:~$ 
```

```sh
bandit7@bandit:~$ cat -n data.txt | grep millionth
 96950	millionth	cvX2JJa4CFALtqS87jk27qwqGhBM9plV
bandit7@bandit:~$ 
```

----

###### Level 8 → Level 9

```sh
ctf@ctf-vm:~$ ssh bandit8@bandit.labs.overthewire.org -p 2220
bandit8@bandit.labs.overthewire.org's password: cvX2JJa4CFALtqS87jk27qwqGhBM9plV
bandit8@bandit:~$ 
```

```sh
bandit8@bandit:~$ ls -l
total 36
-rw-r----- 1 bandit9 bandit8 33033 Oct 16  2018 data.txt
bandit8@bandit:~$ 
```

```sh
bandit8@bandit:~$ cat data.txt | sort | uniq -u
UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR
bandit8@bandit:~$ 
```

- [Bash : grep unique lines](https://stackoverflow.com/questions/27598133/bash-grep-unique-lines)

----

###### Level 9 → Level 10

```sh
ctf@ctf-vm:~$ ssh bandit9@bandit.labs.overthewire.org -p 2220
bandit9@bandit.labs.overthewire.org's password: UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR
bandit9@bandit:~$ 
```

```sh
bandit9@bandit:~$ ls -l
total 20
-rw-r----- 1 bandit10 bandit9 19379 Oct 16  2018 data.txt
bandit9@bandit:~$ 
```

```sh
bandit9@bandit:~$ strings data.txt | grep ======
2========== the
========== password
========== isa
========== truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk
bandit9@bandit:~$ 
```

----

###### Level 10 → Level 11

```sh
ctf@ctf-vm:~$ ssh bandit10@bandit.labs.overthewire.org -p 2220
bandit10@bandit.labs.overthewire.org's password: truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk
bandit10@bandit:~$ 
```

```sh
bandit10@bandit:~$ ls -l
total 4
-rw-r----- 1 bandit11 bandit10 69 Oct 16  2018 data.txt
bandit10@bandit:~$ 
```

```sh
bandit10@bandit:~$ cat data.txt 
VGhlIHBhc3N3b3JkIGlzIElGdWt3S0dzRlc4TU9xM0lSRnFyeEUxaHhUTkViVVBSCg==
bandit10@bandit:~$ 
```

```sh
bandit10@bandit:~$ cat data.txt | base64 -d
The password is IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR
bandit10@bandit:~$ 
```

----

###### Level 11 → Level 12

```sh
ctf@ctf-vm:~$ ssh bandit11@bandit.labs.overthewire.org -p 2220
bandit11@bandit.labs.overthewire.org's password: IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR
bandit11@bandit:~$ 
```

```sh
bandit11@bandit:~$ ls -l 
total 4
-rw-r----- 1 bandit12 bandit11 49 Oct 16  2018 data.txt
bandit11@bandit:~$ 
```

```sh
bandit11@bandit:~$ cat data.txt 
Gur cnffjbeq vf 5Gr8L4qetPEsPk8htqjhRK8XSP6x2RHh
bandit11@bandit:~$ 
```

```sh
bandit11@bandit:~$ cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
The password is 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu
bandit11@bandit:~$ 
```

----

###### Level 12 → Level 13

```sh
tf@ctf-vm:~$ ssh bandit12@bandit.labs.overthewire.org -p 2220
bandit12@bandit.labs.overthewire.org's password: 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu
bandit12@bandit:~$ 
```

```sh
bandit12@bandit:~$ ls -l
total 4
-rw-r----- 1 bandit13 bandit12 2581 Oct 16  2018 data.txt
bandit12@bandit:~$ 
```

```sh
bandit12@bandit:~$ cat data.txt 
00000000: 1f8b 0808 d7d2 c55b 0203 6461 7461 322e  .......[..data2.
00000010: 6269 6e00 013c 02c3 fd42 5a68 3931 4159  bin..<...BZh91AY
00000020: 2653 591d aae5 9800 001b ffff de7f 7fff  &SY.............
00000030: bfb7 dfcf 9fff febf f5ad efbf bbdf 7fdb  ................
00000040: f2fd ffdf effa 7fff fbd7 bdff b001 398c  ..............9.
00000050: 1006 8000 0000 0d06 9900 0000 6834 000d  ............h4..
00000060: 01a1 a000 007a 8000 0d00 0006 9a00 d034  .....z.........4
00000070: 0d1a 3234 68d1 e536 a6d4 4000 341a 6200  ..24h..6..@.4.b.
00000080: 0069 a000 0000 0000 d003 d200 681a 0d00  .i..........h...
00000090: 0001 b51a 1a0c 201e a000 6d46 8068 069a  ...... ...mF.h..
000000a0: 6834 340c a7a8 3406 4000 0680 0001 ea06  h44...4.@.......
000000b0: 8190 03f5 4032 1a00 0343 4068 0000 0686  ....@2...C@h....
000000c0: 8000 0320 00d0 0d00 0610 0014 1844 0308  ... .........D..
000000d0: 04e1 c542 9ab8 2c30 f1be 0b93 763b fb13  ...B..,0....v;..
000000e0: 50c4 c101 e008 3b7a 92a7 9eba 8a73 8d21  P.....;z.....s.!
000000f0: 9219 9c17 052b fb66 a2c2 fccc 9719 b330  .....+.f.......0
00000100: 6068 8c65 e504 5ec0 ae02 fa6d 16bc 904b  `h.e..^....m...K
00000110: ba6c f692 356e c02b 0374 c394 6859 f5bb  .l..5n.+.t..hY..
00000120: 0f9f 528e 4272 22bb 103c 2848 d8aa 2409  ..R.Br"..<(H..$.
00000130: 24d0 d4c8 4b42 7388 ce25 6c1a 7ec1 5f17  $...KBs..%l.~._.
00000140: cc18 ddbf edc1 e3a4 67f1 7a4d 8277 c823  ........g.zM.w.#
00000150: 0450 2232 40e0 07f1 ca16 c6d6 ef0d ecc9  .P"2@...........
00000160: 8bc0 5e2d 4b12 8586 088e 8ca0 e67d a55c  ..^-K........}.\
00000170: 2ca0 18c7 bfb7 7d45 9346 ea5f 2172 01e4  ,.....}E.F._!r..
00000180: 5598 673f 45af 69b7 a739 7814 8706 04ed  U.g?E.i..9x.....
00000190: 5442 1240 0796 6cc8 b2f6 1ef9 8d13 421d  TB.@..l.......B.
000001a0: 461f 2e68 4d91 5343 34b5 56e7 46d0 0a0a  F..hM.SC4.V.F...
000001b0: 72b7 d873 71d9 6f09 c326 402d dbc0 7cef  r..sq.o..&@-..|.
000001c0: 53b1 df60 9ec7 f318 00df 3907 2e85 d85b  S..`......9....[
000001d0: 6a1a e105 0207 c580 e31d 82d5 8646 183c  j............F.<
000001e0: 6a04 4911 101a 5427 087c 1f94 47a2 270d  j.I...T'.|..G.'.
000001f0: ad12 fc5c 9ad2 5714 514f 34ba 701d fb69  ...\..W.QO4.p..i
00000200: 8eed 0183 e2a1 53ea 2300 26bb bd2f 13df  ......S.#.&../..
00000210: b703 08a3 2309 e43c 44bf 75d4 905e 5f96  ....#..<D.u..^_.
00000220: 481b 362e e82d 9093 7741 740c e65b c7f1  H.6..-..wAt..[..
00000230: 5550 f247 9043 5097 d626 3a16 da32 c213  UP.G.CP..&:..2..
00000240: 2acd 298a 5c8a f0c1 b99f e2ee 48a7 0a12  *.).\.......H...
00000250: 03b5 5cb3 0037 cece 773c 0200 00         ..\..7..w<...
bandit12@bandit:~$ 
```

```sh
bandit12@bandit:~$ mkdir /tmp/kanishka
bandit12@bandit:~$ 
```

```sh
bandit12@bandit:~$ cd /tmp/kanishka
bandit12@bandit:/tmp/kanishka$ 
```

```sh
bandit12@bandit:/tmp/kanishka$ cp ~/data.txt .
```

```sh 
bandit12@bandit:/tmp/kanishka$ file data.txt 
data.txt: ASCII text
bandit12@bandit:/tmp/kanishka$ 
```

```sh
bandit12@bandit:/tmp/kanishka$ cat data.txt | xxd -r > result
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ ls -l result 
-rw-r--r-- 1 bandit12 root 605 Dec  9 08:27 result
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ file result 
result: gzip compressed data, was "data2.bin", last modified: Tue Oct 16 12:00:23 2018, max compression, from Unix
bandit12@bandit:/tmp/kanishka$ 
```

```sh
bandit12@bandit:/tmp/kanishka$ mv result result.gz
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ gzip -d result.gz 
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ ls -l
total 8
-rw-r----- 1 bandit12 root 2581 Dec  9 07:53 data.txt
-rw-r--r-- 1 bandit12 root  572 Dec  9 08:28 result
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ file result 
result: bzip2 compressed data, block size = 900k
bandit12@bandit:/tmp/kanishka$ 
```

```sh
bandit12@bandit:/tmp/kanishka$ bzip2 -d result
bzip2: Can't guess original name for result -- using result.out
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ ls -l
total 8
-rw-r----- 1 bandit12 root 2581 Dec  9 07:53 data.txt
-rw-r--r-- 1 bandit12 root  435 Dec  9 08:28 result.out
bandit12@bandit:/tmp/kanishka$  
bandit12@bandit:/tmp/kanishka$ file result.out 
result.out: gzip compressed data, was "data4.bin", last modified: Tue Oct 16 12:00:23 2018, max compression, from Unix
bandit12@bandit:/tmp/kanishka$ 
```

```sh
bandit12@bandit:/tmp/kanishka$ mv result.out result.out.gz
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ gzip -d result.out.gz 
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ ls -l
total 24
-rw-r----- 1 bandit12 root  2581 Dec  9 07:53 data.txt
-rw-r--r-- 1 bandit12 root 20480 Dec  9 08:28 result.out
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ file result.out 
result.out: POSIX tar archive (GNU)
bandit12@bandit:/tmp/kanishka$ 
```

```sh
bandit12@bandit:/tmp/kanishka$ mv result.out result.out.tar
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ tar xvf result.out.tar 
data5.bin
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ file data5.bin 
data5.bin: POSIX tar archive (GNU)
bandit12@bandit:/tmp/kanishka$ 
```

```sh
bandit12@bandit:/tmp/kanishka$ mv data5.bin data5.bin.tar
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ tar xvf data5.bin.tar 
data6.bin
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ file data6.bin 
data6.bin: bzip2 compressed data, block size = 900k
bandit12@bandit:/tmp/kanishka$ 
```

```sh
bandit12@bandit:/tmp/kanishka$ mv data6.bin data6.bin.bz2
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ bzip2 -d data6.bin.bz2 
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ ls -l
total 48
-rw-r--r-- 1 bandit12 root 10240 Oct 16  2018 data5.bin.tar
-rw-r--r-- 1 bandit12 root 10240 Oct 16  2018 data6.bin
-rw-r----- 1 bandit12 root  2581 Dec  9 07:53 data.txt
-rw-r--r-- 1 bandit12 root 20480 Dec  9 08:28 result.out.tar
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ file data6.bin 
data6.bin: POSIX tar archive (GNU)
bandit12@bandit:/tmp/kanishka$ 
```

```sh
bandit12@bandit:/tmp/kanishka$ mv data6.bin data6.bin.tar
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ tar xvf data6.bin.tar 
data8.bin
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ file data8.bin 
data8.bin: gzip compressed data, was "data9.bin", last modified: Tue Oct 16 12:00:23 2018, max compression, from Unix
bandit12@bandit:/tmp/kanishka$ 
```

```sh
bandit12@bandit:/tmp/kanishka$ mv data8.bin data8.bin.gz
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ gzip -d data8.bin.gz 
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ ls -l
total 52
-rw-r--r-- 1 bandit12 root 10240 Oct 16  2018 data5.bin.tar
-rw-r--r-- 1 bandit12 root 10240 Oct 16  2018 data6.bin.tar
-rw-r--r-- 1 bandit12 root    49 Oct 16  2018 data8.bin
-rw-r----- 1 bandit12 root  2581 Dec  9 07:53 data.txt
-rw-r--r-- 1 bandit12 root 20480 Dec  9 08:28 result.out.tar
bandit12@bandit:/tmp/kanishka$ 
bandit12@bandit:/tmp/kanishka$ file data8.bin 
data8.bin: ASCII text
bandit12@bandit:/tmp/kanishka$ 
```

```sh
bandit12@bandit:/tmp/kanishka$ cat data8.bin 
The password is 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL
bandit12@bandit:/tmp/kanishka$ 
```

----

###### Level 13 → Level 14

```sh
ctf@ctf-vm:~$ ssh bandit13@bandit.labs.overthewire.org -p 2220
bandit13@bandit.labs.overthewire.org's password: 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL
bandit13@bandit:~$ 
```

```sh
bandit13@bandit:~$ ls -l
total 4
-rw-r----- 1 bandit14 bandit13 1679 Oct 16  2018 sshkey.private
bandit13@bandit:~$ 
```

```sh
bandit13@bandit:~$ cat sshkey.private 
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAxkkOE83W2cOT7IWhFc9aPaaQmQDdgzuXCv+ppZHa++buSkN+
gg0tcr7Fw8NLGa5+Uzec2rEg0WmeevB13AIoYp0MZyETq46t+jk9puNwZwIt9XgB
ZufGtZEwWbFWw/vVLNwOXBe4UWStGRWzgPpEeSv5Tb1VjLZIBdGphTIK22Amz6Zb
ThMsiMnyJafEwJ/T8PQO3myS91vUHEuoOMAzoUID4kN0MEZ3+XahyK0HJVq68KsV
ObefXG1vvA3GAJ29kxJaqvRfgYnqZryWN7w3CHjNU4c/2Jkp+n8L0SnxaNA+WYA7
jiPyTF0is8uzMlYQ4l1Lzh/8/MpvhCQF8r22dwIDAQABAoIBAQC6dWBjhyEOzjeA
J3j/RWmap9M5zfJ/wb2bfidNpwbB8rsJ4sZIDZQ7XuIh4LfygoAQSS+bBw3RXvzE
pvJt3SmU8hIDuLsCjL1VnBY5pY7Bju8g8aR/3FyjyNAqx/TLfzlLYfOu7i9Jet67
xAh0tONG/u8FB5I3LAI2Vp6OviwvdWeC4nOxCthldpuPKNLA8rmMMVRTKQ+7T2VS
nXmwYckKUcUgzoVSpiNZaS0zUDypdpy2+tRH3MQa5kqN1YKjvF8RC47woOYCktsD
o3FFpGNFec9Taa3Msy+DfQQhHKZFKIL3bJDONtmrVvtYK40/yeU4aZ/HA2DQzwhe
ol1AfiEhAoGBAOnVjosBkm7sblK+n4IEwPxs8sOmhPnTDUy5WGrpSCrXOmsVIBUf
laL3ZGLx3xCIwtCnEucB9DvN2HZkupc/h6hTKUYLqXuyLD8njTrbRhLgbC9QrKrS
M1F2fSTxVqPtZDlDMwjNR04xHA/fKh8bXXyTMqOHNJTHHNhbh3McdURjAoGBANkU
1hqfnw7+aXncJ9bjysr1ZWbqOE5Nd8AFgfwaKuGTTVX2NsUQnCMWdOp+wFak40JH
PKWkJNdBG+ex0H9JNQsTK3X5PBMAS8AfX0GrKeuwKWA6erytVTqjOfLYcdp5+z9s
8DtVCxDuVsM+i4X8UqIGOlvGbtKEVokHPFXP1q/dAoGAcHg5YX7WEehCgCYTzpO+
xysX8ScM2qS6xuZ3MqUWAxUWkh7NGZvhe0sGy9iOdANzwKw7mUUFViaCMR/t54W1
GC83sOs3D7n5Mj8x3NdO8xFit7dT9a245TvaoYQ7KgmqpSg/ScKCw4c3eiLava+J
3btnJeSIU+8ZXq9XjPRpKwUCgYA7z6LiOQKxNeXH3qHXcnHok855maUj5fJNpPbY
iDkyZ8ySF8GlcFsky8Yw6fWCqfG3zDrohJ5l9JmEsBh7SadkwsZhvecQcS9t4vby
9/8X4jS0P8ibfcKS4nBP+dT81kkkg5Z5MohXBORA7VWx+ACohcDEkprsQ+w32xeD
qT1EvQKBgQDKm8ws2ByvSUVs9GjTilCajFqLJ0eVYzRPaY6f++Gv/UVfAPV4c+S0
kAWpXbv5tbkkzbS0eaLPTKgLzavXtQoTtKwrjpolHKIHUz6Wu+n4abfAIRFubOdN
/+aLoRQ0yBDRbdXMsZN/jvY44eM+xRLdRVyMmdPtP8belRi2E2aEzA==
-----END RSA PRIVATE KEY-----
bandit13@bandit:~$ 
```

```sh
bandit13@bandit:~$ ssh -i sshkey.private bandit14@localhost
bandit14@bandit:~$ 
```

```sh
bandit14@bandit:~$ cat /etc/bandit_pass/bandit14
4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e
bandit14@bandit:~$ 
```

----

###### Level 14 → Level 15

```sh
ctf@ctf-vm:~$ ssh bandit14@bandit.labs.overthewire.org -p 2220
bandit14@bandit.labs.overthewire.org's password: 4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e
bandit14@bandit:~$ 
```

```sh
bandit14@bandit:~$ nc localhost 30000
4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e
Correct!
BfMYroe26WYalil77FoDi9qh59eK5xNr

bandit14@bandit:~$ 
```

----

###### Level 15 → Level 16

```sh
ctf@ctf-vm:~$ ssh bandit15@bandit.labs.overthewire.org -p 2220
bandit15@bandit.labs.overthewire.org's password: BfMYroe26WYalil77FoDi9qh59eK5xNr
bandit15@bandit:~$ 
```

```sh
bandit15@bandit:~$ openssl s_client -connect localhost:30001
CONNECTED(00000003)
depth=0 CN = localhost
verify error:num=18:self signed certificate
verify return:1
depth=0 CN = localhost
verify return:1
---
Certificate chain
 0 s:/CN=localhost
   i:/CN=localhost
---
Server certificate
-----BEGIN CERTIFICATE-----
MIICBjCCAW+gAwIBAgIEfkeLojANBgkqhkiG9w0BAQUFADAUMRIwEAYDVQQDDAls
b2NhbGhvc3QwHhcNMTkwODAzMDc0OTMxWhcNMjAwODAyMDc0OTMxWjAUMRIwEAYD
VQQDDAlsb2NhbGhvc3QwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMDGwHmT
GntqHvPYiM0wm4Dsmhlmiywaj0CGZKW1Cx6ze9pH+iWXEvcnWga4Kfevqh0LJLeS
jmgE6hFRK9rTwq+q6UE0hADazxb7r8jpthnHwKyRGEtFmsFTv/JqJDk+V5cngA4Y
m4scTjF+r1Y7jQA5VkUPHy+eYoNoqRqGh7JhAgMBAAGjZTBjMBQGA1UdEQQNMAuC
CWxvY2FsaG9zdDBLBglghkgBhvhCAQ0EPhY8QXV0b21hdGljYWxseSBnZW5lcmF0
ZWQgYnkgTmNhdC4gU2VlIGh0dHBzOi8vbm1hcC5vcmcvbmNhdC8uMA0GCSqGSIb3
DQEBBQUAA4GBAEICbhntCy/wyg56HQpox3nt8YtTkr6g21P4akxso7m08u6FuyiY
t/8yd+iph6qlRDHQ+D8T4TcpflsV8YKPXIgMoJQtGkuVgqHeCfgBEJcx+T52F8aX
84l5d7tEr9XEuCPKIlf4/GL8wOQLww2a2+sjlSwa8S1XlkbC61JzPyS3
-----END CERTIFICATE-----
subject=/CN=localhost
issuer=/CN=localhost
---
No client certificate CA names sent
Peer signing digest: SHA512
Server Temp Key: X25519, 253 bits
---
SSL handshake has read 1019 bytes and written 269 bytes
Verification error: self signed certificate
---
New, TLSv1.2, Cipher is ECDHE-RSA-AES256-GCM-SHA384
Server public key is 1024 bit
Secure Renegotiation IS supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
SSL-Session:
    Protocol  : TLSv1.2
    Cipher    : ECDHE-RSA-AES256-GCM-SHA384
    Session-ID: 6BF69D604F0B171765A25807C947E9515B94C00572D89B48E68E23105ED9D20A
    Session-ID-ctx: 
    Master-Key: 08962A6588F2D6D404A8FEACBF0EEA6FE2AADCC65145199B803FE07454533863E19EA7AF6DA0BC9A934D9E99BEE7AAFB
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - 6a 32 a6 c7 27 26 f0 c8-b4 75 99 96 41 ed a8 13   j2..'&...u..A...
    0010 - a5 d8 22 eb 98 ed 82 ab-05 4e 01 06 e0 64 84 5a   .."......N...d.Z
    0020 - 89 a7 27 2a 62 66 85 91-c8 a2 b9 09 f8 de 20 7c   ..'*bf........ |
    0030 - 34 ad 30 ca 22 c8 be 1c-06 9c 92 32 fc ee 75 5d   4.0."......2..u]
    0040 - 06 51 6b d8 ce c8 86 95-f0 46 4f 7f 91 a5 3a a1   .Qk......FO...:.
    0050 - 1b 86 70 40 82 36 38 21-c7 33 ca 6d 1f 97 53 9d   ..p@.68!.3.m..S.
    0060 - c8 04 14 40 e4 7f 36 e2-ba 38 77 35 17 3f 55 c9   ...@..6..8w5.?U.
    0070 - 64 90 9b df 1c e2 e1 7b-98 5f a2 e1 04 62 87 06   d......{._...b..
    0080 - 37 7c b0 23 b2 d3 c9 7f-02 87 6f 41 5f a4 94 66   7|.#......oA_..f
    0090 - b7 11 c0 a7 a7 be ac aa-a2 07 56 ff 3f d5 bf b3   ..........V.?...

    Start Time: 1575878124
    Timeout   : 7200 (sec)
    Verify return code: 18 (self signed certificate)
    Extended master secret: yes
---
BfMYroe26WYalil77FoDi9qh59eK5xNr
Correct!
cluFn7wTiGryunymYOu4RcffSxQluehd

closed
bandit15@bandit:~$ 
```

----

###### Level 16 → Level 17

```sh
ctf@ctf-vm:~$ ssh bandit16@bandit.labs.overthewire.org -p 2220
bandit16@bandit.labs.overthewire.org's password: cluFn7wTiGryunymYOu4RcffSxQluehd
bandit16@bandit:~$ 
```

```sh
bandit16@bandit:~$ nmap localhost -p 31000-32000

Starting Nmap 7.40 ( https://nmap.org ) at 2019-12-09 08:57 CET
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00019s latency).
Not shown: 999 closed ports
PORT      STATE    SERVICE
31518/tcp filtered unknown
31790/tcp open     unknown

Nmap done: 1 IP address (1 host up) scanned in 1.25 seconds
bandit16@bandit:~$ 
```

```sh
bandit16@bandit:~$ openssl s_client -connect localhost:31790 
CONNECTED(00000003)
depth=0 CN = localhost
verify error:num=18:self signed certificate
verify return:1
depth=0 CN = localhost
verify return:1
---
Certificate chain
 0 s:/CN=localhost
   i:/CN=localhost
---
Server certificate
-----BEGIN CERTIFICATE-----
MIICBjCCAW+gAwIBAgIEbSNYOzANBgkqhkiG9w0BAQUFADAUMRIwEAYDVQQDDAls
b2NhbGhvc3QwHhcNMTkxMTI2MDMzNzA3WhcNMjAxMTI1MDMzNzA3WjAUMRIwEAYD
VQQDDAlsb2NhbGhvc3QwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBAMK/1fWi
3jCBydYlpk1fH5e96vpfdBFXtNXo8foquNUmvdFleKOUIFova64TG6KP6FVzEsV9
xvda7w7HWLYV9n6mX+QUTOFCRAGGrfLMyVtbzbn4B/QHaN6VUpF6nSeKys/H9LW8
jUrW2NaIrMXyOkmcrRHTNt96sGyIwYEOJfJfAgMBAAGjZTBjMBQGA1UdEQQNMAuC
CWxvY2FsaG9zdDBLBglghkgBhvhCAQ0EPhY8QXV0b21hdGljYWxseSBnZW5lcmF0
ZWQgYnkgTmNhdC4gU2VlIGh0dHBzOi8vbm1hcC5vcmcvbmNhdC8uMA0GCSqGSIb3
DQEBBQUAA4GBAFe9QZAhX0RNQIJ92lHIyuh85LlUGfKQPr4psE3tXdrcX9bV0Ici
PRSaFzX8hlBHcwtNmgJjmv5JmyFi7vyIx6JOKf4Eu+Hnxd0SQ2S8090PIM6cg8eS
2viDh3dTUeY7vIGqK/p/TXi3n4YVnpd6uzkCyGUmK+37FRjQOYbZvnt/
-----END CERTIFICATE-----
subject=/CN=localhost
issuer=/CN=localhost
---
No client certificate CA names sent
Peer signing digest: SHA512
Server Temp Key: X25519, 253 bits
---
SSL handshake has read 1019 bytes and written 269 bytes
Verification error: self signed certificate
---
New, TLSv1.2, Cipher is ECDHE-RSA-AES256-GCM-SHA384
Server public key is 1024 bit
Secure Renegotiation IS supported
Compression: NONE
Expansion: NONE
No ALPN negotiated
SSL-Session:
    Protocol  : TLSv1.2
    Cipher    : ECDHE-RSA-AES256-GCM-SHA384
    Session-ID: 42EF76AFAF66C6F836B1EFC1FB23C7F356ED17C1BB188C53D5E68D6EF92D9B55
    Session-ID-ctx: 
    Master-Key: 0743CCF870CC8101D0AF7008A6EA3A5117BA345F27C464EE3FCD2E38F44D98992883008DF2B6A58CB09F19B092595FF9
    PSK identity: None
    PSK identity hint: None
    SRP username: None
    TLS session ticket lifetime hint: 7200 (seconds)
    TLS session ticket:
    0000 - 63 2b 91 29 36 5b 10 08-a3 16 68 1e e1 f3 bd 40   c+.)6[....h....@
    0010 - cd da 55 90 74 a3 39 d2-00 84 c2 4c c5 c7 a4 c8   ..U.t.9....L....
    0020 - 2b c4 e9 12 b2 8e c7 46-d3 23 f3 1d dc bd e3 0f   +......F.#......
    0030 - 33 97 35 c8 47 46 23 f1-f5 cb 62 bf e4 91 95 f0   3.5.GF#...b.....
    0040 - 94 ee 86 fe c7 78 fe ad-99 78 7b 42 71 ca 86 b0   .....x...x{Bq...
    0050 - 0f d8 7b 42 3f 67 0c b0-36 96 bd 19 b9 9e 5b 09   ..{B?g..6.....[.
    0060 - de dd 6c 5c dd b7 c7 22-aa 03 80 9a 87 f4 a2 05   ..l\..."........
    0070 - 85 21 d0 e0 38 f5 7c 02-67 36 2a 24 bc 38 ee 4b   .!..8.|.g6*$.8.K
    0080 - 40 20 b9 4f 20 17 08 62-82 3f d3 a7 7a b0 13 84   @ .O ..b.?..z...
    0090 - 8c 5d 8c 81 61 e8 8f b5-33 7e 44 ad be a4 f4 70   .]..a...3~D....p

    Start Time: 1575878313
    Timeout   : 7200 (sec)
    Verify return code: 18 (self signed certificate)
    Extended master secret: yes
---
cluFn7wTiGryunymYOu4RcffSxQluehd
Correct!
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAvmOkuifmMg6HL2YPIOjon6iWfbp7c3jx34YkYWqUH57SUdyJ
imZzeyGC0gtZPGujUSxiJSWI/oTqexh+cAMTSMlOJf7+BrJObArnxd9Y7YT2bRPQ
Ja6Lzb558YW3FZl87ORiO+rW4LCDCNd2lUvLE/GL2GWyuKN0K5iCd5TbtJzEkQTu
DSt2mcNn4rhAL+JFr56o4T6z8WWAW18BR6yGrMq7Q/kALHYW3OekePQAzL0VUYbW
JGTi65CxbCnzc/w4+mqQyvmzpWtMAzJTzAzQxNbkR2MBGySxDLrjg0LWN6sK7wNX
x0YVztz/zbIkPjfkU1jHS+9EbVNj+D1XFOJuaQIDAQABAoIBABagpxpM1aoLWfvD
KHcj10nqcoBc4oE11aFYQwik7xfW+24pRNuDE6SFthOar69jp5RlLwD1NhPx3iBl
J9nOM8OJ0VToum43UOS8YxF8WwhXriYGnc1sskbwpXOUDc9uX4+UESzH22P29ovd
d8WErY0gPxun8pbJLmxkAtWNhpMvfe0050vk9TL5wqbu9AlbssgTcCXkMQnPw9nC
YNN6DDP2lbcBrvgT9YCNL6C+ZKufD52yOQ9qOkwFTEQpjtF4uNtJom+asvlpmS8A
vLY9r60wYSvmZhNqBUrj7lyCtXMIu1kkd4w7F77k+DjHoAXyxcUp1DGL51sOmama
+TOWWgECgYEA8JtPxP0GRJ+IQkX262jM3dEIkza8ky5moIwUqYdsx0NxHgRRhORT
8c8hAuRBb2G82so8vUHk/fur85OEfc9TncnCY2crpoqsghifKLxrLgtT+qDpfZnx
SatLdt8GfQ85yA7hnWWJ2MxF3NaeSDm75Lsm+tBbAiyc9P2jGRNtMSkCgYEAypHd
HCctNi/FwjulhttFx/rHYKhLidZDFYeiE/v45bN4yFm8x7R/b0iE7KaszX+Exdvt
SghaTdcG0Knyw1bpJVyusavPzpaJMjdJ6tcFhVAbAjm7enCIvGCSx+X3l5SiWg0A
R57hJglezIiVjv3aGwHwvlZvtszK6zV6oXFAu0ECgYAbjo46T4hyP5tJi93V5HDi
Ttiek7xRVxUl+iU7rWkGAXFpMLFteQEsRr7PJ/lemmEY5eTDAFMLy9FL2m9oQWCg
R8VdwSk8r9FGLS+9aKcV5PI/WEKlwgXinB3OhYimtiG2Cg5JCqIZFHxD6MjEGOiu
L8ktHMPvodBwNsSBULpG0QKBgBAplTfC1HOnWiMGOU3KPwYWt0O6CdTkmJOmL8Ni
blh9elyZ9FsGxsgtRBXRsqXuz7wtsQAgLHxbdLq/ZJQ7YfzOKU4ZxEnabvXnvWkU
YOdjHdSOoKvDQNWu6ucyLRAWFuISeXw9a/9p7ftpxm0TSgyvmfLF2MIAEwyzRqaM
77pBAoGAMmjmIJdjp+Ez8duyn3ieo36yrttF5NSsJLAbxFpdlc1gvtGCWW+9Cq0b
dxviW8+TFVEBl1O4f7HVm6EpTscdDxU+bCXWkfjuRb7Dy9GOtt9JPsX8MBTakzh3
vBgsyi/sN3RqRBcGU40fOoZyfAMT8s1m/uYv52O6IgeuZ/ujbjY=
-----END RSA PRIVATE KEY-----

closed
bandit16@bandit:~$ 
```

----

###### Level 17 → Level 18

```sh
ctf@ctf-vm:~$ nano level17.key 
ctf@ctf-vm:~$ cat level17.key 
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAvmOkuifmMg6HL2YPIOjon6iWfbp7c3jx34YkYWqUH57SUdyJ
imZzeyGC0gtZPGujUSxiJSWI/oTqexh+cAMTSMlOJf7+BrJObArnxd9Y7YT2bRPQ
Ja6Lzb558YW3FZl87ORiO+rW4LCDCNd2lUvLE/GL2GWyuKN0K5iCd5TbtJzEkQTu
DSt2mcNn4rhAL+JFr56o4T6z8WWAW18BR6yGrMq7Q/kALHYW3OekePQAzL0VUYbW
JGTi65CxbCnzc/w4+mqQyvmzpWtMAzJTzAzQxNbkR2MBGySxDLrjg0LWN6sK7wNX
x0YVztz/zbIkPjfkU1jHS+9EbVNj+D1XFOJuaQIDAQABAoIBABagpxpM1aoLWfvD
KHcj10nqcoBc4oE11aFYQwik7xfW+24pRNuDE6SFthOar69jp5RlLwD1NhPx3iBl
J9nOM8OJ0VToum43UOS8YxF8WwhXriYGnc1sskbwpXOUDc9uX4+UESzH22P29ovd
d8WErY0gPxun8pbJLmxkAtWNhpMvfe0050vk9TL5wqbu9AlbssgTcCXkMQnPw9nC
YNN6DDP2lbcBrvgT9YCNL6C+ZKufD52yOQ9qOkwFTEQpjtF4uNtJom+asvlpmS8A
vLY9r60wYSvmZhNqBUrj7lyCtXMIu1kkd4w7F77k+DjHoAXyxcUp1DGL51sOmama
+TOWWgECgYEA8JtPxP0GRJ+IQkX262jM3dEIkza8ky5moIwUqYdsx0NxHgRRhORT
8c8hAuRBb2G82so8vUHk/fur85OEfc9TncnCY2crpoqsghifKLxrLgtT+qDpfZnx
SatLdt8GfQ85yA7hnWWJ2MxF3NaeSDm75Lsm+tBbAiyc9P2jGRNtMSkCgYEAypHd
HCctNi/FwjulhttFx/rHYKhLidZDFYeiE/v45bN4yFm8x7R/b0iE7KaszX+Exdvt
SghaTdcG0Knyw1bpJVyusavPzpaJMjdJ6tcFhVAbAjm7enCIvGCSx+X3l5SiWg0A
R57hJglezIiVjv3aGwHwvlZvtszK6zV6oXFAu0ECgYAbjo46T4hyP5tJi93V5HDi
Ttiek7xRVxUl+iU7rWkGAXFpMLFteQEsRr7PJ/lemmEY5eTDAFMLy9FL2m9oQWCg
R8VdwSk8r9FGLS+9aKcV5PI/WEKlwgXinB3OhYimtiG2Cg5JCqIZFHxD6MjEGOiu
L8ktHMPvodBwNsSBULpG0QKBgBAplTfC1HOnWiMGOU3KPwYWt0O6CdTkmJOmL8Ni
blh9elyZ9FsGxsgtRBXRsqXuz7wtsQAgLHxbdLq/ZJQ7YfzOKU4ZxEnabvXnvWkU
YOdjHdSOoKvDQNWu6ucyLRAWFuISeXw9a/9p7ftpxm0TSgyvmfLF2MIAEwyzRqaM
77pBAoGAMmjmIJdjp+Ez8duyn3ieo36yrttF5NSsJLAbxFpdlc1gvtGCWW+9Cq0b
dxviW8+TFVEBl1O4f7HVm6EpTscdDxU+bCXWkfjuRb7Dy9GOtt9JPsX8MBTakzh3
vBgsyi/sN3RqRBcGU40fOoZyfAMT8s1m/uYv52O6IgeuZ/ujbjY=
-----END RSA PRIVATE KEY-----

ctf@ctf-vm:~$ 
```

```sh
ctf@ctf-vm:~$ chmod 600 level17.key 
```

```sh
ctf@ctf-vm:~$ ls -l level17.key 
-rw------- 1 ctf ctf 1676 Dec  9 03:04 level17.key
ctf@ctf-vm:~$ 
```

```sh
ctf@ctf-vm:~$ ssh -i level17.key bandit17@bandit.labs.overthewire.org -p 2220
bandit17@bandit:~$ 
```

```sh
bandit17@bandit:~$ ls -l
total 8
-rw-r----- 1 bandit18 bandit17 3300 Oct 16  2018 passwords.new
-rw-r----- 1 bandit18 bandit17 3300 Oct 16  2018 passwords.old
bandit17@bandit:~$ 
```

```sh
bandit17@bandit:~$ diff passwords.new passwords.old 
42c42
< kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd
---
> hlbSBPAWJmL6WFDb06gpTx1pPButblOA
bandit17@bandit:~$ 
```

----

###### Level 18 → Level 19

```sh
ctf@ctf-vm:~$ ssh bandit18@bandit.labs.overthewire.org -p 2220
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit18@bandit.labs.overthewire.org's password: kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd
Byebye !
Connection to bandit.labs.overthewire.org closed.
ctf@ctf-vm:~$ 
```

```sh
ctf@ctf-vm:~$ ssh bandit18@bandit.labs.overthewire.org -p 2220 "cat ~/readme"
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit18@bandit.labs.overthewire.org's password: 
IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x
ctf@ctf-vm:~$ 
```

----

###### Level 19 → Level 20

```sh
ctf@ctf-vm:~$ ssh bandit19@bandit.labs.overthewire.org -p 2220 
bandit19@bandit.labs.overthewire.org's password: IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x
bandit19@bandit:~$ 
```

```sh
bandit19@bandit:~$ ls -l
total 8
-rwsr-x--- 1 bandit20 bandit19 7296 Oct 16  2018 bandit20-do
bandit19@bandit:~$ 
```

```sh
bandit19@bandit:~$ ./bandit20-do 
Run a command as another user.
  Example: ./bandit20-do id
bandit19@bandit:~$ 
```

```sh
bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/* 2>/dev/null
GbKksEFF4yrVs6il55v6gwY5aVje5f0j
bandit19@bandit:~$ 
```

- [suid](https://en.wikipedia.org/wiki/Setuid)

----

###### Level 20 → Level 21

```sh
ctf@ctf-vm:~$ ssh bandit20@bandit.labs.overthewire.org -p 2220 
bandit20@bandit.labs.overthewire.org's password: GbKksEFF4yrVs6il55v6gwY5aVje5f0j
bandit20@bandit:~$ 
```

```sh
bandit20@bandit:~$ nc -nlvp 25000
listening on [any] 25000 ...
connect to [127.0.0.1] from (UNKNOWN) [127.0.0.1] 43358
GbKksEFF4yrVs6il55v6gwY5aVje5f0j
gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr
bandit20@bandit:~$ 
```

```sh
bandit20@bandit:~$ ./suconnect 25000
Read: GbKksEFF4yrVs6il55v6gwY5aVje5f0j
Password matches, sending next password
bandit20@bandit:~$ 
```

----

###### Level 21 → Level 22

```sh
ctf@ctf-vm:~$ ssh bandit21@bandit.labs.overthewire.org -p 2220 
bandit21@bandit.labs.overthewire.org's password: gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr
bandit21@bandit:~$ 
```

```sh
bandit21@bandit:~$ cd /etc/cron.d
bandit21@bandit:/etc/cron.d$ ls -l
total 16
-rw-r--r-- 1 root root 189 Jan 25  2017 atop
-rw-r--r-- 1 root root 120 Oct 16  2018 cronjob_bandit22
-rw-r--r-- 1 root root 122 Oct 16  2018 cronjob_bandit23
-rw-r--r-- 1 root root 120 Oct 16  2018 cronjob_bandit24
bandit21@bandit:/etc/cron.d$ 
```

```sh
bandit21@bandit:/etc/cron.d$ cat atop 
PATH=/bin:/usr/bin:/sbin:/usr/sbin

# daily restart of atop at midnight
0 0 * * * root if [ -d "/run/systemd/system" ]; then systemctl restart atop; else /usr/share/atop/atop.daily \& ; fi
bandit21@bandit:/etc/cron.d$ 
```

```sh
bandit21@bandit:/etc/cron.d$ cat cronjob_bandit22 
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
bandit21@bandit:/etc/cron.d$
```

```sh
bandit21@bandit:/etc/cron.d$ cat cronjob_bandit23 
@reboot bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
bandit21@bandit:/etc/cron.d$ 
```

```sh
bandit21@bandit:/etc/cron.d$ cat cronjob_bandit24
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
bandit21@bandit:/etc/cron.d$ 
```

```sh
bandit21@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit22.sh
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
bandit21@bandit:/etc/cron.d$ 
```

```sh
bandit21@bandit:/etc/cron.d$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI
bandit21@bandit:/etc/cron.d$ 
```

- [Linux/Mac Tutorial: Cron Jobs - How to Schedule Commands with crontab](https://www.youtube.com/watch?v=QZJ1drMQz1A)
- [crontab.guru](https://crontab.guru/)

----

###### Level 22 → Level 23

```sh
ctf@ctf-vm:~$ ssh bandit22@bandit.labs.overthewire.org -p 2220 
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit22@bandit.labs.overthewire.org's password: Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI
bandit22@bandit:~$ 
```

```sh
bandit22@bandit:~$ cd /etc/cron.d
bandit22@bandit:/etc/cron.d$ ls -l
total 16
-rw-r--r-- 1 root root 189 Jan 25  2017 atop
-rw-r--r-- 1 root root 120 Oct 16  2018 cronjob_bandit22
-rw-r--r-- 1 root root 122 Oct 16  2018 cronjob_bandit23
-rw-r--r-- 1 root root 120 Oct 16  2018 cronjob_bandit24
bandit22@bandit:/etc/cron.d$ 
```

```sh
bandit22@bandit:/etc/cron.d$ cat atop 
PATH=/bin:/usr/bin:/sbin:/usr/sbin

# daily restart of atop at midnight
0 0 * * * root if [ -d "/run/systemd/system" ]; then systemctl restart atop; else /usr/share/atop/atop.daily \& ; fi
bandit22@bandit:/etc/cron.d$ 
```

```sh
bandit22@bandit:/etc/cron.d$ cat cronjob_bandit22
@reboot bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
* * * * * bandit22 /usr/bin/cronjob_bandit22.sh &> /dev/null
bandit22@bandit:/etc/cron.d$ 
```

```sh
bandit22@bandit:/etc/cron.d$ cat cronjob_bandit23
@reboot bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
bandit22@bandit:/etc/cron.d$ 
```

```sh
bandit22@bandit:/etc/cron.d$ cat cronjob_bandit24
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
bandit22@bandit:/etc/cron.d$ 
```

```sh
bandit22@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit22.sh
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
bandit22@bandit:/etc/cron.d$ 
```

```sh
bandit22@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit23.sh
#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
bandit22@bandit:/etc/cron.d$ 
```

```sh
bandit22@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit24.sh
cat: /usr/bin/cronjob_bandit24.sh: Permission denied
bandit22@bandit:/etc/cron.d$ 
```

```sh
#!/bin/bash

myname=bandit23
mytarget=8ca319486bfbbc3663ea0fbe81326349

echo "Copying passwordfile /etc/bandit_pass/bandit23 to /tmp/8ca319486bfbbc3663ea0fbe81326349"

cat /etc/bandit_pass/bandit23 > /tmp/8ca319486bfbbc3663ea0fbe81326349
```

```sh
bandit22@bandit:~$ cat /tmp/8ca319486bfbbc3663ea0fbe81326349
jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n
bandit22@bandit:~$ 
```

----

###### Level 23 → Level 24

```sh
ctf@ctf-vm:~$ ssh bandit23@bandit.labs.overthewire.org -p 2220 
bandit23@bandit.labs.overthewire.org's password: jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n
bandit23@bandit:~$ 
```

```sh
bandit23@bandit:~$ cd /etc/cron.d
bandit23@bandit:/etc/cron.d$ ls -l
total 16
-rw-r--r-- 1 root root 189 Jan 25  2017 atop
-rw-r--r-- 1 root root 120 Oct 16  2018 cronjob_bandit22
-rw-r--r-- 1 root root 122 Oct 16  2018 cronjob_bandit23
-rw-r--r-- 1 root root 120 Oct 16  2018 cronjob_bandit24
bandit23@bandit:/etc/cron.d$ cat cronjob_bandit24
@reboot bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
* * * * * bandit24 /usr/bin/cronjob_bandit24.sh &> /dev/null
bandit23@bandit:/etc/cron.d$ 
```

```sh
bandit23@bandit:/etc/cron.d$ cat /usr/bin/cronjob_bandit24.sh
#!/bin/bash

myname=$(whoami)

cd /var/spool/$myname
echo "Executing and deleting all scripts in /var/spool/$myname:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
	echo "Handling $i"
	timeout -s 9 60 ./$i
	rm -f ./$i
    fi
done


bandit23@bandit:/etc/cron.d$ 
```

```sh
bandit23@bandit:/etc/cron.d$ mkdir -p /tmp/level24unlock
bandit23@bandit:/etc/cron.d$ cd /tmp/level24unlock
bandit23@bandit:/tmp/level24unlock$ touch key
bandit23@bandit:/tmp/level24unlock$ chmod 666 key 
bandit23@bandit:/tmp/level24unlock$ ls -l
total 0
-rw-rw-rw- 1 bandit23 root 0 Dec 10 05:35 key
bandit23@bandit:/tmp/level24unlock$ 
```

```sh
bandit23@bandit:/tmp/level24unlock$ nano script.sh 
bandit23@bandit:/tmp/level24unlock$ cat script.sh 
#!/bin/bash

cat /etc/bandit_pass/bandit24 > /tmp/level24unlock/key
bandit23@bandit:/tmp/level24unlock$ 
bandit23@bandit:/tmp/level24unlock$ chmod 777 script.sh 
bandit23@bandit:/tmp/level24unlock$ 
bandit23@bandit:/tmp/level24unlock$ ls -l script.sh 
-rwxrwxrwx 1 bandit23 root 68 Dec 10 05:39 script.sh
bandit23@bandit:/tmp/level24unlock$ 
```

```sh
bandit23@bandit:/tmp/level24unlock$ cp script.sh /var/spool/bandit24
```

```sh
bandit23@bandit:/tmp/level24unlock$ cat key 
UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ
bandit23@bandit:/tmp/level24unlock$ 
```

----

###### Level 24 → Level 25

```sh
ctf@ctf-vm:~$ ssh bandit24@bandit.labs.overthewire.org -p 2220 
bandit24@bandit.labs.overthewire.org's password: UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ
bandit24@bandit:~$ 
```

```sh
bandit24@bandit:~$ mkdir -p /tmp/level25unlocker
```

```sh
bandit24@bandit:~$ cd /tmp/level25unlocker
bandit24@bandit:/tmp/level25unlocker$
```

```sh
bandit24@bandit:/tmp/level25unlocker$ nc localhost 30002
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ 1234
Wrong! Please enter the correct pincode. Try again.
^C
bandit24@bandit:/tmp/level25unlocker$ 
```

`crack.py`

```python
#!/usr/bin/python

import sys
import socket

HOST = '127.0.0.1'
PORT = 30002

password24 = "UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ"
pin = 0

try:
	# Connect to the server	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))

	# Print welcome message
	messageFromServer = s.recv(2048)
	print(messageFromServer)

	# Brute Force PIN
	while pin<10000:
		pinString = str(pin).zfill(4)
		message = password24 + " " + pinString + "\n"

		# Send message
		s.sendall(message)
		receivedFromServer = s.recv(1024)

		# Check result
		if "Wrong" in receivedFromServer:
		        print("Wrong Pin: %s" %pinString)
		else:
		        print(receivedFromServer)
		        break
		pin += 1
finally:
	sys.exit(1)
```

```sh
bandit24@bandit:/tmp/level25unlocker$ python crack.py 
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.

Wrong Pin: 0000
Wrong Pin: 0001
Wrong Pin: 0002
Wrong Pin: 0003
Wrong Pin: 0004
Wrong Pin: 0005
Wrong Pin: 0006
Wrong Pin: 0007
Wrong Pin: 0008
<----SNIP---->
Wrong Pin: 8984
Wrong Pin: 8985
Wrong Pin: 8986
Wrong Pin: 8987
Wrong Pin: 8988
Correct!
The password of user bandit25 is uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG

Exiting.

bandit24@bandit:/tmp/level25unlocker$ 
```

----

###### Level 25 → Level 26

```sh
ctf@ctf-vm:~$ ssh bandit25@bandit.labs.overthewire.org -p 2220 
bandit25@bandit.labs.overthewire.org's password: uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG
bandit25@bandit:~$ 
```

```sh
bandit25@bandit:~$ ls
bandit26.sshkey
bandit25@bandit:~$ 
```

```sh
bandit25@bandit:~$ cat bandit26.sshkey 
-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEApis2AuoooEqeYWamtwX2k5z9uU1Afl2F8VyXQqbv/LTrIwdW
pTfaeRHXzr0Y0a5Oe3GB/+W2+PReif+bPZlzTY1XFwpk+DiHk1kmL0moEW8HJuT9
/5XbnpjSzn0eEAfFax2OcopjrzVqdBJQerkj0puv3UXY07AskgkyD5XepwGAlJOG
xZsMq1oZqQ0W29aBtfykuGie2bxroRjuAPrYM4o3MMmtlNE5fC4G9Ihq0eq73MDi
1ze6d2jIGce873qxn308BA2qhRPJNEbnPev5gI+5tU+UxebW8KLbk0EhoXB953Ix
3lgOIrT9Y6skRjsMSFmC6WN/O7ovu8QzGqxdywIDAQABAoIBAAaXoETtVT9GtpHW
qLaKHgYtLEO1tOFOhInWyolyZgL4inuRRva3CIvVEWK6TcnDyIlNL4MfcerehwGi
il4fQFvLR7E6UFcopvhJiSJHIcvPQ9FfNFR3dYcNOQ/IFvE73bEqMwSISPwiel6w
e1DjF3C7jHaS1s9PJfWFN982aublL/yLbJP+ou3ifdljS7QzjWZA8NRiMwmBGPIh
Yq8weR3jIVQl3ndEYxO7Cr/wXXebZwlP6CPZb67rBy0jg+366mxQbDZIwZYEaUME
zY5izFclr/kKj4s7NTRkC76Yx+rTNP5+BX+JT+rgz5aoQq8ghMw43NYwxjXym/MX
c8X8g0ECgYEA1crBUAR1gSkM+5mGjjoFLJKrFP+IhUHFh25qGI4Dcxxh1f3M53le
wF1rkp5SJnHRFm9IW3gM1JoF0PQxI5aXHRGHphwPeKnsQ/xQBRWCeYpqTme9amJV
tD3aDHkpIhYxkNxqol5gDCAt6tdFSxqPaNfdfsfaAOXiKGrQESUjIBcCgYEAxvmI
2ROJsBXaiM4Iyg9hUpjZIn8TW2UlH76pojFG6/KBd1NcnW3fu0ZUU790wAu7QbbU
i7pieeqCqSYcZsmkhnOvbdx54A6NNCR2btc+si6pDOe1jdsGdXISDRHFb9QxjZCj
6xzWMNvb5n1yUb9w9nfN1PZzATfUsOV+Fy8CbG0CgYEAifkTLwfhqZyLk2huTSWm
pzB0ltWfDpj22MNqVzR3h3d+sHLeJVjPzIe9396rF8KGdNsWsGlWpnJMZKDjgZsz
JQBmMc6UMYRARVP1dIKANN4eY0FSHfEebHcqXLho0mXOUTXe37DWfZza5V9Oify3
JquBd8uUptW1Ue41H4t/ErsCgYEArc5FYtF1QXIlfcDz3oUGz16itUZpgzlb71nd
1cbTm8EupCwWR5I1j+IEQU+JTUQyI1nwWcnKwZI+5kBbKNJUu/mLsRyY/UXYxEZh
ibrNklm94373kV1US/0DlZUDcQba7jz9Yp/C3dT/RlwoIw5mP3UxQCizFspNKOSe
euPeaxUCgYEAntklXwBbokgdDup/u/3ms5Lb/bm22zDOCg2HrlWQCqKEkWkAO6R5
/Wwyqhp/wTl8VXjxWo+W+DmewGdPHGQQ5fFdqgpuQpGUq24YZS8m66v5ANBwd76t
IZdtF5HXs2S5CADTwniUS5mX1HO9l5gUkk+h0cH5JnPtsMCnAUM+BRY=
-----END RSA PRIVATE KEY-----
bandit25@bandit:~$ 
```

```sh
bandit25@bandit:~$ exit
logout
Connection to bandit.labs.overthewire.org closed.
ctf@ctf-vm:~$ 
```

```sh
ctf@ctf-vm:~$ chmod 600 bandit26.sshkey 
```

```sh
ctf@ctf-vm:~$ ssh bandit26@bandit.labs.overthewire.org -p 2220 -i bandit26.sshkey 
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

Linux bandit 4.18.12 x86_64 GNU/Linux
               
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

    * pwndbg (https://github.com/pwndbg/pwndbg) in /usr/local/pwndbg/
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

  _                     _ _ _   ___   __  
 | |                   | (_) | |__ \ / /  
 | |__   __ _ _ __   __| |_| |_   ) / /_  
 | '_ \ / _` | '_ \ / _` | | __| / / '_ \ 
 | |_) | (_| | | | | (_| | | |_ / /| (_) |
 |_.__/ \__,_|_| |_|\__,_|_|\__|____\___/ 
Connection to bandit.labs.overthewire.org closed.
ctf@ctf-vm:~$ 
```

```sh
bandit25@bandit:~$ cat /etc/passwd | grep bandit26
bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext
bandit25@bandit:~$ 
```

```sh
bandit25@bandit:~$ cat /usr/bin/showtext
#!/bin/sh

export TERM=linux

more ~/text.txt
exit 0
bandit25@bandit:~$ 
```

```sh
ctf@ctf-vm:~$ ssh bandit26@bandit.labs.overthewire.org -p 2220 -i bandit26.sshkey
```

![](images/1.png)

![](images/2.png)

```sh
v
```

![](images/3.png)

```sh
:e /etc/bandit_pass/bandit26
```

![](images/4.png)

![](images/5.png)

```
5czgV9L3Xx8JPOyRbXh6lQbmIOWvPT6Z
```

```sh
:set shell=/bin/bash
```

![](images/6.png)

```sh
:shell
```

![](images/7.png)

![](images/8.png)

----

###### Level 26 → Level 27

```sh
bandit26@bandit:~$ ls -l
total 12
-rwsr-x--- 1 bandit27 bandit26 7296 Oct 16  2018 bandit27-do
-rw-r----- 1 bandit26 bandit26  258 Oct 16  2018 text.txt
bandit26@bandit:~$ 
```

```sh
bandit26@bandit:~$ cat text.txt 
  _                     _ _ _   ___   __  
 | |                   | (_) | |__ \ / /  
 | |__   __ _ _ __   __| |_| |_   ) / /_  
 | '_ \ / _` | '_ \ / _` | | __| / / '_ \ 
 | |_) | (_| | | | | (_| | | |_ / /| (_) |
 |_.__/ \__,_|_| |_|\__,_|_|\__|____\___/ 
bandit26@bandit:~$ 
```

```sh
bandit26@bandit:~$ file bandit27-do 
bandit27-do: setuid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=8e941f24b8c5cd0af67b22b724c57e1ab92a92a1, not stripped
bandit26@bandit:~$ 
```

```sh
bandit26@bandit:~$ ./bandit27-do id
uid=11026(bandit26) gid=11026(bandit26) euid=11027(bandit27) groups=11026(bandit26)
bandit26@bandit:~$ 
```

```sh
bandit26@bandit:~$ ./bandit27-do whoami
bandit27
bandit26@bandit:~$ 
```

```sh
bandit26@bandit:/tmp/level27unlocker$ cat steal.sh 
cat /etc/bandit_pass/bandit27
bandit26@bandit:/tmp/level27unlocker$ 
```

```sh
bandit26@bandit:/tmp/level27unlocker$ chmod 777 steal.sh 
```

```sh
bandit26@bandit:~$ ./bandit27-do /tmp/level27unlocker/steal.sh
3ba3118a22e93127a4ed485be72ef5ea
bandit26@bandit:~$ 
```

----

###### Level 27 → Level 28

```sh
ctf@ctf-vm:~$ ssh bandit27@bandit.labs.overthewire.org -p 2220
bandit27@bandit.labs.overthewire.org's password: 3ba3118a22e93127a4ed485be72ef5ea
bandit27@bandit:~$ 
```

```sh
bandit27@bandit:~$ mkdir -p /tmp/kanishka101
```

```sh
bandit27@bandit:~$ cd /tmp/kanishka101
```

```sh
bandit27@bandit:/tmp/kanishka101$ git clone ssh://bandit27-git@localhost/home/bandit27-git/repo
Cloning into 'repo'...
Could not create directory '/home/bandit27/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit27/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit27-git@localhost's password: 3ba3118a22e93127a4ed485be72ef5ea
remote: Counting objects: 3, done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (3/3), done.
bandit27@bandit:/tmp/kanishka101$ 
```

```sh
bandit27@bandit:/tmp/kanishka101$ ls -l
total 4
drwxr-sr-x 3 bandit27 root 4096 Dec 11 09:58 repo
bandit27@bandit:/tmp/kanishka101$ 
```

```sh
bandit27@bandit:/tmp/kanishka101$ cd repo/
bandit27@bandit:/tmp/kanishka101/repo$ ls -l
total 4
-rw-r--r-- 1 bandit27 root 68 Dec 11 09:58 README
bandit27@bandit:/tmp/kanishka101/repo$ cat README 
The password to the next level is: 0ef186ac70e04ea33b4c1853d2526fa2
bandit27@bandit:/tmp/kanishka101/repo$ 
```

----

###### Level 28 → Level 29

```sh
ctf@ctf-vm:~$ ssh bandit28@bandit.labs.overthewire.org -p 2220
bandit28@bandit.labs.overthewire.org's password: 0ef186ac70e04ea33b4c1853d2526fa2
bandit28@bandit:~$ 
```

```sh
bandit28@bandit:~$ mkdir -p /tmp/kanishka102
```

```sh
bandit28@bandit:~$ cd /tmp/kanishka102
bandit28@bandit:/tmp/kanishka102$ 
```

```sh
bandit28@bandit:/tmp/kanishka102$ git clone ssh://bandit28-git@localhost/home/bandit28-git/repo
Cloning into 'repo'...
Could not create directory '/home/bandit28/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit28/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit28-git@localhost's password: 0ef186ac70e04ea33b4c1853d2526fa2
remote: Counting objects: 9, done.
remote: Compressing objects: 100% (6/6), done.
remote: Total 9 (delta 2), reused 0 (delta 0)
Receiving objects: 100% (9/9), done.
Resolving deltas: 100% (2/2), done.
bandit28@bandit:/tmp/kanishka102$ 
```

```sh
bandit28@bandit:/tmp/kanishka102$ cd repo/
bandit28@bandit:/tmp/kanishka102/repo$ ls -l
total 4
-rw-r--r-- 1 bandit28 root 111 Dec 11 10:03 README.md
bandit28@bandit:/tmp/kanishka102/repo$ cat README.md 
# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: xxxxxxxxxx

bandit28@bandit:/tmp/kanishka102/repo$ 
```

```sh
bandit28@bandit:/tmp/kanishka102/repo$ git log
commit 073c27c130e6ee407e12faad1dd3848a110c4f95
Author: Morla Porla <morla@overthewire.org>
Date:   Tue Oct 16 14:00:39 2018 +0200

    fix info leak

commit 186a1038cc54d1358d42d468cdc8e3cc28a93fcb
Author: Morla Porla <morla@overthewire.org>
Date:   Tue Oct 16 14:00:39 2018 +0200

    add missing data

commit b67405defc6ef44210c53345fc953e6a21338cc7
Author: Ben Dover <noone@overthewire.org>
Date:   Tue Oct 16 14:00:39 2018 +0200

    initial commit of README.md
bandit28@bandit:/tmp/kanishka102/repo$ 
```

```sh
bandit28@bandit:/tmp/kanishka102/repo$ git checkout 186a1038cc54d1358d42d468cdc8e3cc28a93fcb
Previous HEAD position was b67405d... initial commit of README.md
HEAD is now at 186a103... add missing data
bandit28@bandit:/tmp/kanishka102/repo$ 
```

```sh
bandit28@bandit:/tmp/kanishka102/repo$ cat README.md 
# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: bbc96594b4e001778eee9975372716b2

bandit28@bandit:/tmp/kanishka102/repo$ 
```

----

###### Level 29 → Level 30

```sh
ctf@ctf-vm:~$ ssh bandit29@bandit.labs.overthewire.org -p 2220
bandit29@bandit.labs.overthewire.org's password: bbc96594b4e001778eee9975372716b2
bandit29@bandit:~$ 
```

```sh
bandit29@bandit:~$ mkdir -p /tmp/kanishka103
```

```sh
bandit29@bandit:~$ cd /tmp/kanishka103
bandit29@bandit:/tmp/kanishka103$ 
```

```sh
bandit29@bandit:/tmp/kanishka103$ git clone ssh://bandit29-git@localhost/home/bandit29-git/repo
Cloning into 'repo'...
Could not create directory '/home/bandit29/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit29/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit29-git@localhost's password: bbc96594b4e001778eee9975372716b2
remote: Counting objects: 16, done.
remote: Compressing objects: 100% (11/11), done.
remote: Total 16 (delta 2), reused 0 (delta 0)
Receiving objects: 100% (16/16), done.
Resolving deltas: 100% (2/2), done.
bandit29@bandit:/tmp/kanishka103$ 
```

```sh
bandit29@bandit:/tmp/kanishka103$ ls -l
total 4
drwxr-sr-x 3 bandit29 root 4096 Dec 11 10:08 repo
bandit29@bandit:/tmp/kanishka103$ cd repo/
bandit29@bandit:/tmp/kanishka103/repo$ ls -l
total 4
-rw-r--r-- 1 bandit29 root 131 Dec 11 10:08 README.md
bandit29@bandit:/tmp/kanishka103/repo$ cat README.md 
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: <no passwords in production!>

bandit29@bandit:/tmp/kanishka103/repo$ 
```

```sh
bandit29@bandit:/tmp/kanishka103/repo$ git log 
commit 84abedc104bbc0c65cb9eb74eb1d3057753e70f8
Author: Ben Dover <noone@overthewire.org>
Date:   Tue Oct 16 14:00:41 2018 +0200

    fix username

commit 9b19e7d8c1aadf4edcc5b15ba8107329ad6c5650
Author: Ben Dover <noone@overthewire.org>
Date:   Tue Oct 16 14:00:41 2018 +0200

    initial commit of README.md
bandit29@bandit:/tmp/kanishka103/repo$ 
```

```sh
bandit29@bandit:/tmp/kanishka103/repo$ git log -p
commit 9b19e7d8c1aadf4edcc5b15ba8107329ad6c5650
Author: Ben Dover <noone@overthewire.org>
Date:   Tue Oct 16 14:00:41 2018 +0200

    initial commit of README.md

diff --git a/README.md b/README.md
new file mode 100644
index 0000000..2da2f39
--- /dev/null
+++ b/README.md
@@ -0,0 +1,8 @@
+# Bandit Notes
+Some notes for bandit30 of bandit.
+
+## credentials
+
+- username: bandit29
+- password: <no passwords in production!>
+
bandit29@bandit:/tmp/kanishka103/repo$ 
```

```sh
bandit29@bandit:/tmp/kanishka103/repo$ git branch
* (HEAD detached at 9b19e7d)
  master
bandit29@bandit:/tmp/kanishka103/repo$ 
```

```sh
bandit29@bandit:/tmp/kanishka103/repo$ git branch --all
* (HEAD detached at 9b19e7d)
  master
  remotes/origin/HEAD -> origin/master
  remotes/origin/dev
  remotes/origin/master
  remotes/origin/sploits-dev
bandit29@bandit:/tmp/kanishka103/repo$ 
bandit29@bandit:/tmp/kanishka103/repo$ git checkout dev
Previous HEAD position was 9b19e7d... initial commit of README.md
Branch dev set up to track remote branch dev from origin.
Switched to a new branch 'dev'
bandit29@bandit:/tmp/kanishka103/repo$ 
```

```sh
bandit29@bandit:/tmp/kanishka103/repo$ git log -p
commit 33ce2e95d9c5d6fb0a40e5ee9a2926903646b4e3
Author: Morla Porla <morla@overthewire.org>
Date:   Tue Oct 16 14:00:41 2018 +0200

    add data needed for development

diff --git a/README.md b/README.md
index 1af21d3..39b87a8 100644
--- a/README.md
+++ b/README.md
@@ -4,5 +4,5 @@ Some notes for bandit30 of bandit.
 ## credentials
 
 - username: bandit30
-- password: <no passwords in production!>
+- password: 5b90576bedb2cc04c86a9e924ce42faf
 

commit a8af722fccd4206fc3780bd3ede35b2c03886d9b
Author: Ben Dover <noone@overthewire.org>
Date:   Tue Oct 16 14:00:41 2018 +0200

    add gif2ascii

diff --git a/code/gif2ascii.py b/code/gif2ascii.py
new file mode 100644
index 0000000..8b13789
--- /dev/null
+++ b/code/gif2ascii.py
@@ -0,0 +1 @@
+

commit 84abedc104bbc0c65cb9eb74eb1d3057753e70f8
Author: Ben Dover <noone@overthewire.org>
Date:   Tue Oct 16 14:00:41 2018 +0200

    fix username

diff --git a/README.md b/README.md
index 2da2f39..1af21d3 100644
--- a/README.md
+++ b/README.md
@@ -3,6 +3,6 @@ Some notes for bandit30 of bandit.
 
 ## credentials
 
-- username: bandit29
+- username: bandit30
 - password: <no passwords in production!>
 

commit 9b19e7d8c1aadf4edcc5b15ba8107329ad6c5650
Author: Ben Dover <noone@overthewire.org>
Date:   Tue Oct 16 14:00:41 2018 +0200

    initial commit of README.md

diff --git a/README.md b/README.md
new file mode 100644
index 0000000..2da2f39
--- /dev/null
+++ b/README.md
@@ -0,0 +1,8 @@
+# Bandit Notes
+Some notes for bandit30 of bandit.
+
+## credentials
+
+- username: bandit29
+- password: <no passwords in production!>
+
bandit29@bandit:/tmp/kanishka103/repo$ 
```

```sh
bandit29@bandit:/tmp/kanishka103/repo$ cat README.md 
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: 5b90576bedb2cc04c86a9e924ce42faf

bandit29@bandit:/tmp/kanishka103/repo$ 
```

----

###### Level 30 → Level 31

```sh
ctf@ctf-vm:~$ ssh bandit30@bandit.labs.overthewire.org -p 2220
bandit30@bandit.labs.overthewire.org's password: 5b90576bedb2cc04c86a9e924ce42faf
bandit30@bandit:~$ 
```

```sh
bandit30@bandit:~$ mkdir -p /tmp/kanishka104
```

```sh
bandit30@bandit:~$ cd /tmp/kanishka104
bandit30@bandit:/tmp/kanishka104$ 
```

```sh
bandit30@bandit:/tmp/kanishka104$ git clone ssh://bandit30-git@localhost/home/bandit30-git/repo
Cloning into 'repo'...
Could not create directory '/home/bandit30/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit30/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit30-git@localhost's password: 
remote: Counting objects: 4, done.
remote: Total 4 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (4/4), done.
bandit30@bandit:/tmp/kanishka104$ 
```

```sh
bandit30@bandit:/tmp/kanishka104$ ls -l
total 4
drwxr-sr-x 3 bandit30 root 4096 Dec 11 10:22 repo
bandit30@bandit:/tmp/kanishka104$ cd repo/
bandit30@bandit:/tmp/kanishka104/repo$ ls -l
total 4
-rw-r--r-- 1 bandit30 root 30 Dec 11 10:22 README.md
bandit30@bandit:/tmp/kanishka104/repo$ cat README.md 
just an epmty file... muahaha
bandit30@bandit:/tmp/kanishka104/repo$ 
```

```sh
bandit30@bandit:/tmp/kanishka104/repo$ git log -p
commit 3aa4c239f729b07deb99a52f125893e162daac9e
Author: Ben Dover <noone@overthewire.org>
Date:   Tue Oct 16 14:00:44 2018 +0200

    initial commit of README.md

diff --git a/README.md b/README.md
new file mode 100644
index 0000000..029ba42
--- /dev/null
+++ b/README.md
@@ -0,0 +1 @@
+just an epmty file... muahaha
bandit30@bandit:/tmp/kanishka104/repo$ 
```

```sh
bandit30@bandit:/tmp/kanishka104/repo$ git branch
* master
bandit30@bandit:/tmp/kanishka104/repo$ 
```

```sh
bandit30@bandit:/tmp/kanishka104/repo$ git branch --all
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master
bandit30@bandit:/tmp/kanishka104/repo$ 
```

```sh
bandit30@bandit:/tmp/kanishka104/repo$ ls -lah
total 16K
drwxr-sr-x 3 bandit30 root 4.0K Dec 11 10:22 .
drwxr-sr-x 3 bandit30 root 4.0K Dec 11 10:21 ..
drwxr-sr-x 8 bandit30 root 4.0K Dec 11 10:22 .git
-rw-r--r-- 1 bandit30 root   30 Dec 11 10:22 README.md
bandit30@bandit:/tmp/kanishka104/repo$ 
```

```sh
bandit30@bandit:/tmp/kanishka104/repo$ cd .git/
bandit30@bandit:/tmp/kanishka104/repo/.git$ ls -lah
total 52K
drwxr-sr-x 8 bandit30 root 4.0K Dec 11 10:22 .
drwxr-sr-x 3 bandit30 root 4.0K Dec 11 10:22 ..
drwxr-sr-x 2 bandit30 root 4.0K Dec 11 10:21 branches
-rw-r--r-- 1 bandit30 root  276 Dec 11 10:22 config
-rw-r--r-- 1 bandit30 root   73 Dec 11 10:21 description
-rw-r--r-- 1 bandit30 root   23 Dec 11 10:22 HEAD
drwxr-sr-x 2 bandit30 root 4.0K Dec 11 10:21 hooks
-rw-r--r-- 1 bandit30 root  137 Dec 11 10:22 index
drwxr-sr-x 2 bandit30 root 4.0K Dec 11 10:21 info
drwxr-sr-x 3 bandit30 root 4.0K Dec 11 10:22 logs
drwxr-sr-x 4 bandit30 root 4.0K Dec 11 10:21 objects
-rw-r--r-- 1 bandit30 root  165 Dec 11 10:22 packed-refs
drwxr-sr-x 5 bandit30 root 4.0K Dec 11 10:22 refs
bandit30@bandit:/tmp/kanishka104/repo/.git$ 
```

```sh
bandit30@bandit:/tmp/kanishka104/repo/.git$ cat HEAD 
ref: refs/heads/master
bandit30@bandit:/tmp/kanishka104/repo/.git$ 
```

```sh
bandit30@bandit:/tmp/kanishka104/repo/.git$ cat packed-refs 
# pack-refs with: peeled fully-peeled 
3aa4c239f729b07deb99a52f125893e162daac9e refs/remotes/origin/master
f17132340e8ee6c159e0a4a6bc6f80e1da3b1aea refs/tags/secret
bandit30@bandit:/tmp/kanishka104/repo/.git$ 
```

```sh
bandit30@bandit:/tmp/kanishka104/repo/.git$ git show secret
47e603bb428404d265f59c42920d81e5
bandit30@bandit:/tmp/kanishka104/repo/.git$ 
```

- [A Hacker's Guide to Git](https://wildlyinaccurate.com/a-hackers-guide-to-git/)

----

###### Level 31 → Level 32

```sh
ctf@ctf-vm:~$ ssh bandit31@bandit.labs.overthewire.org -p 2220
bandit31@bandit.labs.overthewire.org's password: 47e603bb428404d265f59c42920d81e5
bandit31@bandit:~$ 
```

```sh
bandit31@bandit:~$ mkdir -p /tmp/kanishka105
```

```sh
bandit31@bandit:~$ cd /tmp/kanishka105
bandit31@bandit:/tmp/kanishka105$ 
```

```sh
bandit31@bandit:/tmp/kanishka105$ git clone ssh://bandit31-git@localhost/home/bandit31-git/repo
Cloning into 'repo'...
Could not create directory '/home/bandit31/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit31/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit31-git@localhost's password: 47e603bb428404d265f59c42920d81e5
remote: Counting objects: 4, done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 4 (delta 0), reused 0 (delta 0)
Receiving objects: 100% (4/4), done.
bandit31@bandit:/tmp/kanishka105$ 
```

```sh
bandit31@bandit:/tmp/kanishka105$ ls -l
total 4
drwxr-sr-x 3 bandit31 root 4096 Dec 11 10:38 repo
bandit31@bandit:/tmp/kanishka105$ 
```

```sh
bandit31@bandit:/tmp/kanishka105$ cd repo/
bandit31@bandit:/tmp/kanishka105/repo$ ls -l
total 4
-rw-r--r-- 1 bandit31 root 147 Dec 11 10:38 README.md
bandit31@bandit:/tmp/kanishka105/repo$ cat README.md 
This time your task is to push a file to the remote repository.

Details:
    File name: key.txt
    Content: 'May I come in?'
    Branch: master

bandit31@bandit:/tmp/kanishka105/repo$ 
```

```sh
bandit31@bandit:/tmp/kanishka105/repo$ echo "May I come in?" > key.txt
```

```sh
bandit31@bandit:/tmp/kanishka105/repo$ git status 
On branch master
Your branch is up-to-date with 'origin/master'.
nothing to commit, working tree clean
bandit31@bandit:/tmp/kanishka105/repo$
```

```sh
bandit31@bandit:/tmp/kanishka105/repo$ git add key.txt 
The following paths are ignored by one of your .gitignore files:
key.txt
Use -f if you really want to add them.
bandit31@bandit:/tmp/kanishka105/repo$ 
```

```sh
bandit31@bandit:/tmp/kanishka105/repo$ ls -lah
total 24K
drwxr-sr-x 3 bandit31 root 4.0K Dec 11 10:44 .
drwxr-sr-x 3 bandit31 root 4.0K Dec 11 10:38 ..
drwxr-sr-x 8 bandit31 root 4.0K Dec 11 10:44 .git
-rw-r--r-- 1 bandit31 root    6 Dec 11 10:38 .gitignore
-rw-r--r-- 1 bandit31 root   15 Dec 11 10:44 key.txt
-rw-r--r-- 1 bandit31 root  147 Dec 11 10:38 README.md
bandit31@bandit:/tmp/kanishka105/repo$ 
```

```sh
bandit31@bandit:/tmp/kanishka105/repo$ cat .gitignore 
*.txt
bandit31@bandit:/tmp/kanishka105/repo$ 
```

```sh
bandit31@bandit:/tmp/kanishka105/repo$ git add key.txt -f
bandit31@bandit:/tmp/kanishka105/repo$ git commit -m "adding key.txt"
[master eaf2c6e] adding key.txt
 1 file changed, 1 insertion(+)
 create mode 100644 key.txt
bandit31@bandit:/tmp/kanishka105/repo$ git push 
Could not create directory '/home/bandit31/.ssh'.
The authenticity of host 'localhost (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:98UL0ZWr85496EtCRkKlo20X3OPnyPSB5tB5RPbhczc.
Are you sure you want to continue connecting (yes/no)? yes
Failed to add the host to the list of known hosts (/home/bandit31/.ssh/known_hosts).
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit31-git@localhost's password: 47e603bb428404d265f59c42920d81e5
Counting objects: 3, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 326 bytes | 0 bytes/s, done.
Total 3 (delta 0), reused 0 (delta 0)
remote: ### Attempting to validate files... ####
remote: 
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote: 
remote: Well done! Here is the password for the next level:
remote: 56a9bf19c63d650ce78e6ec0354ee45e
remote: 
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote: 
To ssh://localhost/home/bandit31-git/repo
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'ssh://bandit31-git@localhost/home/bandit31-git/repo'
bandit31@bandit:/tmp/kanishka105/repo$ 
```

----

###### Level 32 → Level 33

```sh
ctf@ctf-vm:~$ ssh bandit32@bandit.labs.overthewire.org -p 2220
This is a OverTheWire game server. More information on http://www.overthewire.org/wargames

bandit32@bandit.labs.overthewire.org's password: 56a9bf19c63d650ce78e6ec0354ee45e
Linux bandit 4.18.12 x86_64 GNU/Linux
               
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

    * pwndbg (https://github.com/pwndbg/pwndbg) in /usr/local/pwndbg/
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

WELCOME TO THE UPPERCASE SHELL
>> ls
sh: 1: LS: not found
>> id
sh: 1: ID: not found
>> $0
$ pwd
/home/bandit32
$ ls -lah
total 28K
drwxr-xr-x  2 root     root     4.0K Oct 16  2018 .
drwxr-xr-x 41 root     root     4.0K Oct 16  2018 ..
-rw-r--r--  1 root     root      220 May 15  2017 .bash_logout
-rw-r--r--  1 root     root     3.5K May 15  2017 .bashrc
-rw-r--r--  1 root     root      675 May 15  2017 .profile
-rwsr-x---  1 bandit33 bandit32 7.4K Oct 16  2018 uppershell
$ file uppershell
uppershell: setuid ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=e6a8ed571599ce2bfa8b77145dbfc4eb933c1477, not stripped
$ id
uid=11033(bandit33) gid=11032(bandit32) groups=11032(bandit32)
$ cat /etc/bandit_pass/bandit33
c9c3199ddf4121b10cf581a98d51caee
$ 
```

- [What is the meaning of $0 in the Bash shell](https://unix.stackexchange.com/questions/280454/what-is-the-meaning-of-0-in-the-bash-shell)

----

EOF