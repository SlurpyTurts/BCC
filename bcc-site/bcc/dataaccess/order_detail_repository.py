import db_connection

class OrderDetailRepository:
    def get_order_lines(self, order_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "SELECT orderLine.partNumber, part.description, orderLine.lineQuantity, orderLine.lineDiscount, IF(orderOverview.termsid = 1, pricing.dealerGrossPrice, IF(orderOverview.termsid = 2, pricing.dealerDemoGrossPrice, 0)) as unitPrice,  IF(orderOverview.termsid = 1, (pricing.dealerGrossPrice - orderLine.lineDiscount) * orderLine.lineQuantity, IF(orderOverview.termsid = 2, (pricing.dealerDemoGrossPrice - orderLine.lineDiscount) * orderLine.lineQuantity, 0)) as linePrice FROM orderOverview INNER JOIN orderLine ON orderOverview.orderNumber = orderLine.orderNumber INNER JOIN pricing ON orderLine.partNumber = pricing.partNumber INNER JOIN part ON orderLine.partNumber = part.partNumber WHERE orderOverview.orderNumber = %s;"
                cursor.execute(sql, order_number)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_order_payments(self, order_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "SELECT transactionDate, amount, method FROM payment WHERE orderNumber = %s;"
                cursor.execute(sql, order_number)
                return cursor.fetchall()
        finally:
            connection.close()