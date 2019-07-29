#### 5. Residue Metadata II

----

- You are given access to a developer's machine. While working on an application, the developer added a flag to one of the dev directories but later deleted it. Some or all of this activity might have been captured in the source code repository used in the organization.
- Objective: Recover the flag value!

----

```sh
root@attackdefense:~# ls -l
total 8
drwxr-xr-x 11 root root 4096 May 16 17:53 Pico
drwxr-xr-x  2 root root 4096 May 16 18:21 secret
root@attackdefense:~#
```

```sh
root@attackdefense:~# cat secret/flag.txt

root@attackdefense:~#
```

```sh
root@attackdefense:~# git log
commit 30c2efd241851b5186b5d81cbe22274b7f17baab (HEAD -> master)
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 17:54:03 2019 +0000

    Removed unecessary files

commit 899e2ba43e045c51b92748dbc621ecf00f9ad674
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 17:51:13 2019 +0000

    Added file

commit 6eb96c420bbda2493b759d7ed6d72a7c38201cf2
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 17:50:32 2019 +0000

    Added Pico web app
root@attackdefense:~#
```

```sh
root@attackdefense:~# git show --stat 30c2efd241851b5186b5d81cbe22274b7f17baab
commit 30c2efd241851b5186b5d81cbe22274b7f17baab (HEAD -> master)
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 17:54:03 2019 +0000

    Removed unecessary files

 Pico/CHANGELOG.md    | 550 --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
---
 Pico/CONTRIBUTING.md | 209 -------------------------------------------------------------------------
 Pico/LICENSE.md      |  22 --------
 Pico/README.md       | 233 ---------------------------------------------------------------------------------
 4 files changed, 1014 deletions(-)
root@attackdefense:~#
```

```sh
root@attackdefense:~# git show --stat 899e2ba43e045c51b92748dbc621ecf00f9ad674
commit 899e2ba43e045c51b92748dbc621ecf00f9ad674
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 17:51:13 2019 +0000

    Added file

 secret/flag.txt | 1 +
 1 file changed, 1 insertion(+)
root@attackdefense:~#
```

```sh
root@attackdefense:~# git branch
  dev
* master
root@attackdefense:~#
```

```sh
root@attackdefense:~# git checkout dev
Switched to branch 'dev'
root@attackdefense:~#
```

```sh
root@attackdefense:~# git branch
* dev
  master
root@attackdefense:~#
```

```sh
root@attackdefense:~# git log
commit 8d779745404963116e7277c7237d5a3acbcdc5e7 (HEAD -> dev)
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 18:23:57 2019 +0000

    Updated flag

commit 1fb45721b4ab34d606f6e74201e6e9424662cea9
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 17:53:34 2019 +0000

    Removed unecessary files

commit cc20362c31e3c3f9e8bad325a3eeb7650502555e
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 17:52:29 2019 +0000

    updated file

commit 899e2ba43e045c51b92748dbc621ecf00f9ad674
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 17:51:13 2019 +0000

    Added file

commit 6eb96c420bbda2493b759d7ed6d72a7c38201cf2
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 17:50:32 2019 +0000

    Added Pico web app
root@attackdefense:~# 
```

```sh
root@attackdefense:~# cat secret/flag.txt

root@attackdefense:~#
```

```sh
root@attackdefense:~# git show --stat cc20362c31e3c3f9e8bad325a3eeb7650502555e
commit cc20362c31e3c3f9e8bad325a3eeb7650502555e (HEAD)
Author: webdev <webdev@xyz.com>
Date:   Thu May 16 17:52:29 2019 +0000

    updated file

 secret/flag.txt | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
root@attackdefense:~#
```

```sh
root@attackdefense:~# git checkout cc20362c31e3c3f9e8bad325a3eeb7650502555e
Previous HEAD position was 8d77974 Updated flag
HEAD is now at cc20362 updated file
root@attackdefense:~#
root@attackdefense:~# cat secret/flag.txt
38e14f1e843a372c07f721d3497f5d37
root@attackdefense:~#
```

----

EOF