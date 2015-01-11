# -*- coding: utf-8 -*-
"""
Created on Sat Dec 27 01:36:27 2014

@author: zhk
"""

# high card: 7 choose 5 --> (1, 462)
# pair: 1 choose 1 + 5 choose 3 --> (1, 13*84)
# two pair: 2 choose 2 + 3 choose 1, 3 choose 2 + ?2 choose 1? -->(1092+1, 1092+1+78*13)
# three of a kind: 1 choose 1 + 4 choose 2 --> (1, 13*84)
# straight/straight flush: 7 choose 5, 6 choose 5, 5 choose 5 --> (1, 10)
# full house: 1,2 choose 1 + 1,2 choose 1 --> (1, 84*13)
# four of a kind: 1 choose 1 + (1-3) choose 1 --> (1, 84*13)


# flush table
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

def map_52_to_15(x):
  x = (x>>31) + x
  x = ((x>>14) + x) & 0x0000000000007fff
  return x

# class table
result = [0] * 32768
# 7, 6, 5 choose 5 --> (1, 462), for high card or flush
count = 462
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
              index = map_52_to_15(bin_x)
              assert result[index] == 0              
              result[index] = count + 1
count = 462
for a in range(12, 5, -1):
  for b in range(a-1, 4, -1):
    for c in range(b-1, 3, -1):
      for d in range(c-1, 2, -1):
        for e in range(d-1, 1, -1):
          count -= 1
          for f in range(e-1, 0, -1):
            x = (1<<a)|(1<<b)|(1<<c)|(1<<d)|(1<<e)|(1<<f)
            bin_str = bin(x)[2:]
            bin_x = int(''.join(['000' + char for char in bin_str]), 2)
            index = map_52_to_15(bin_x)
            assert result[index] == 0              
            result[index] = count + 1
count = 462
for a in range(12, 5, -1):
  for b in range(a-1, 4, -1):
    for c in range(b-1, 3, -1):
      for d in range(c-1, 2, -1):
        for e in range(d-1, 1, -1):
          count -= 1
          x = (1<<a)|(1<<b)|(1<<c)|(1<<d)|(1<<e)
          bin_str = bin(x)[2:]
          bin_x = int(''.join(['000' + char for char in bin_str]), 2)
          index = map_52_to_15(bin_x)
          assert result[index] == 0
          result[index] = count + 1

# 7 choose 5, 6 choose 5, 5 choose 5 --> (1, 10) + 462, for straight
for x in range(1+0b1111111111111):
  bin_str = bin(x)[2:]
  bin_x = int(''.join(['000' + char for char in bin_str]), 2)
  index = map_52_to_15(bin_x)
  if '11111' in bin_str:
    value = len(bin_str) - bin_str.find('11111') - 3
    result[index] = value + 5000
  elif (bin_str.startswith('1') and bin_str.endswith('1111') and len(bin_str) == 13):
    value =  1 + 5000
    result[index] = value

# 1 choose 1 --> (1, 13*84+1), for four of a kind and one pair
for a in range(12, -1, -1):
  x = (1<<a)
  bin_str = bin(x)[2:]
  bin_x = int(''.join(['000' + char for char in bin_str]), 2)
  index = (bin_x >> 31) + bin_x
  index = ((index >> 14) + index) & 0x0000000000007fff
  assert result[index] == 0
  result[index] = a * 84 + 1

# 2 choose 2 --> (1092+1, 1092+1+78*13), for two pair
count = 78
for a in range(12, 0, -1):
  for b in range(a-1, -1, -1):
    count -= 1
    x = (1<<a)|(1<<b)
    bin_str = bin(x)[2:]
    bin_x = int(''.join(['000' + char for char in bin_str]), 2)
    index = (bin_x >> 31) + bin_x
    index = ((index >> 14) + index) & 0x0000000000007fff
    assert result[index] == 0
    result[index] = count * 13 + 1 + 1092

