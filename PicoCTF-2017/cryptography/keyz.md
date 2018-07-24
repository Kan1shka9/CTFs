#### keyz

```sh
u64@vm:~/.ssh$ ssh-keygen -b 4096
Generating public/private rsa key pair.
Enter file in which to save the key (/home/u64/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/u64/.ssh/id_rsa.
Your public key has been saved in /home/u64/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:AxQpqtRhny/EaJZiIjvgRDR9CyHIygNzXddNHR3DSv0 u64@vm
The key's randomart image is:
+---[RSA 4096]----+
|++.o..+o.. o..+=.|
|+o+=oo..  . ...oo|
|=oo.O.+     . . .|
|=B.* * .     .  E|
|Oo= . . S        |
|+.   . . .       |
| .    .          |
|                 |
|                 |
+----[SHA256]-----+
u64@vm:~/.ssh$ 
```

```sh
u64@vm:~/.ssh$ cat id_rsa.pub 
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDHdKW0m/9QqoVB8b/sUqcwHHMwVi4hSX0/5uakjcX0Bihifu4NO/IiZE1z/xfpMT0awScCP98QlcWpVZEeg5xrbdLjhbti6j5JwGnXw3bO5hviwiYNZb9CEEKkaufzlpNsgUEGQNBsUKAVXhTscE4awReabr5f8d0EMt7ScvM5Xpmd5N1XGHLF1ATjmoUcDaYVqVqmrJQCoVh+4kI9RmheUCMDX7dPV+O6+Njt02b5/h47HYxk9VJK85olWCj5pYgi35d4m7gmysDeaWWuGAk8DHr3+dvEIaeUkohcHHrM4FkyvWe1cE/w0cDetPyEpOIVQ7GbjH1cSy6O/R0FmH82khN00lAyepJ3KQDbO6PaJwuVzVP+e4e9Bzyu6Zu2phzMPhDBTYhY9NXioLnATschuYBkv2yTcGb7TaTMXqZ7BBfRI2sf9U4Q7iTXRmIF08l04ubunZN5RBhKWvlTz2WYwnlwV1CxFsY22bcig7hrBQTP/O6QOg2r7dM1UoxJzLoZLfJo3hV/w2cmKLqU/OR+ZrTUg53XtZPdn50UkbUgEe2UgMDGYrN3YJFdv700OdHXsZ462noexUygKZiZcLio4VOa80YwUmUdk23ymHW5du7RgXH6c+CCV8uR1ghDaHOv5wq1sAp2Qe7beeU/TmJqITHHteocZp50PHhsxa0WTQ== u64@vm
u64@vm:~/.ssh$
```

```sh
kan1shka9@shell-web:~/.ssh$ echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABA
AACAQDHdKW0m/9QqoVB8b/sUqcwHHMwVi4hSX0/5uakjcX0Bihifu4NO/IiZE1z/xfp
MT0awScCP98QlcWpVZEeg5xrbdLjhbti6j5JwGnXw3bO5hviwiYNZb9CEEKkaufzlpN
sgUEGQNBsUKAVXhTscE4awReabr5f8d0EMt7ScvM5Xpmd5N1XGHLF1ATjmoUcDaYVqV
qmrJQCoVh+4kI9RmheUCMDX7dPV+O6+Njt02b5/h47HYxk9VJK85olWCj5pYgi35d4m
7gmysDeaWWuGAk8DHr3+dvEIaeUkohcHHrM4FkyvWe1cE/w0cDetPyEpOIVQ7GbjH1c
Sy6O/R0FmH82khN00lAyepJ3KQDbO6PaJwuVzVP+e4e9Bzyu6Zu2phzMPhDBTYhY9NX
ioLnATschuYBkv2yTcGb7TaTMXqZ7BBfRI2sf9U4Q7iTXRmIF08l04ubunZN5RBhKWv
lTz2WYwnlwV1CxFsY22bcig7hrBQTP/O6QOg2r7dM1UoxJzLoZLfJo3hV/w2cmKLqU/
OR+ZrTUg53XtZPdn50UkbUgEe2UgMDGYrN3YJFdv700OdHXsZ462noexUygKZiZcLio
4VOa80YwUmUdk23ymHW5du7RgXH6c+CCV8uR1ghDaHOv5wq1sAp2Qe7beeU/TmJqITH
HteocZp50PHhsxa0WTQ== u64@vm" >> ~/.ssh/authorized_keys            
kan1shka9@shell-web:~/.ssh$ 
```

```sh                                     
kan1shka9@shell-web:~/.ssh$ cat authorized_keys                    
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDHdKW0m/9QqoVB8b/sUqcwHHMwVi4
hSX0/5uakjcX0Bihifu4NO/IiZE1z/xfpMT0awScCP98QlcWpVZEeg5xrbdLjhbti6j
5JwGnXw3bO5hviwiYNZb9CEEKkaufzlpNsgUEGQNBsUKAVXhTscE4awReabr5f8d0EM
t7ScvM5Xpmd5N1XGHLF1ATjmoUcDaYVqVqmrJQCoVh+4kI9RmheUCMDX7dPV+O6+Njt
02b5/h47HYxk9VJK85olWCj5pYgi35d4m7gmysDeaWWuGAk8DHr3+dvEIaeUkohcHHr
M4FkyvWe1cE/w0cDetPyEpOIVQ7GbjH1cSy6O/R0FmH82khN00lAyepJ3KQDbO6PaJw
uVzVP+e4e9Bzyu6Zu2phzMPhDBTYhY9NXioLnATschuYBkv2yTcGb7TaTMXqZ7BBfRI
2sf9U4Q7iTXRmIF08l04ubunZN5RBhKWvlTz2WYwnlwV1CxFsY22bcig7hrBQTP/O6Q
Og2r7dM1UoxJzLoZLfJo3hV/w2cmKLqU/OR+ZrTUg53XtZPdn50UkbUgEe2UgMDGYrN
3YJFdv700OdHXsZ462noexUygKZiZcLio4VOa80YwUmUdk23ymHW5du7RgXH6c+CCV8
uR1ghDaHOv5wq1sAp2Qe7beeU/TmJqITHHteocZp50PHhsxa0WTQ== u64@vm      
kan1shka9@shell-web:~/.ssh$                                        
```

```sh
u64@vm:~$ ssh -i ~/.ssh/id_rsa kan1shka9@shell2017.picoctf.com
The authenticity of host 'shell2017.picoctf.com (35.153.110.19)' can't be established.
ECDSA key fingerprint is SHA256:ZIqVNC9hm15Z6mdDFCWC/H0+5MzSzXEhW3a+iHP1HM4.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'shell2017.picoctf.com,35.153.110.19' (ECDSA) to the list of known hosts.
Congratulations on setting up SSH key authentication!
Here is your flag: who_needs_pwords_anyways
kan1shka9@shell-web:~$ 
```