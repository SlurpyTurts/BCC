import db_connection

class OrderOverviewRepository:
    def get_order_overview(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "SELECT orderOverview.orderNumber, orderOverview.orderDate, contact.firstName, contact.lastName, dealer.dealerName, orderOverview.dealerid, terms.description as termsDescription, orderOverview.invoiceSentDate, orderOverview.invoiceStatus, orderOverview.termsid, SUM(pricing.dealerGrossPrice*orderLine.lineQuantity) as orderTotal, SUM(orderLine.lineDiscount*orderLine.lineQuantity) as orderDiscount FROM orderOverview INNER JOIN orderLine ON orderOverview.orderNumber = orderLine.orderNumber INNER JOIN pricing ON orderLine.partNumber = pricing.partNumber INNER JOIN contact ON orderOverview.customerid = contact.id INNER JOIN dealer ON orderOverview.dealerid = dealer.id INNER JOIN terms ON orderOverview.termsid = terms.id GROUP BY orderLine.orderNumber;"
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()