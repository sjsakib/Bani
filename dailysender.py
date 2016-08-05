from routines import *


con = mdb.connect(**DB_CONFIG)

with con as cur:
    cur.execute("""SELECT * FROM users""")
    for i in xrange(cur.rowcount):
        x = cur.fetchone()
        if(x[1] == 'y'):
            mess = getRandom(x[0],con,x[2])
            sendMessage(x[0],mess)