import db_connection

class SupplierRepository:
    def get_supplier_parts_by_part(self, part_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT supplierPart.supplierid, supplier.supplierName, supplierPart.supplierPartNumber, supplierPart.supplierLink, supplierPart.purchaseUnitPrice, supplierPart.purchaseMOQ, supplierPart.standardPartPrice
                FROM supplierPart
                INNER JOIN supplier ON supplierPart.supplierid = supplier.id
                WHERE orgPartNumber = %s
                ORDER BY purchaseMOQ ASC"""
                cursor.execute(sql, part_number)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_supplier_list(self, supplier_start, number_of_suppliers):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM supplier ORDER BY supplierName ASC LIMIT %s, %s;"""
                cursor.execute(sql, (supplier_start, number_of_suppliers))
                return cursor.fetchall()
        finally:
            connection.close()

    def get_supplier_detail(self, supplier_id):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM supplier WHERE id = %s"""
                cursor.execute(sql, supplier_id)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_part_price(self, part_number, moq, supplier_part_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql =   """
                        SELECT purchaseUnitPrice
                        FROM supplierPart
                        WHERE orgPartNumber = %s
                            AND purchaseMOQ= %s
                            AND supplierPartNumber = %s
                        """
                cursor.execute(sql, (part_number, moq, supplier_part_number))
                result = cursor.fetchone()
                return result['purchaseUnitPrice']
        finally:
            connection.close()

    def get_supplier_part_by_supplier(self, supplier_id):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM supplierPart WHERE supplierid = %s"""
                cursor.execute(sql, supplier_id)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_max_supplier_id(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT MAX(id) as id FROM supplier"""
                cursor.execute(sql)
                result = cursor.fetchone()
                return result['id']
        finally:
            connection.close()

    def set_new_supplier(self, supplier, website, status, shipping_address_line_1, shipping_address_line_2, shipping_city, shipping_state, shipping_zip, shipping_country,billing_address_line_1, billing_address_line_2, billing_city, billing_state, billing_zip, billing_country):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = """INSERT INTO supplier
                        (supplierName, website, status, shippingAddressLine1, shippingAddressLine2, shippingCity, shippingState, shippingZip, shippingCountry, billingAddressLine1, billingAddressLine2, billingCity, billingState, billingZip, billingCountry)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (supplier, website, status, shipping_address_line_1, shipping_address_line_2, shipping_city, shipping_state, shipping_zip, shipping_country,billing_address_line_1, billing_address_line_2, billing_city, billing_state, billing_zip, billing_country))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def set_standard_purchase_price(self, part_number, moq, supplier_part_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = """UPDATE supplierPart
                        SET standardPartPrice = 1
                        WHERE orgPartNumber = %s AND purchaseMOQ = %s AND supplierPartNumber = %s
                        LIMIT 1"""
                cursor.execute(sql, (part_number, moq, supplier_part_number))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def remove_standard_purchase_price(self, part_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = """UPDATE supplierPart
                        SET standardPartPrice = 0
                        WHERE orgPartNumber = %s"""
                cursor.execute(sql, (part_number))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()