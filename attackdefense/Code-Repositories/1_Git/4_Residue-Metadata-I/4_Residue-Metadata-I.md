#### 4. Residue Metadata I

----

- You are given access to a developer's machine. While working on an application, the developer added a flag to one of the dev directories but later deleted it. Some or all of this activity might have been captured in the source code repository used in the organization.
- Objective: Recover the flag value!

----

```sh
root@attackdefense:~# ls -lah
total 36K
drwx------ 1 root root 4.0K May 16 13:41 .
drwxr-xr-x 1 root root 4.0K Jul 29 03:17 ..
-rw-r--r-- 1 root root 3.1K Apr  9  2018 .bashrc
drwxr-xr-x 8 root root 4.0K May 16 13:30 .git
-rw-r--r-- 1 root root   46 May 16 13:26 .gitconfig
-rw-r--r-- 1 root root   38 May 16 13:34 .gitignore
-rw-r--r-- 1 root root  148 Aug 17  2015 .profile
drwxr-xr-x 6 root root 4.0K May 16 13:30 bludit
drwxr-xr-x 2 root root 4.0K May 16 13:27 secret
root@attackdefense:~#
```

```sh
root@attackdefense:~# cd secret/
root@attackdefense:~/secret# ls -lah
total 12K
drwxr-xr-x 2 root root 4.0K May 16 13:27 .
drwx------ 1 root root 4.0K May 16 13:41 ..
-rw-r--r-- 1 root root    1 May 16 13:29 flag.txt
root@attackdefense:~/secret# cat flag.txt

root@attackdefense:~/secret#
```

```sh
root@attackdefense:~# git log
commit afca042540e9b3d864e400a2c9b5590641b1bee8 (HEAD -> master)
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 13:30:41 2019 +0000

    Added README

commit c89c59294524eda318e5b6c08190819e271960a1
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 13:30:09 2019 +0000

    Updated flag.txt

commit 30a006e6e3267f1cd8874fef2b3054fffb2f9ac9
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 13:29:22 2019 +0000

    Removed unecessary files

commit ff4b158c2941d90321fcb09567c59a06d21fad5a
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 13:28:45 2019 +0000

    Added Web application files

commit 8064bcf3410680044e41f293ec5dbf76a5bc5916
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 13:27:47 2019 +0000

    Initial Commit
root@attackdefense:~#
```

```sh
root@attackdefense:~# git show --stat c89c59294524eda318e5b6c08190819e271960a1
commit c89c59294524eda318e5b6c08190819e271960a1
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 13:30:09 2019 +0000

    Updated flag.txt

 secret/flag.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
root@attackdefense:~#
```

```sh
root@attackdefense:~# git checkout 30a006e6e3267f1cd8874fef2b3054fffb2f9ac9
Note: checking out '30a006e6e3267f1cd8874fef2b3054fffb2f9ac9'.

You are in 'detached HEAD' state. You can look around, make experimental
changes and commit them, and you can discard any commits you make in this
state without impacting any branches by performing another checkout.

If you want to create a new branch to retain commits you create, you may
do so (now or later) by using -b with the checkout command again. Example:

  git checkout -b <new-branch-name>

HEAD is now at 30a006e Removed unecessary files
root@attackdefense:~#
```

```sh
root@attackdefense:~# cat secret/flag.txt
5e9da93befddb6bb5f5941f55b0b27af
root@attackdefense:~#
```

----

EOF