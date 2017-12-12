#### Rate Limit Implementation

```
http://192.168.1.22:8000/api/v1/trains/
```

- Header

```
Key : Content-Type
Value : application/json
```

```
Key : Accept
Value : application/json
```

- POST

```
{
	"PNR": "9875-4581-234"
}
```

![](images/4/1.png)

![](images/4/2.png)

![](images/4/3.png)

Issue ``10`` requests to the ``API`` end point with ``anonymous user`` (without ``Authorization header``) 

![](images/4/4.png)

```
Key : Authorization
Value : Bearer vYcJ7Y7WWRPahB7BDqwjJGMeoLvBl7
```

![](images/4/5.png)

![](images/4/6.png)

Issue ``20`` requests with ``authenticated user`` (with ``Authorization header``)

![](images/4/7.png)

[```HTTP Status 429```](https://httpstatuses.com/429)