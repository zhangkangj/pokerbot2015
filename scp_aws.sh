#siemng add
#download nash data
#ask Kang for pokerbot.pem
#use with caution, it will override the old data files in data/cfr/aws_new
scp -i pokerbot.pem ubuntu@54.205.253.94:data/prob4_10_total.npy data/cfr/aws_new/.
scp -i pokerbot.pem ubuntu@54.205.253.94:data/prob4_25_total.npy data/cfr/aws_new/.
scp -i pokerbot.pem ubuntu@54.205.253.94:data/prob4_50_total.npy data/cfr/aws_new/.
scp -i pokerbot.pem ubuntu@54.205.253.94:data/prob4_90_total.npy data/cfr/aws_new/.
scp -i pokerbot.pem ubuntu@54.205.253.94:data/prob4_140_total.npy data/cfr/aws_new/.
scp -i pokerbot.pem ubuntu@54.205.253.94:data/prob4_200_total.npy data/cfr/aws_new/.
scp -i pokerbot.pem ubuntu@54.205.253.94:data/prob4_300_total.npy data/cfr/aws_new/.
