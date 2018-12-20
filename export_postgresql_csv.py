#!/bin/python

import os,psycopg2,csv,datetime

class db_conn():
	def __init__(self):
		self.database = "smsdb"
		self.user = "smsapi"
		self.host = "##hostname or ip##"
		self.password = "##your password##"
		self.conn = psycopg2.connect("dbname='" + self.database + "' user='" + self.user + "' host='" + self.host + "' password='" + self.password + "'")
		self.cursor = self.conn.cursor()
		self.date = datetime.date.today().strftime("%Y%m%d")
		self.dump_dir = "/var/spool/metadataretention/%s" % self.date

	def dump_sent(self):
		if not os.path.isdir(self.dump_dir):
			os.makedirs(self.dump_dir)
		dump_sent = "SELECT id_downstream,from_addr,to_addr,status,segment_count,request_id,account_id,user_id,client_ip,created_at FROM service_sms_sms_mt WHERE (current_timestamp-created_at)<'24 hours'"
		sent_file = "%s/sms_sent_%s.csv" % (self.dump_dir,self.date)
		self.cursor.copy_expert("COPY (%s) TO STDOUT DELIMITER ',' CSV HEADER" % (dump_sent), open(sent_file, "w"))
	
	def dump_received(self):
		dump_received = "SELECT id_upstream,from_addr,to_addr,account_id,created_at FROM service_sms_inbound_sms_mo WHERE (current_timestamp-created_at)<'24 hours'"
		received_file = "%s/sms_received_%s.csv" % (self.dump_dir,self.date)
		self.cursor.copy_expert("COPY (%s) TO STDOUT DELIMITER ',' CSV HEADER" % (dump_received), open(received_file, "w"))
	
	def get_files(self):
		self.dump_sent()
		self.dump_received()

if __name__ == "__main__":
	dump = db_conn()
	dump.get_files()
