#!/usr/bin/python

#   mkvirtualenv --python=/usr/bin/python3.7 mysite-virtualenv
#   pip install pyTelegramBotAPI

#   pip3 install mysql-connector-python==8.0.29
#   pip3 install opencv-python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.


import telebot
from hashlib import sha256
import mysql.connector
from mysql.connector import Error
import cv2
from io import BytesIO
import numpy as np
from secrets.db_config import DB_CONFIG


API_TOKEN = '5603564914:AAGzm6Lt4SrElEPpdawdDFKsMSchiEgQwWY'

bot = telebot.TeleBot(API_TOKEN)

ID_LEN=64
PAIRING = "pairing"
PAIRED = "paired"
OK = "ok"
is_valid_qr = False
#table_name = "RollerChorderDatabaseTable"
username = "645843test_username98923823"
qr_hash = ''
hex_number = sha256(b"test_hash")
hashcode = hex_number.hexdigest()
link = "no_link"

# //. PREPARED STATEMENTS

insertline= """INSERT INTO RollerChorderDatabaseTable (telegram_id, qr_hash_code, last_link)
    VALUES
    ('%s', '%s', '%s'); """ # % (username, hashcode, link,)
lookForToupleFromUsername= """SELECT * FROM RollerChorderDatabaseTable WHERE telegram_id = %s;"""# % (username,)
lookForUsername= """SELECT telegram_id FROM RollerChorderDatabaseTable WHERE telegram_id = %s;"""# % (username,)
lookForState= """SELECT user_state FROM RollerChorderDatabaseTable WHERE telegram_id = %s;"""# % (username,)
registerUsername= """INSERT INTO RollerChorderDatabaseTable (telegram_id,user_state)
                            VALUES  (%s,%s); """ #% ( hashusername,PAIRING,)
updateState= """UPDATE RollerChorderDatabaseTable
                SET user_state = %s
                WHERE telegram_id=%s;""" #% (PAIRING, hashusername,)
updateQRState= """UPDATE RollerChorderDatabaseTable
                SET qr_hash_code=%s, user_state = %s
                WHERE telegram_id=%s;""" #% (qr_value,PAIRED, hashusername,)
updateLink= """UPDATE RollerChorderDatabaseTable
                SET last_link=%s
                WHERE telegram_id=%s;""" #% (link, hashusername,)
lookForQR= """SELECT * FROM RollerChorderDatabaseTable WHERE qr_hash_code = %s;"""# % (qr_value,)
deleteQR= """UPDATE RollerChorderDatabaseTable
                SET qr_hash_code = ""
                WHERE qr_hash_code = %s;"""# % (qr_value,)

#   //. FUNCTIONS
def indexExists(list,index):
    try:
        list[index]
        return True
    except IndexError:
        return False

def getHashUsername(message):
    username = str(message.from_user.id)
    hashusername=sha256(username.encode("UTF-8")).hexdigest()
    return hashusername

def read_qr_code(bytes,type = ".png"):
    """Read an image and read the QR code.

    Args:
        filename (string): Path to file

    Returns:
        qr (string): Value from QR code
    """
    y=80
    x=0
    h=368
    w=368
    try:
        img = cv2.imdecode(bytes, 1)
        #img = img[y:y+h, x:x+w]
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        return value
    except:
        return "the reading of QR code has been unsuccesful"

