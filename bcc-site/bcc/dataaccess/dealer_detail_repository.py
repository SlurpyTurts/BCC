import db_connection

class DealerDetailRepository:

    def get_dealer_detail(self, dealer_id):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "SELECT * FROM bcc.dealer WHERE id = %s"
                cursor.execute(sql, dealer_id)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_order_list(self, dealer_id):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "SELECT orderNumber, contact.lastName, orderDate, invoiceSentDate, invoiceStatus FROM orderOverview INNER JOIN contact ON orderOverview.customerid = contact.id WHERE orderOverview.dealerID = %s;"
                cursor.execute(sql, dealer_id)
                return cursor.fetchall()
        finally:
            connection.close()