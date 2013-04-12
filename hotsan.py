#!/usr/bin/env python
# $Id$
# This will work on a Solaris 10 system with SAN storage disks (with QFS or not).
# The idea is to sample the average services time of the disks and guage how
# busy is the disk array that might be shared with other systems.
# Author: Philip Lee

import os, sys, time

def usage():
	if (len(sys.argv) == 2) and ((sys.argv[1] == '-h') or (sys.argv[1] == '-help')):
		print sys.argv[0] + " samples iostat data and reports when SAN disks are hot."
	else:
		print "Usage: " + sys.argv[0] + " [-h|--help]"

def iostat_stats(s):
	S = []
	cmd = "iostat -xnM " + str(s) + " 1|egrep -v 'c0|c1'|awk '{print $8}'|egrep -v asvc_t"
	S = os.popen(cmd).read()
	S = S.split()
	return S

def test_hot(S):
	burning = False
	normal = 35.0		# define asvc_t thershold anything above 35 msec, flag as hot	
	size = len(S)		# define size of the iostat output, depends on number of disk
	half = len(S)/2		# define number of disks > normal then capture one data point

	hot = 0
	for stat in range(0,size):
		if float(S[stat]) > normal:
			hot +=  1

	if hot > half:
		burning = True
		
	return burning
	
def main():
	sec = 1 		# iostat in 2 sec intervals
	num_reg = 5		# do sample set of 5 data points
	sleep_sec = 5		# sleep between each sample point
	num_hot = 0
	is_hot = False

	for reg in range(0,num_reg):
		T = iostat_stats(sec)
		is_hot = test_hot(T)
		if (is_hot):
			num_hot += 1 
		time.sleep(sleep_sec)

	if num_hot == num_reg:
		print "Hot!! num_hot: %d /num_reg: %d" % (num_hot, num_reg)
	else:
		print "Not burning yet. num_hot: %d /num_reg: %d" % (num_hot, num_reg)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		usage()
	else:
		main()
