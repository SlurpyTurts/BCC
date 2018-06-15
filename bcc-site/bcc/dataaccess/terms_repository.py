import db_connection

class TermsRepository:
    def get_terms_list(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM terms"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()