#!/usr/bin/python

import ldap,sys,getopt

def usage():
	print """ldap_user_search.py [-h|--help] [-H|--host ldap_host] [-u|--username ldap_user]"""

def ldap_conn_test(ldap_host):
	try:
		l = ldap.open(ldap_host)
		l.protocol_version = ldap.VERSION3
	except ldap.LDAPError, e:
		print e
		sys.exit(0)

def ldap_user_search(ldap_host, username):
	l = ldap.open(ldap_host)
	l.protocol_version = ldap.VERSION3

	baseDN = "ou=people,dc=yourcompany,dc=com,dc=au"
	searchScope = ldap.SCOPE_SUBTREE
	retrieveAttributes = None
	searchFilter = "uid=*" + username + "*"

	try:
		ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
		result_set = []
		while 1:
			result_type, result_data = l.result(ldap_result_id, 0)
			if (result_data == []):
				break
			else:
				if result_type == ldap.RES_SEARCH_ENTRY:
					result_set.append(result_data)
		if len(result_set) == 0:
			print "User %s not found!" % username
		else:
			for i in range(0,len(result_set)):
				user_info = result_set[i][0][1]
				print "User %d" % i
				print "Name:",user_info['cn']
				print "Title:",user_info['title']
				print "User ID:",user_info['uidNumber']
				print "Mail:",user_info['mail']
				user_info = {}
				i+= 1
	except ldap.LDAPError, e:
		print e

  
def main():
	short_args = "hH:u:"
	long_args = ["help","host=","username="]
	
	try:
		options, args = getopt.getopt(sys.argv[1:], short_args, long_args)
	except getopt.GetoptError:
		usage()
		sys.exit(1)
	
	for name, value in options:
		if name in ("-h", "--help"):
			usage()
			sys.exit(0)
		if name in ("-H", "--hostname"):
			ldap_host = value
		if name in ("-u", "--username"):
			username = value
				
	if len(sys.argv) == 1:
		usage()
		sys.exit(1)

	ldap_conn_test(ldap_host)
	ldap_user_search(ldap_host, username)
	
if __name__ == "__main__":
	main()
