import pymysql.cursors

def get_connection():
    # connect to the database
    return pymysql.connect(host='localhost',
                           user='root',
                           password='my-secret-password',
                           db='bcc',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)

