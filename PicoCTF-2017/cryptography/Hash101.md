#### Hash101

###### Level 1

```sh
➜  ~ nc shell2017.picoctf.com 9661

Welcome to Hashes 101!

There are 4 Levels. Complete all and receive a prize!


-------- LEVEL 1: Text = just 1's and 0's --------
All text can be represented by numbers. To see how different letters translate to numbers, go to http://www.asciitable.com/

TO UNLOCK NEXT LEVEL, give me the ASCII representation of 011011000110111101110110011001010110110001111001

>lovely
Correct! Completed level 1
```

```sh
>>> hex(int('011011000110111101110110011001010110110001111001',2))[2:].decode('hex')
'lovely'
>>>
```

###### Level 2

```sh
------ LEVEL 2: Numbers can be base ANYTHING -----
Numbers can be represented many ways. A popular way to represent computer data is in base 16 or 'hex' since it lines up with bytes very well (2 hex characters = 8 binary bits). Other formats include base64, binary, and just regular base10 (decimal)! In a way, that ascii chart represents a system where all text can be seen as "base128" (not including the Extended ASCII codes)

TO UNLOCK NEXT LEVEL, give me the text you just decoded, lovely, as its hex equivalent, and then the decimal equivalent of that hex number ("foo" -> 666f6f -> 6713199)

hex>6c6f76656c79
Good job! 6c6f76656c79 to ASCII -> lovely is lovely
Now decimal
dec>119225983528057
Good job! 119225983528057 to Hex -> 6c6f76656c79 to ASCII -> lovely is lovely
Correct! Completed level 2
```

```sh
>>> 'lovely'.encode('hex')
'6c6f76656c79'
>>> int('6c6f76656c79',16)
119225983528057
>>>
```

###### Level 3

```sh
----------- LEVEL 3: Hashing Function ------------
A Hashing Function intakes any data of any size and irreversibly transforms it to a fixed length number. For example, a simple Hashing Function could be to add up the sum of all the values of all the bytes in the data and get the remainder after dividing by 16 (modulus 16)

TO UNLOCK NEXT LEVEL, give me a string that will result in a 1 after being transformed with the mentioned example hashing function

>helll
Correct! Completed level 3
```

```sh
>>> sum([ ord(c) for c in 'hello' ]) % 16
4
>>> sum([ ord(c) for c in 'helll' ]) % 16
1
>>>
```

###### Level 4

```sh
--------------- LEVEL 4: Real Hash ---------------
A real Hashing Function is used for many things. This can include checking to ensure a file has not been changed (its hash value would change if any part of it is changed). An important use of hashes is for storing passwords because a Hashing Function cannot be reversed to find the initial data. Therefore if someone steals the hashes, they must try many different inputs to see if they can "crack" it to find what password yields the same hash. Normally, this is too much work (if the password is long enough). But many times, people's passwords are easy to guess... Brute forcing this hash yourself is not a good idea, but there is a strong possibility that, if the password is weak, this hash has been cracked by someone before. Try looking for websites that have stored already cracked hashes.

TO CLAIM YOUR PRIZE, give me the string password that will result in this MD5 hash (MD5, like most hashes, are represented as hex digits):
3f4e535a671209f394817559372286f2

>d3b17
Correct! Completed level 4
You completed all 4 levels! Here is your prize: c3ee093f26ba147ccc451fd13c91ffce

➜  ~
```

![](images/101/1.png)