import db_connection

class TodoRepository:
    def get_todo_list(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM todo;"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()

    def add_todo_item(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM todo;"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()