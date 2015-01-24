import numpy
import subprocess

low_card_lim_min = 0
low_card_lim_max = 0.5
low_card_lim_sample_size = 5
low_card_lim_paras = list(numpy.linspace(low_card_lim_min, low_card_lim_max, num=low_card_lim_sample_size))

high_card_lim_min = 0.5
high_card_lim_max = 1
high_card_lim_sample_size = 5
high_card_lim_paras = list(numpy.linspace(high_card_lim_min, high_card_lim_max, num=high_card_lim_sample_size))





for low_card_lim in low_card_lim_paras:
  for high_card_lim in high_card_lim_paras:
    f = open('massive_params.txt', 'w')
    f.write('%f, %f, ' %(low_card_lim, high_card_lim))
    f.close()
    p = subprocess.call("java -jar engine.jar", shell=True)
    print "subprocess call result: " + str(p)

# cmd = ["java -jar engine.jar", "", ""]
# p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
