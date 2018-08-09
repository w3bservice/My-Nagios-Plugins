#!/usr/bin/python

import mysql.connector,os,sys,getopt

def usage():
    print """Usage: check_mysql_slave.py [-h] [-H hostname or ipaddr] [-u username] [-p password]\
 [-w seconds] [-c seconds]"""
 

def db_conn_test():
	global config
	try: 
		cnn=mysql.connector.connect(**config) 
		if cnn: 
			print "Database connection: OK" 
			cnn.close()
			return cnn
	except mysql.connector.Error as e: 
		print('Database connect fails!{}'.format(e))
		sys.exit(3)
	  
def db_slave_test(warn,crit):
	global config
	que = "show slave status"
	cnn = mysql.connector.connect(**config)
	cur = cnn.cursor()
	cur.execute(que)
	col	= cur.column_names
	data = cur.fetchone()
	result = {}
	for i in range(0,len(data)):
		result[col[i]] = data[i]
		i += 1
	
	cur.close()
	cnn.close()

	warn = int(warn)
	crit = int(crit)
	if warn > crit:
		usage()
		print ('Parameter inconsistency: "warning time" is greater than "critical time"!')
		sys.exit(3)
	
	hostname = os.popen("/bin/hostname -f").read().strip('\n')
	slave_sec = int(result['Seconds_Behind_Master'])
	info_list = ('Master_Host:', str(result['Master_Host']),'Master_Log_File:', str(result['Master_Log_File']),\
				'Read_Master_Log_Pos:',result['Read_Master_Log_Pos'],'Slave_IO_Running:', str(result['Slave_IO_Running']),\
				'Slave_SQL_Running:',str(result['Slave_SQL_Running']),'Last_Errno:',result['Last_Errno'],\
				'Seconds_Behind_Master:',result['Seconds_Behind_Master'])
	
	if result['Slave_IO_Running'] != 'Yes' or result['Slave_SQL_Running'] != 'Yes':
		print ("Critical: %s MySQL Master-Slave status: Down " % hostname, info_list)
		sys.exit(2)
	if warn == 0 and crit == 0:
		print ("OK: %s MySQL Master-Slave status: "% hostname, info_list)
		sys.exit(0)
	if slave_sec > crit:
		print ("Critical: Seconds Behind Master large than %d Seconds" % crit,\
		"Seconds_Behind_Master is: %d" % result['Seconds_Behind_Master']) 
		sys.exit(2)
	if slave_sec > warn:
		print ("Warning: Seconds Behind Master large than %d Seconds" % warn,\
		"Seconds_Behind_Master is: %d" % result['Seconds_Behind_Master']) 
		sys.exit(1)
	else:
		print ("OK: %s MySQL Master-Slave status: "% hostname, info_list)
		sys.exit(0)

 
def main():
 
	allargs = "hH:u:p:w:c:"

	try:
		options, args = getopt.getopt(sys.argv[1:],allargs)
	except getopt.GetoptError:
		usage()
		sys.exit(3)

	global warn_val
	global crit_val

	for name, value in options:
		if name == "-h":
			usage()
			sys.exit(0)
		elif name == "-H":
			host = value
		elif name == "-u":
			username = value
		elif name == "-p":
			passwd = value
		elif name == "-w":
			warn_val = value
		elif name == "-c":
			crit_val = value

	if len(sys.argv) == 1:
		usage()
		sys.exit(3)

	global config
	config = {
		'host':'127.0.0.1',
		'port':3306,
		'user':username,
		'password':passwd,
	}

	db_conn_test()
	db_slave_test(warn_val,crit_val)

if __name__ == "__main__":
	config = {}
	warn_val = 0
	crit_val = 0
	main()
