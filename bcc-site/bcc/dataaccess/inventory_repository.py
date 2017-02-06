# All things that have to do with accessing and manipulating inventory go here

import db_connection

class InventoryRepository:

    def get_inventory_list(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "SELECT * FROM bcc.inventory;"
                cursor.execute(sql)

                return cursor.fetchall()
        finally:
            connection.close()