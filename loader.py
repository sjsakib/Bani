# -*- coding: utf-8 -*-
import MySQLdb as mdb
from variables import DB_CONFIG

con = mdb.connect(**DB_CONFIG)
cur = con.cursor()
with open('banies','r') as f:
    while True:
        s = f.readline()[:-1]
        if not s: break
        s = s.decode('utf-8')
        print s
        s = s.split('#')
        if(len(s) == 3):
            cur.execute(u"""INSERT INTO quotes VALUES(NULL,"{}","{}")""".format(s[0],s[1]))
            cur.execute(u"""SELECT LAST_INSERT_ID()""")
            i = cur.fetchone()[0]

            s[1] = s[1].strip().replace(' ','_')
            s[1] = s[1].replace('.','')
            s[2] = s[2].strip().replace(' ','_')

            if(s[2]):
                cur.execute(u"""SELECT alias FROM aliases WHERE alias = '{}'""".format(s[2]))
                if(cur.rowcount == 0):
                    cur.execute(u"""INSERT INTO aliases VALUES('{}','{}')""".format(s[2],s[2]))
                    cur.execute(u"""CREATE TABLE  IF NOT EXISTS {}(id INT NOT NULL auto_increment primary key,quote_id INT references quotes(id)) CHARACTER SET utf8 COLLATE utf8_general_ci""".format(s[2]))
                    con.commit()
                cur.execute(u"""INSERT INTO {} VALUES(null,{})""".format(s[2],i))


            if(s[1]):
                cur.execute(u"""SELECT alias FROM aliases WHERE alias = '{}'""".format(s[1]))
                if(cur.rowcount == 0):
                    cur.execute(u"""INSERT INTO aliases VALUES('{}','{}')""".format(s[1],s[1]))
                    cur.execute(u"""CREATE TABLE IF NOT EXISTS {}(id INT NOT NULL auto_increment primary key,quote_id INT references quotes(id)) CHARACTER SET utf8 COLLATE utf8_general_ci""".format(s[1]))
                    con.commit()
                cur.execute(u"""INSERT INTO {} VALUES(null,{})""".format(s[1],i))

con.commit()
con.close()

