#!/usr/bin/env python

HDHR_DEVICE_ID="10176195"
HDHR_TUNER_ID=0
HDHR_CFG_CMD="/usr/bin/hdhomerun_config"
LOCAL_PORT="1234"

import re, os, sys, socket, time

class Program(object):
	def __init__(self, channel, program_number, description):
		self.channel=channel
		self.number=program_number
		self.description=description
	def __str__(self):
		return "Program %d: %s"%(self.number,self.description)
	def setProgram(self):
		self.channel.setChannel()
		cmd = "%s %s set /tuner%d/program %d"%(HDHR_CFG_CMD, HDHR_DEVICE_ID, HDHR_TUNER_ID, self.number)
		if os.system(cmd) != 0:
			print "ERROR: %s"%(cmd)
		

class Channel(object):
	def __init__(self, channel_number):
		self.number=channel_number
		self.program_list=[]
	def __str__(self):
		return "Channel %d"%(self.number)
	def addProgram(self, program_number, description):
		self.program_list.append(Program(self,program_number,description))
	def getPrograms(self):
		return self.program_list
	def setChannel(self):
		cmd = "%s %s set /tuner%d/channel %d"%(HDHR_CFG_CMD, HDHR_DEVICE_ID, HDHR_TUNER_ID, self.number)
		if os.system(cmd) != 0:
			print "ERROR: %s"%(cmd)
		

re_channel=re.compile("^SCANNING: [0-9]+ \(.*:([0-9]+)\)$")
re_lock=re.compile("^LOCK: ([^ ]+) \(.*\)$")
re_program=re.compile("^PROGRAM ([0-9]+): (.*)$")
channel_number=0
channel=None
channels=[]
f = open("scan0.txt")

for l in f.readlines():

	m = re_channel.match(l)
	if m:
		channel_number = int(m.group(1))
		continue

	m = re_lock.match(l)
	if m:
		lock = m.group(1)
		if lock != "none":
			channel=Channel(channel_number)
			channels.append(channel)

	m = re_program.match(l)
	if m:
		program_number = int(m.group(1))
		program_description = m.group(2)
		channel.addProgram(program_number,program_description)

def get_local_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	try:
	    s.connect(("8.8.8.8", 9))
	    client = s.getsockname()[0]
	except socket.error:
	    client = "Unknown IP"
	finally:
	    del s
	print "DEBUG: Got Local IP = %s"%(client)
	return client

def local_display():
	cmd = "vlc udp://@:%s &"%(LOCAL_PORT)
	if os.system(cmd) != 0:
		print "ERROR: %s"%(cmd)

def set_target():
	cmd = "%s %s set /tuner%d/target %s:%s"%(HDHR_CFG_CMD, HDHR_DEVICE_ID, HDHR_TUNER_ID, get_local_ip(), LOCAL_PORT)
	if os.system(cmd) != 0:
		print "ERROR: %s"%(cmd)

if len(sys.argv) > 1:
	ch_in = int(sys.argv[1])
	pr_in = int(sys.argv[2])
	for c in channels:
		if c.number == ch_in:
			for p in c.getPrograms():
				if p.number == pr_in:
					p.setProgram()
					local_display()
					time.sleep(2)
					set_target()
					
else:
	
	for c in channels:
		print "%s"%(c)
		for p in c.getPrograms():
			print "%s"%(p)
		print
