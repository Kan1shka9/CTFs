#### Login

![](images/1.png)

![](images/2.png)

![](images/3.png)

![](images/4.png)

![](images/5.png)

![](images/6.png)

![](images/7.png)

![](images/8.png)

![](images/9.png)

```sh
cewl --verbose --depth=1 --min_word_length=4 --count --write=./cewl_result http://192.168.1.2/mutillidae/index.php?page=view-someones-blog.php
```

![](images/10.png)

```
less cewl_result
```

![](images/11.png)

```sh
cat cewl_result | sed 's/,/ /' | awk '{print $1}' > cewl_result_pruned
```

![](images/12.png)