import random
import requests
import MySQLdb as mdb
from variables import *
import time

def callSendAPI(data):
    requests.post(API_URL+ACCESS_TOKEN,json = data)

def sendMessage(user,message):
    data = {
        'recipient': {'id':user},
        'message'  : {'text':message}
    }
    callSendAPI(data)

def findUser(user,con):
    with con as cur:
        cur.execute("SELECT id FROM users WHERE id = {} ".format(user))
        if(cur.rowcount == 0 ):
            cur.execute("""INSERT INTO users VALUES ({},'n',0)""".format(user))
            sendMessage(user,WELCOME_MESSAGE)


def subscribe(userId,con):
    with con as cur:
        #not checking if somebody subscribed already
        cur.execute("""UPDATE users SET status='y' WHERE id = {}""".format(userId))

def unsubscribe(userId,con):
    with con as cur:
        cur.execute("""UPDATE users SET status='n' WHERE id = {}""".format(userId))

def getRandom(userId,con,cnt = None):
    with con as cur:
        if(cnt == None):
            cur.execute("""SELECT cnt from users WHERE id = {}""".format(userId))
            cnt = cur.fetchone()[0]
        cur.execute("""UPDATE users SET cnt = {} WHERE id = {}""".format(cnt+1,userId))
        cur.execute("""SELECT COUNT(*) FROM quotes""")
        total = cur.fetchone()[0]


        #Don't know how much it will work.
        #But I think this will reduce the chances of sending same message again
        random.seed(int(userId))
        for i in xrange(cnt):
            x = random.randint(1,total)
        cur.execute("""SELECT text,author FROM quotes WHERE id = {}""".format(random.randint(1,total)))
        random.seed(time.clock()*1000000)
        data = cur.fetchone()

        if(data[1]): return data[0]+u'\n--- '+data[1]
        else: return data[0]


def checkCat(text,con):
    with con as cur:
        cur.execute(u"""SELECT cat FROM aliases WHERE alias = '{}'""".format(text))
        if(cur.rowcount == 0):
            return -1
        else:
            return cur.fetchone()[0]
def checkGeekyCat(text,con):
    with con as cur:
        cur.execute(u"""SELECT cat FROM geeky_aliases WHERE alias = '{}'""".format(text))
        if(cur.rowcount == 0):
            return -1
        else:
            return cur.fetchone()[0]

def getByCat(cat,con):
    with con as cur:
        cur.execute(u"""SELECT COUNT(*) FROM {}""".format(cat))
        total = cur.fetchone()[0]
        cur.execute(u"""SELECT quote_id FROM {} WHERE id = {}""".format(cat,random.randint(1,total)))
        quote_id = cur.fetchone()[0]
        cur.execute(u"""SELECT text,author FROM quotes WHERE id = {}""".format(quote_id))
        data = cur.fetchone()

        if(data[1]): return data[0]+u'\n--- '+data[1]
        else: return data[0]


def getByGeekyCat(cat,con):
    with con as cur:
        cur.execute(u"""SELECT COUNT(*) FROM {}""".format(cat))
        total = cur.fetchone()[0]
        cur.execute(u"""SELECT quote_id FROM {} WHERE id = {}""".format(cat,random.randint(1,total)))
        quote_id = cur.fetchone()[0]
        cur.execute(u"""SELECT text,author FROM geeky_quotes WHERE id = {}""".format(quote_id))
        data = cur.fetchone()

        if(data[1]): return data[0]+u'\n--- '+data[1]
        else: return data[0]



def respond(user,message):
    try:
        con = mdb.connect(**DB_CONFIG)
    except:
        return -1

    message = message.replace(' ','_')
    findUser(user,con)

    if(message == 'subscribe' or message == 'Subscribe'):
        subscribe(user,con)
        #print SUBSCRIBED_MESSAGE
        sendMessage(user,SUBSCRIBED_MESSAGE)
    elif(message == 'unsubscribe' or message == 'Unsubscribe'):
        unsubscribe(user,con)
        #print UNSUBSCRIBED_MESSAGE
        sendMessage(user,UNSUBSCRIBED_MESSAGE)
    elif(message == 'random' or message == 'Random'):
        mess = getRandom(user,con)
        #print mess
        sendMessage(user,mess)
    else:
        cat = checkCat(message,con)
        if(cat == -1):
            cat = checkGeekyCat(message,con)
            if(cat == -1):
                #print INSTRUCTIONS_MESSAGE
                sendMessage(user,INSTRUCTIONS_MESSAGE)
                with open('log','a') as f:
                    f.write('Failed to respond: '+message+'\n')
            else:
                mess = getByGeekyCat(cat,con)
                sendMessage(user,mess)
        else:
            mess = getByCat(cat,con)
            #print mess
            sendMessage(user,mess)

