#!/bin/python3
import sys

arg_pid = sys.argv[1]
arg_address = sys.argv[-1]

# virtual memory area
# http://books.gigatux.nl/mirror/kerneldevelopment/0672327201/ch14lev1sec2.html
class Vma:
 def __init__(self, map):
  parts = [x.strip() for x in map.split(' ')]
  min,max = parts[0].split('-')
  self.range = range(int(min, base=16), int(max, base=16))
  self.size = self.range.stop - self.range.start
  self.permission = parts[1]
  self.offset = parts[2]
  self.device = parts[3]
  self.inode = parts[4]
  self.path = parts[-1]

 def __str__(self):
  self_dict = vars(self)
  self_dict['range'] = f'({hex(self.range.start)}, {hex(self.range.stop)})'
  return str(self_dict)

def round(address):
 with open(f'/proc/{arg_pid}/maps') as f:
  for line in f:
   map_entry = Vma(line)
   if address in map_entry.range:
    return print(map_entry)
  print('{}')

def address_to_int(s):
 isHex = s[0:2].lower() == '0x'
 base = 16 if isHex else 10
 address = int(s, base=base)
 return address

def show_help():
 print('''Usage: ./find-mem.py PID MEMADDRESS
or ./find-mem.py PID to enter interactive mode''')

def main():
 args_count = len(sys.argv)
 if args_count == 1:
  show_help()
 else:
  isReplMode = len(sys.argv) == 2
  round_count = (sys.maxsize if isReplMode else 1)
  for i in range(round_count):
   input_address = input('address> ') if isReplMode else arg_address
   try:
    address = address_to_int(input_address)
   except ValueError:
    continue
   round(address)

main()
