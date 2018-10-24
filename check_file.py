#!/usr/bin/python
# Check lock files exist and file time
# Jack.Su - INFRA-699|PLAT-806

import os,datetime,sys,getopt,glob

def usage():
	print """check_file_exist_time.py [-h|--help] [-t|--time mins] [-C|--check '<filename with full path>']"""
	
def check_file(filename,time):
	current_time = datetime.datetime.now()
	time = int(time)
	check_time = current_time - datetime.timedelta(minutes=time)
	file_list=glob.glob(filename)
	errors = 0
	if len(file_list) == 0:
		print "OK: File %s not exist!" % filename
		sys.exit(0)
	else:
		for i in range(0,len(file_list)):
			filemtime = os.path.getmtime(file_list[i])
			file_time = datetime.datetime.fromtimestamp(filemtime)
			file_exist_time = current_time - file_time
			if file_time < check_time:
				print "Warning: File %s exist and older than %d minutes" % (file_list[i],time)
				errors = i + 1
		if errors > 0:
			sys.exit(1)
		else:
			print "OK: Files %s all less than %s minutes." % (filename,time)
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
