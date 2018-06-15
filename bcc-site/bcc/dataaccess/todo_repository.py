import db_connection

class TodoRepository:
    def get_todo_list(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM todo ORDER BY dateUpdated DESC"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_todo_category_list(self, category):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM todo WHERE category=%s ORDER BY dateUpdated DESC"
                cursor.execute(sql, category)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_todo_unfinished_list(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM todo WHERE dateCompleted IS NULL ORDER BY dateUpdated DESC"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()

    def set_todo_item(self, category, description, date_added):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT IGNORE INTO todo (category, description, dateUpdated) VALUES (%s, %s, %s)"
                cursor.execute(sql, (category, description, date_added))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def get_todo_categories(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT DISTINCT category FROM todo"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()

    def set_complete_todo(self, id):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "UPDATE todo SET dateCompleted = CURDATE() WHERE id=%s;"
                cursor.execute(sql, id)
                return cursor.fetchall()
        finally:
            connection.close()