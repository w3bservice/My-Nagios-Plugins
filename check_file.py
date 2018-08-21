#!/usr/bin/python
# Check lock files exist and file time
# Jack.Su - INFRA-699

import os,datetime,sys,getopt

def usage():
	print """check_file_exist_time.py [-h|--help] [-t|--time mins] [-C|--check <filename with full path>]"""
	
def check_file(filename,time):
	current_time = datetime.datetime.now()
	time = int(time)
	check_time = current_time - datetime.timedelta(minutes=time)
	if os.path.exists(filename):
		filemtime = os.path.getmtime(filename)
		file_time = datetime.datetime.fromtimestamp(filemtime)
		file_exist_time = current_time - file_time
		if file_time < check_time:
			print "Warning: File %s exist and older than %d minutes" % (filename,time)
			sys.exit(1)
		else:
			print "OK: File %s exists for %s" % (filename,file_exist_time)
			sys.exit(0)
	else:
		print "OK: File %s not exist!" % filename
		sys.exit(0)

def main():
	short_args = "ht:C:"
	long_args = ["help","time=","check="]

	try:
   		options, args = getopt.getopt(sys.argv[1:], short_args, long_args)
	except getopt.GetoptError:
    		usage()
		sys.exit(3)

	for name, value in options:
		if name in ("-h", "--help"):
			usage()
			sys.exit(0)
		if name in ("-t", "--time"):
			time = value
		if name in ("-C", "--check"):
			file = value
			check_file(file,time)

	if len(sys.argv) == 1:
		usage()
		sys.exit(3)

if __name__ == "__main__":
	main()
