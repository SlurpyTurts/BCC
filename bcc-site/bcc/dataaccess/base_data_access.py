import db_connection

class BaseDataAccess:

    def select_request(self, query, parameters=()):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, parameters)
                return cursor.fetchall()
        finally:
            connection.close()