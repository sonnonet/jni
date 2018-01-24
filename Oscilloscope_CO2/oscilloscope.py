#!/usr/bin/env python
# write by sonnonet 1.2Ver
# CO2 Rev 2.4
# THL Rev 1.6 Extenstion 
# Serial to Mysql 

# Data Format
# CO2  Data0
# THL Temperature Data0, Humidity Data1, Illumination Data2

import sys
import tos
import datetime
import threading
import pymysql


AM_OSCILLOSCOPE = 0x93

conn = pymysql.connect(host='125.7.128.42', user='root', password='fxoo0880', db='test',charset='utf8')

sql = ""

class OscilloscopeMsg(tos.Packet):
    def __init__(self, packet = None):
        tos.Packet.__init__(self,
                            [('srcID',  'int', 2),
                             ('seqNo', 'int', 4),
                             ('type', 'int', 2),
                             ('Data0', 'int', 2),
                             ('Data1', 'int', 2),
                             ('Data2', 'int', 2),
                             ('Data3', 'int', 2),
                             ('Data4', 'int', 2),
                             ('Data5', 'int', 2),
                             ],
                            packet)
if '-h' in sys.argv:
    print "Usage:", sys.argv[0], "serial@/dev/ttyUSB0:57600"
    sys.exit()

am = tos.AM()

def pbrNum_return(x):
	return {100:1,
		101:2,
		102:3,
		}.get(x,0) 

while True:
    p = am.read()
    if p and p.type == AM_OSCILLOSCOPE:
	msg = OscilloscopeMsg(p.data)

####### CO2 Logic ############
    if msg.type == 1:
	pbr_Num = pbrNum_return(msg.srcID)
	CO2 = msg.Data0
	CO2 = 1.5 * CO2 / 4096 * 2 * 1000
	Now = datetime.datetime.now()
	### MySQL Insert ###
        try:
            with conn.cursor() as curs:
                sql = """insert into JB_Sensor_CO2(NODE_ID,SEQ,CO2,PBR_NUM,REGDATE)
                        values(%s, %s, %s, %s, %s)"""
                curs.execute(sql,(msg.srcID,msg.seqNo,CO2,pbr_Num,Now))
                conn.commit()
        except:
            conn.close()
        print "ID:",msg.srcID, "seqNo:",msg.seqNo, "CO2:",CO2
####### THL Logic ############
    if msg.type == 2:
        Illumi = msg.Data2
        Illumi = (Illumi * 100) / 75
        Illumi = Illumi * 10
        humi = -2.0468 + (0.0367*msg.Data1) + (-1.5955*0.000001)*msg.Data1*msg.Data1
        temp = -(39.6) + (msg.Data0 * 0.01)
        try:
            with conn.cursor() as curs:
                sql = """insert into JB_Sensor_THL(NODE_ID,SEQ,TEMPERATURE,HUMIDITY,ILLUMINATION,REGDATE)
                        values(%s, %s, %s, %s, %s, %s)"""
                curs.execute(sql,(msg.srcID,msg.seqNo,temp,humi,Illumi,Now))
                conn.commit()
        except:
            conn.close()
        print "id:" , msg.srcID, " Count : ", msg.seqNo, \
        "Temperature: ",temp, "Humidity: ",humi, "Illumination: ",Illumi