# 3 choose 2 --> (1092+1, 1092+1+78*13) for two pair
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
      assert result[index] == 0
      result[index] = count * 13 + 1 + 1092

# 2 choose smaller 1
for a in range(0, 12):
  for b in range(a+1, 13):
    x = (1<<a)|(1<<b)
    bin_str = bin(x)[2:]
    bin_x = int(''.join(['000' + char for char in bin_str]), 2)
    index = (bin_x >> 31) + bin_x
    index = ((index >> 14) + index) & 0x0000000000007fff
    index = 0x7fff^index
    assert result[index] == 0    
    result[index] = map_52_to_15(1<<(a*4))
print ','.join([str(x) for x in result])


# kicker table
# 5 choose 3 --> (0, 83), for one pair
count = 84
for a in range(12, 5, -1):
  for b in range(a-1, 4, -1):
    for c in range(b-1, 3, -1):
      count -= 1
      for d in range(c-1, 2, -1):
        for e in range(d-1, 1, -1):
          x = (1<<a)|(1<<b)|(1<<c)|(1<<d)|(1<<e)
          bin_str = bin(x)[2:]
          bin_x = int(''.join(['000' + char for char in bin_str]), 2)
          index = (bin_x >> 31) + bin_x
          index = ((index >> 14) + index) & 0x0000000000007fff
          assert result[index] == 0
          result[index] = count

# 3 choose 1 --> (0, 10), for two pair (2,2,1,1,1)
for a in range(12, 1, -1):
  for b in range(a-1, 0, -1):
    for c in range(b-1, -1, -1):
      x = (1<<a)|(1<<b)|(1<<c)
      bin_str = bin(x)[2:]
      bin_x = int(''.join(['000' + char for char in bin_str]), 2)
      index = (bin_x >> 31) + bin_x
      index = ((index >> 14) + index) & 0x0000000000007fff
      assert result[index] == 0
      result[index] = a

# 4 choose 2 --> (0, 54), for three of a kind
count = 55
for a in range(12, 2, -1):
  for b in range(a-1, 1, -1):
    count -= 1
    for c in range(b-1, 0, -1):
      for d in range(c-1, -1, -1):
        x = (1<<a)|(1<<b)|(1<<c)|(1<<d)
        bin_str = bin(x)[2:]
        bin_x = int(''.join(['000' + char for char in bin_str]), 2)
        index = (bin_x >> 31) + bin_x
        index = ((index >> 14) + index) & 0x0000000000007fff
        assert result[index] == 0
        result[index] = count

# 1 choose 1 --> (0, 12), for full house and three of a kind and two pair (2,2,2,1)
for a in range(12, -1, -1):
  x = (1<<a)
  bin_str = bin(x)[2:]
  bin_x = int(''.join(['000' + char for char in bin_str]), 2)
  index = (bin_x >> 31) + bin_x
  index = ((index >> 14) + index) & 0x0000000000007fff
  assert result[index] == 0
  result[index] = a
  
# 2 choose 1 --> (0, 12), for full house and three of a kind
for a in range(12, 0, -1):
  for b in range(a-1, -1, -1):
    x = (1<<a)|(1<<b)
    bin_str = bin(x)[2:]
    bin_x = int(''.join(['000' + char for char in bin_str]), 2)
    index = (bin_x >> 31) + bin_x
    index = ((index >> 14) + index) & 0x0000000000007fff
    assert result[index] == 0
    result[index] = a

# 3 choose smaller 1
for a in range(0, 12):
  for b in range(a+1, 13):
    for c in range(b+1, 13):
      x = (1<<a)|(1<<b)|(1<<c)
      bin_str = bin(x)[2:]
      bin_x = int(''.join(['000' + char for char in bin_str]), 2)
      index = (bin_x >> 31) + bin_x
      index = ((index >> 14) + index) & 0x0000000000007fff
      index = 0x7fff^index
      assert result[index] == 0    
      result[index] = map_52_to_15(1<<(a*4))
print ','.join([str(x) for x in result])