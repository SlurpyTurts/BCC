import db_connection

class SupplierRepository:
    def get_supplier_parts_by_part(self, part_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT supplierPart.supplierid, supplier.supplierName, supplierPart.supplierPartNumber, supplierPart.supplierLink, supplierPart.purchaseUnitPrice, supplierPart.purchaseMOQ
                FROM supplierPart
                INNER JOIN supplier ON supplierPart.supplierid = supplier.id
                WHERE orgPartNumber = %s"""
                cursor.execute(sql, part_number)
                return cursor.fetchall()
        finally:
            connection.close()