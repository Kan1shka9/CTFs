for i in $(seq 0 15);do

curl -i -s -k  -X $'POST' \
    -H $'Host: 10.10.10.60' -H $'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0' -H $'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H $'Accept-Language: en-US,en;q=0.5' -H $'Accept-Encoding: gzip, deflate' -H $'Referer: https://10.10.10.60/index.php' -H $'Cookie: PHPSESSID=f3ee818d4bd987f6b62b88e71601414e; cookie_test=1529956217' -H $'DNT: 1' -H $'Connection: close' -H $'Upgrade-Insecure-Requests: 1' -H $'Content-Type: application/x-www-form-urlencoded' -H $'Content-Length: 121' \
    -b $'PHPSESSID=f3ee818d4bd987f6b62b88e71601414e; cookie_test=1529956217' \
    --data-binary $'__csrf_magic=sid%3A7e7ff1c3faf7cd9569fd1d6c15cfb2a519681d16%2C1529952617&usernamefld=test&passwordfld=testing&login=Login' \
    $'https://10.10.10.60/index.php'

echo $i
done
