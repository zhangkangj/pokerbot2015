import sys
import re



def lose(string, line):
  return (string +' (0)' in line) or string +'2 (0)' in line or string +'3 (0)' in line or string +'4 (0)' in line or string +'5 (0)' in line or string +'6 (0)' in line

files = sys.argv[1:]
print files[0], len(files)
files = [file for file in files if 'match' in file]
num_hand = 0
num_2p = 0
nash_win_2p = 0
nash_win = 0
nash_out = 0
stack = 0
winning = 0
mixed_win = 0
for file in files:
  num_hand += 1
  f= open(file,'r')
  lines = f.readlines()
  winline = lines[-2]
  if 'NASH' in winline:
    nash_win += 1
  elif 'MIXED' in winline:
    mixed_win += 1
  for line in lines:
    if 'Hand' in line and '(0)' in line:
      if lose('RANDOM', line):
        a = re.search(r'NASH[23456]* \((\d+)\)', line)
        stack += int(a.group(1))
        winning += -int(a.group(1))
        num_2p += 1
        if 'NASH' in winline:
          nash_win_2p += 1    
          winning += 600
      if lose('NASH', line):
        nash_out += 1
      print line
      break
  for line in lines:
    if 'Illegal' in line:
      print 'illegal actions in',file
  print lines[-2]
    
print 'report:'
print num_hand, 'games',
print 'nash won', nash_win
print 'mixed won', mixed_win
print 'random won', num_hand - nash_win - mixed_win
print 
print '2p game:', num_2p
print 'nash won', nash_win_2p, 'mixed won', num_2p - nash_win_2p
print 'nash starting stack', stack/num_2p, 'average winning', winning/num_2p
print
print 'nash:random', nash_win - nash_win_2p, num_hand - num_2p - nash_out - nash_win + nash_win_2p
print 'mixed:random', mixed_win - num_2p + nash_win_2p, nash_out - (mixed_win - num_2p + nash_win_2p)
