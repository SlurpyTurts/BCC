import pymysql.cursors

def get_connection():
    # connect to the database
    return pymysql.connect(host='127.0.0.1',
                           user='bccuser',
                           password='password',
                           db='BCC',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
