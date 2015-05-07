import pymysql

def connect_to_database():
    try:
        db = pymysql.connect(host='amundsen.co', user='amundxao_andreas', password='Tennis123',
                             database='amundxao_globalhighscores')
        global cur
        cur = db.cursor()
        valid_connection = True
        print("Connection successful!")
    except:
        valid_connection = False
        print("Connection failed!")
    return valid_connection, cur