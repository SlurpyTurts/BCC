import db_connection

class FreightRepository:
    def get_freight_carrier_list(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM freight"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()