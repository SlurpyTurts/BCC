import db_connection

class DealerRepository:

    def get_dealer_list(self, start_id, number_of_dealers):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "SELECT * FROM bcc.dealer WHERE id > %s AND id <= %s"
                cursor.execute(sql, (start_id, start_id + number_of_dealers))
                return cursor.fetchall()
        finally:
            connection.close()