import db_connection, base_data_access

data_access = base_data_access.BaseDataAccess()

class OrderRepository:
    def get_order_overview(self, order_start, number_of_orders):
        return data_access.select_request("""SELECT orderOverview.orderNumber, orderOverview.orderDate, contact.firstName, contact.lastName, dealer.dealerName, orderOverview.dealerid, terms.defaultDescription as termsDescription, orderOverview.invoiceSentDate, orderOverview.orderStatus, orderOverview.termsid, SUM(pricing.grossPrice*orderLine.lineQuantity) as orderTotal, SUM(orderLine.lineDiscount*orderLine.lineQuantity) as orderDiscount
                FROM orderOverview
                INNER JOIN orderLine ON orderOverview.orderNumber = orderLine.orderNumber
                INNER JOIN pricing ON orderLine.partNumber = pricing.partNumber
                INNER JOIN contact ON orderOverview.customerid = contact.id
                INNER JOIN dealer ON orderOverview.dealerid = dealer.id
                INNER JOIN terms ON orderOverview.termsid = terms.id
                GROUP BY orderLine.orderNumber
                LIMIT %s, %s""", (order_start, number_of_orders))

    def get_order_lines(self, order_number):
        return data_access.select_request("""SELECT
                            orderLine.partNumber,
                            part.description,
                            orderLine.lineQuantity,
                            orderLine.lineDiscount,
                            IF(orderOverview.termsid = 1, pricing.grossPrice, IF(orderOverview.termsid = 2, pricing.dealerDemoNetPrice, IF(orderOverview.termsid = 3, pricing.umrp,0))) as unitPrice,
                            IF(orderOverview.termsid = 1, (pricing.grossPrice - orderLine.lineDiscount) * orderLine.lineQuantity, IF(orderOverview.termsid = 2, (pricing.dealerNetPrice - orderLine.lineDiscount) * orderLine.lineQuantity, IF(orderOverview.termsid = 3, (pricing.umrp - orderLine.lineDiscount) * orderLine.lineQuantity,0))) as linePrice
                        FROM orderOverview
                        INNER JOIN orderLine ON orderOverview.orderNumber = orderLine.orderNumber
                        INNER JOIN pricing ON orderLine.partNumber = pricing.partNumber
                        INNER JOIN part ON orderLine.partNumber = part.partNumber
                        WHERE orderOverview.orderNumber = %s""", order_number)

    def get_order_line_detail(self, order_number, lineItem):
        return data_access.select_request("""SELECT *
                FROM orderLine
                WHERE orderNumber = %s AND partNumber = %s""", (order_number,lineItem))

    def get_order_payments(self, order_number):
        return data_access.select_request("SELECT transactionDate, amount, method FROM payment WHERE orderNumber = %s;", order_number)

    def get_order_payments_total(self, order_number):
        return data_access.select_one("""SELECT SUM(amount) as amount
                        FROM payment
                        WHERE orderNumber = %s""", order_number)['amount']

    def get_orders_count(self):
        return data_access.select_one("SELECT COUNT(*) as numberOfOrders FROM orderOverview")['numberOfOrders']

    def get_order_shipments(self, order_number):
        return data_access.select_request("""SELECT dateShipped, trackingNumber, partNumber, shipmentMethod, price, carrier
                        FROM orderShipping
                        WHERE orderNumber = %s""", order_number)

    def get_order_info(self, order_number):
        return data_access.select_request("""SELECT orderNumber, orderDate, dealer.id, dealer.dealerName,
        terms.defaultDescription, invoiceSentDate, orderStatus, DATE_ADD(invoiceSentDate,
        INTERVAL terms.periodDays DAY) as invoiceDueDate,
        CONCAT(contact.firstName," ",contact.lastName) as customerName
                    FROM orderOverview
                    INNER JOIN dealer
                    ON orderOverview.dealerid = dealer.id
                    INNER JOIN terms
                    ON orderOverview.termsid = terms.id
                    INNER JOIN contact
                    ON orderOverview.customerid = contact.id
                    WHERE orderNumber = %s""", order_number)


    # TODO WOAAHHHHH if you have to write SQL like this, something is wrong
    # SQL databases should be treated as a CRUD store, not a number crunching calculator
    def get_order_total(self, order_number):
        return data_access.select_one("""SELECT SUM(orderLines.linePrice) as orderTotal
                FROM(
                    SELECT orderLine.partNumber, part.description, orderLine.lineQuantity, orderLine.lineDiscount,
                        IF(orderOverview.termsid = 1, pricing.dealerNetPrice,
                            IF(orderOverview.termsid = 2, pricing.dealerDemoNetPrice,
                                IF(orderOverview.termsid = 3, pricing.umrp,
                                    IF(orderOverview.termsid = 4, pricing.distributorNetPrice,
                                        IF(orderOverview.termsid = 5, pricing.distributorDemoNetPrice,0
                                        )
                                    )
                                )
                            )
                        ) as unitPrice,
                        IF(orderOverview.termsid = 1, (pricing.dealerNetPrice - orderLine.lineDiscount) * orderLine.lineQuantity,
                            IF(orderOverview.termsid = 2, (pricing.dealerDemoNetPrice - orderLine.lineDiscount) * orderLine.lineQuantity,
                                IF(orderOverview.termsid = 3, (pricing.umrp - orderLine.lineDiscount) * orderLine.lineQuantity,
                                    IF(orderOverview.termsid = 4, (pricing.distributorNetPrice - orderLine.lineDiscount) * orderLine.lineQuantity,
                                        IF(orderOverview.termsid = 5, (pricing.distributorDemoNetPrice - orderLine.lineDiscount) * orderLine.lineQuantity,0
                                        )
                                    )
                                )
                            )
                        ) as linePrice
                    FROM orderOverview
                    INNER JOIN orderLine ON orderOverview.orderNumber = orderLine.orderNumber
                    INNER JOIN pricing ON orderLine.partNumber = pricing.partNumber
                    INNER JOIN part ON orderLine.partNumber = part.partNumber
                    WHERE orderOverview.orderNumber = %s
                ) as orderLines""", order_number)['orderTotal']

    def get_max_order_number(self):
        return data_access.select_one("SELECT MAX(orderNumber) as maxOrder FROM orderOverview")['maxOrder']

    def set_new_order(self, dealer, terms, cust_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO orderOverview (dealerid, termsid, customerid, orderDate) VALUES(%s, %s, %s, CURDATE())"
                cursor.execute(sql, (dealer, terms, cust_number))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def set_new_order_line(self, order_number, part_number, quantity, unit_discount):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO orderLine (orderNumber, partNumber, lineQuantity, lineDiscount, dateAdded) VALUES(%s, %s, %s, %s, CURDATE())"
                cursor.execute(sql, (order_number, part_number, quantity, unit_discount))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def set_new_order_payment(self, order_number, payment_amount, payment_method, payment_reference):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO payment (orderNumber, amount, method, reference, transactionDate) VALUES(%s, %s, %s, %s, CURDATE())"
                cursor.execute(sql, (order_number, payment_amount, payment_method, payment_reference))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def set_new_order_shipment(self, order_number, shipment_item, shipment_serial, shipment_date, shipment_carrier, shipping_method, tracking_number, shipment_cost):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO orderShipping
                (orderNumber, dateShipped, trackingNumber, partNumber, shipmentMethod, price, carrier, productSerialNumber)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (order_number, shipment_date, tracking_number, shipment_item, shipping_method, shipment_cost, shipment_carrier, shipment_serial))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def update_order_line(self, order_number, line_item, quantity, unit_discount):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                        UPDATE orderLine
                        SET dateUpdated = CURDATE(), lineQuantity = %s, lineDiscount = %s
                        WHERE orderNumber = %s AND partNumber = %s
                        """
                cursor.execute(sql, (quantity, unit_discount, order_number, line_item))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def update_order_status(self, order_number, new_status):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                        UPDATE orderOverview
                        SET orderStatus = %s
                        WHERE orderNumber = %s
                        """
                cursor.execute(sql, (new_status, order_number))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def remove_order_line(self, order_number, line_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                        DELETE FROM orderLine
                        WHERE orderNumber = %s AND partNumber = %s
                        """
                cursor.execute(sql, (order_number, line_number))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()