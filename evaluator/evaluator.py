# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 01:36:27 2014

@author: zhk
"""

result = [0] * 32768
for x in range(1+0b1111111111111):
  bin_str = bin(x)[2:]
  bin_x = int(''.join(['000' + char for char in bin_str]), 2)
  index = (bin_x >> 31) + bin_x
  index = ((index >> 14) + index) & 0x0000000000007fff
  #index = x
  value = 0
  if '11111' in bin_str:
    value = len(bin_str) - bin_str.find('11111') - 3
  elif (bin_str.startswith('1') and bin_str.endswith('1111') and len(bin_str) == 13):
    value =  1
  if index >= 32768:
    print index, bin_str, bin_x
  result[index] = value
print ','.join([str(x) for x in result])

for n in range(1+0b1111111111111):
  rank_unique = int(''.join(['000' + x for x in bin(n)[2:]]), 2)
  rank_unique = ((rank_unique >> 3) | rank_unique)
  rank_unique = ((rank_unique >> 6) | rank_unique) & 0x000f000f000f000f
  rank_unique = ((rank_unique >> 12) | rank_unique)
  rank_unique = ((rank_unique >> 24) | rank_unique) & 0x000000000000ffff
  print rank_unique
  assert bin(rank_unique) == bin(n)

result = [0] * 4096
l = []
for i in range(4):
  for j in range(4):
    for k in range(4):
      temp = [0] * 4
      temp[i] += 5
      temp[j] += 1
      temp[k] += 1
      index = int('0b' + ''.join([bin(x)[2:].zfill(3) for x in temp]), 2)
      result[index] = (3-i)*3+1
      l.append(index)
print ','.join([str(x) for x in result])





#high card 7 choose 5
#pair 5 choose 4
#two pair, four of a kind 3 choose 1
#three of a kind 4 choose 2
#full house 2 


# high card
count = 463
result = [0] * 32768
for a in range(12, 5, -1):
  for b in range(a-1, 4, -1):
    for c in range(b-1, 3, -1):
      for d in range(c-1, 2, -1):
        for e in range(d-1, 1, -1):
          count -= 1
          for f in range(e-1, 0, -1):
            for g in range(f-1, -1, -1):
              x = (1<<a)|(1<<b)|(1<<c)|(1<<d)|(1<<e)|(1<<f)|(1<<g)
              bin_str = bin(x)[2:]
              bin_x = int(''.join(['000' + char for char in bin_str]), 2)
              index = (bin_x >> 31) + bin_x
              index = ((index >> 14) + index) & 0x0000000000007fff
              print count, index
              result[index] = count
print ','.join([str(x) for x in result])

#pair
result = [0] * 32768
for a in range(12, -1, -1):
  x = (1<<a)
  bin_str = bin(x)[2:]
  bin_x = int(''.join(['000' + char for char in bin_str]), 2)
  index = (bin_x >> 31) + bin_x
  index = ((index >> 14) + index) & 0x0000000000007fff
  result[index] = a * 462
count = 78
for a in range(12, 0, -1):
  for b in range(a-1, -1, -1):
    count -= 1
    x = (1<<a)|(1<<b)
    bin_str = bin(x)[2:]
    bin_x = int(''.join(['000' + char for char in bin_str]), 2)
    index = (bin_x >> 31) + bin_x
    index = ((index >> 14) + index) & 0x0000000000007fff
    print count, index
    result[index] = count + 1 + 462*13    
count = 78
for a in range(12, 1, -1):
  for b in range(a-1, 0, -1):
    count -= 1
    for c in range(b-1, -1, -1):
      x = (1<<a)|(1<<b)|(1<<c)
      bin_str = bin(x)[2:]
      bin_x = int(''.join(['000' + char for char in bin_str]), 2)
      index = (bin_x >> 31) + bin_x
      index = ((index >> 14) + index) & 0x0000000000007fff
      print count, index
      result[index] = count + 1 + 462*13    
print ','.join([str(x) for x in result])
