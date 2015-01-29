import sys

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

orig_file = sys.argv[1]
gen_file = sys.argv[2]

with open(orig_file) as f:
    orig_content = f.readlines()
    print str(orig_content)
    print str(len(orig_content))
    with open(gen_file, 'w') as f1:
      for i in range(len(orig_content)):
        # newline = str(i) + ": " orig_content[i]
        f1.write('#%i: %s' % (i, orig_content[i]))
