#!/usr/bin/env python3
import sys


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
 arg_pid = sys.argv[1]
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
 print('''Usage:

./memfind.py PID ADDRESS
./memfind.py PID - to enter REPL mode

PID - process id
ADDRESS - memory address in hex or decimal form, e.g.: 0x7fffffffe168 or 140737488347496''')

def main():
 args_count = len(sys.argv)

 if args_count == 1 or sys.argv[1].strip() == '-h' or sys.argv[1].strip() == '--help':
  show_help()
 else:
  isReplMode = args_count == 2
  round_count = (sys.maxsize if isReplMode else 1)
  arg_address = sys.argv[-1]
  for i in range(round_count):
   input_address = input('address> ') if isReplMode else arg_address
   try:
    address = address_to_int(input_address)
   except ValueError:
    continue
   round(address)

main()
