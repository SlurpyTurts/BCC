import db_connection, base_data_access

data_access = base_data_access.BaseDataAccess()

class SupplierRepository:
    def get_supplier_parts_by_part(self, part_number):
        return data_access.select_request("""SELECT supplierPart.supplierid, supplier.supplierName, supplierPart.supplierPartNumber, supplierPart.supplierLink, supplierPart.purchaseUnitPrice, supplierPart.purchaseMOQ, supplierPart.standardPartPrice
                FROM supplierPart
                INNER JOIN supplier ON supplierPart.supplierid = supplier.id
                WHERE orgPartNumber = %s
                ORDER BY purchaseMOQ ASC""", part_number)

    def get_supplier_list(self, supplier_start, number_of_suppliers):
        return data_access.select_request("""SELECT * FROM supplier ORDER BY supplierName ASC LIMIT %s, %s;""", (supplier_start, number_of_suppliers))

    def get_supplier_detail(self, supplier_id):
        return data_access.select_request("""SELECT * FROM supplier WHERE id = %s""")

    def get_part_price(self, part_number, moq, supplier_part_number):
        return data_access.select_one("""
                        SELECT purchaseUnitPrice
                        FROM supplierPart
                        WHERE orgPartNumber = %s
                            AND purchaseMOQ= %s
                            AND supplierPartNumber = %s
                        """, (part_number, moq, supplier_part_number))['purchaseUnitPrice']

    def get_supplier_part_by_supplier(self, supplier_id):
        return data_access.select_request("""SELECT * FROM supplierPart WHERE supplierid = %s""", supplier_id)

    def get_max_supplier_id(self):
        return data_access.select_one("""SELECT MAX(id) as id FROM supplier""")['id']

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