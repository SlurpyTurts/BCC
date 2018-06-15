import db_connection

class TestRepository:
    def set_amp_test(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM todo ORDER BY dateUpdated DESC"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()