from telegram.ext import MessageHandler, Filters
from telegram import Bot, Update
from config import *
import datetime
import re
import threading
import pprint

lock = threading.Lock()
def asl(bot:Bot,update:Update):    
    new_members = update.message.new_chat_members
    sekarang    = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()+datetime.timedelta(seconds = 0, hours=0))
    waktu       = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()+datetime.timedelta(seconds=600,hours=0))
    chat_id     = update.message["chat"]["id"]
    chat_type   = update.message["chat"]["type"]
    
    for member in new_members:
        user_id  = member.id
        if user_id == Config.BOT_ID:
            pass
        else:
            user_name= member.username
            pesan = "banned %s"%user_id
            try:
                lock.acquire(True)
                sql         = "INSERT INTO daftar_timer (waktu, chat_id, chat_type, user_id, user_name, pesan, done, sholat, kota) VALUES (?,?,?,?,?,?,?,'','')"
                cur.execute(sql,(waktu, chat_id, chat_type, user_id, user_name, pesan, 0))
                db.commit()
            finally:
                lock.release()

            try:
                lock.acquire(True)
                sql_new_member         = "INSERT INTO new_members (chat_id, chat_type, user_id, user_name,age,done) VALUES (?,?,?,?,?,0)"
                cur.execute(sql_new_member,(chat_id, chat_type, user_id, user_name, 0))
                db.commit()
            finally:
                lock.release()
            update.message.reply_text("Hei @%s! \nASL plz, Or you will be banned in 10 minutes."%member.username)

def check_age(bot:Bot,update:Update):
    # pprint.pprint (update)
    message = update.message.text   
    chat_id     = update.message["chat"]["id"]
    user_id = str(update.message.from_user.id)
    pesan = "banned %s"%user_id
    cek_new_member = "SELECT age FROM new_members WHERE chat_id = '%s' AND user_id = '%s' AND done = 0 and age = 0"%(chat_id, user_id)
    bar, jum = eksekusi( cek_new_member)
    if jum == 0:
        pass
    else:
        age =  (re.sub("\D", "", message))
        if age == "":
            update.message.reply_text("ASL PLS!")
        else:            
            if int(age) >= 17:
                try:
                    lock.acquire(True)
                    done = "UPDATE new_members SET done = 1, age = '%s' WHERE chat_id = '%s' AND user_id = '%s'"%(age,chat_id,user_id)
                    cur.execute(done)
                    db.commit()
                finally:
                    lock.release()

                try:
                    lock.acquire(True)
                    done_timer = "DELETE FROM daftar_timer WHERE chat_id = '%s' AND user_id = '%s' AND pesan = '%s'"%(chat_id,user_id,pesan)
                    cur.execute(done_timer)
                    db.commit()
                finally:
                    lock.release()
                update.message.reply_text("Welcome to the group")
            else:
                update.message.reply_text("You are not allowed to join the group")
            




# dp = Config.dp
# dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, asl))