def getConnection():
    connection = mysql.connector.connect(
        host=DB_CONFIG['host'],
        database=DB_CONFIG['database'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    return connection

def close_connection(connection):
    if connection:
        connection.commit()
        result = connection.close()
        print("Connection closed:",result)

#   //. HANDLERS

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start', 'restart'])
def send_welcome(message):
    bot.reply_to(message, """\
    Hi there, I am RollerChorderBot.
I am here to forward to your apple watch the links you will send to me!
To begin use the command /pair to pair an apple watch to your telegram account.""")
    username = message.from_user.id
    hashusername=getHashUsername(message)
    try:
        connection = getConnection()
        cursor = connection.cursor()

        cursor.execute(registerUsername,(hashusername,PAIRING))
        record = cursor.fetchone()
        close_connection(connection)
        print("'help', 'start', 'restart':",record)
    except (Exception, mysql.connector.Error) as error:
        print("'help', 'start', 'restart': Error while registering username: ", error)

# Handle photo sending
@bot.message_handler(content_types=['photo'])
def photo(message):
    hashusername= getHashUsername(message)
    try:
        connection = getConnection()
        cursor = connection.cursor()

        cursor.execute(lookForState,(hashusername,))
        record = cursor.fetchone() #none se non trova niente
        close_connection(connection)
        print('photo: ',record)

        if record[0] == PAIRING:
            fileID = message.photo[-1].file_id
            file_info = bot.get_file(fileID)
            raw_img = BytesIO()
            print("'photo: ' , ",file_info.file_path,"\n\n", raw_img)
            raw_img = bot.download_file(file_info.file_path)
            file_bytes = np.frombuffer(raw_img, dtype=np.uint8)

            #downloaded_file = bot.download_file(file_info.file_path)
            #print ('message.photo =', message.photo)
            #print ('fileID =', fileID)
            #print ('file.file_path =', file_info.file_path)
            #with open("image.jpg", 'wb') as new_file:
            #    new_file.write(downloaded_file)
            qr_value = read_qr_code(file_bytes)
            if len(qr_value) == ID_LEN:
                print("'photo: ' ,qr_value:  ",qr_value)
                try:
                    connection = getConnection()
                    cursor = connection.cursor()

                    cursor.execute(lookForQR,(qr_value,))
                    record = cursor.fetchall()
                    close_connection(connection)
                    if len(record)>=1:

                        bot.reply_to(message,"This QR Code has already been used. Please ask for another one using the button under the QR Code")
                    else:
                        connection = getConnection()
                        cursor = connection.cursor()

                        cursor.execute(updateQRState,(qr_value,PAIRED, hashusername))
                        record = cursor.fetchone()
                        close_connection(connection)
                        print('photo: ',record)
                        bot.reply_to(message,"Great! Now you can proceed and send me a link!")

                except (Exception, mysql.connector.Error) as error:
                    print("'photo: 'Error while updating qr and state", error)
            else:
                bot.reply_to(message,"Nice QR code, but you have to give me a QR from the watch app. Please try again.")
        else:
            bot.reply_to(message,"Nice pic, but you have to start the pairing with /pair to make me parse this image. Please try again.")

    except (Exception, mysql.connector.Error) as error:
        print("'photo: 'Error while getting user data", error)

# Handle '/pair'
@bot.message_handler(commands=['pair'])
def pair(message):
    hashusername= getHashUsername(message)
    try:
        connection = getConnection()
        cursor = connection.cursor()

        cursor.execute(lookForState,(hashusername,))
        record = cursor.fetchone() #none se non trova niente
        close_connection(connection)
        print('pair: ',record)

        if record[0] != PAIRING:
            try:
                connection = getConnection()
                cursor = connection.cursor()

                cursor.execute(updateState,(PAIRING, hashusername))
                record1 = cursor.fetchone() #none se non trova niente
                close_connection(connection)
                print('pair_in: ',record1)
            except (Exception, mysql.connector.Error) as error:
                print("'pair_in: 'Error while getting user data", error)
    except (Exception, mysql.connector.Error) as error:
        print("'pair: 'Error while getting user data", error)


    bot.reply_to(message,"Go on the applewatch app settings, press on 'see QR code' and send me an image of the QR code ")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def parse(message):
    text = str(message.text)
    username = message.from_user.id
    hashusername=getHashUsername(message)
    print ('default: ',username,":",hashusername)

    #query id username is present in database
    try:
        connection = getConnection()
        cursor = connection.cursor()

        cursor.execute(lookForToupleFromUsername,(hashusername,))
        record = cursor.fetchone() #none se non trova niente
        close_connection(connection)
        print('default: ',record)

        if record is None:
            bot.reply_to(message, "It seems that your username is not registered in the RollerChord database. \nUse the command /restart fix this, then use the command /pair")
        elif not indexExists(record,1): #no QR
            bot.reply_to(message, "use the command /pair to pair the apple watch with this telegram account")
        elif len(record[1])!=ID_LEN:
            bot.reply_to(message, "use the command /pair to pair the apple watch with this telegram account")

        else:
            if text.startswith("https://tabs.ultimate-guitar.com/") and not(" " in text):
                    link = str(text)
                    bot.reply_to(message, "Great! the link seems to be fine, i'll now send it to the apple watch")
                    try:
                        connection = getConnection()
                        cursor = connection.cursor()

                        cursor.execute(updateLink,(link, hashusername,))
                        record = cursor.fetchone() #none se non trova niente
                        close_connection(connection)
                        print('default: link updated!',record)

                    except (Exception, mysql.connector.Error) as error:
                        print('default: ',"Error while updating link", error)
                    #1.  update touple userid,qrhash,link with new link

            else:
                    bot.reply_to(message, "Wait a minute, this is not a correct link. \nA corret link should start with something like this: https://tabs.ultimate-guitar.com/ \nPlease try again" )

    except (Exception, mysql.connector.Error) as error:
        print('default: ',"Error while getting data", error)

bot.infinity_polling()

"""
try:
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute(lookForToupleFromUsername,(hashusername,))
    record = cursor.fetchone() #none se non trova niente
    close_connection(connection)
    print('default: ',record)


except (Exception, mysql.connector.Error) as error:
    print('default: ',"Error while getting data", error)
"""