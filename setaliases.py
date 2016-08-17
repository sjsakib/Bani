# -*- coding:utf-8 -*-
from variables import DB_CONFIG
import MySQLdb as mdb

con = mdb.connect(**DB_CONFIG)

f  = open("aliases",'r');

with con as cur:
    line = f.readline()[:-1]
    line = line.decode('utf-8')
    line = line.split('-')
    al = line[0]
    als = line[1].split(',')
    for a in als:
        try:
            #cur.execute("INSERT INTO aliases VALUES('{}','{}')".format(a,al))
            cur.execute(u"""INSERT INTO geeky_aliases VALUES('{}','{}')""".format(a,al))
        except:
            print "Failed "+a+" "+al
            raise


