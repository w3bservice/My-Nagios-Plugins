#!/usr/bin/python
# Get it from internet - useful tool

def mysql_hash_password(password):
    nr = 1345345333
    add = 7
    nr2 = 0x12345671
 
    for c in (ord(x) for x in password if x not in (' ', '\t')):
        nr^= (((nr & 63)+add)*c)+ (nr << 8) & 0xFFFFFFFF
        nr2= (nr2 + ((nr2 << 8) ^ nr)) & 0xFFFFFFFF
        add= (add + c) & 0xFFFFFFFF
 
    return "%08x%08x" % (nr & 0x7FFFFFFF,nr2 & 0x7FFFFFFF)
 
import hashlib
 
def mysql_password(str):
        """
	Hash string twice with SHA1 and return uppercase hex digest,
	prepended with an asterix.
	This function is identical to the MySQL PASSWORD() function.
        """
	pass1 = hashlib.sha1(str).digest()
	pass2 = hashlib.sha1(pass1).hexdigest()
        return "*" + pass2.upper()
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print >> sys.stderr , 'Python Implementation of MySQL\'s old password hash'
        print >> sys.stderr , 'Usage: %s password' % sys.argv[0]
        sys.exit(1) 
    print mysql_hash_password(sys.argv[1])
    print mysql_password(sys.argv[1])
