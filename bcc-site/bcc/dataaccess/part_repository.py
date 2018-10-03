
# All things that have to do with accessing and manipulating inventory go here

import db_connection
import base_data_access;

class PartRepository:

    def __init__(self):
        self.data_access = base_data_access.BaseDataAccess()

    def get_part_by_part_number(self, part_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT part.partNumber, part.description, part.partTypeSubClass1, part.partTypeSubClass2, part.partTypeSubClass3, part.dateAdded, part.unit, partUnitType.description as unitDescription, part.status, partStatus.statusName as statusDescription, part.standardSellPrice, part.standardPurchasePrice as standardPurchasePrice
                FROM part
                LEFT JOIN partStatus ON part.status = partStatus.id
                LEFT JOIN partUnitType ON part.unit = partUnitType.id
                WHERE partNumber = %s
                LIMIT 1"""
                cursor.execute(sql, part_number)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_parts_by_part_number_prefix(self, part_number_prefix):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM bcc.part where partNumber like %s"
                cursor.execute(sql, part_number_prefix + '%')
                return cursor.fetchall()
        finally:
            connection.close()

    def get_parts_by_description(self, part_description):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM bcc.part where description like %s"
                cursor.execute(sql, '%' + part_description + '%')
                return cursor.fetchall()
        finally:
            connection.close()

    def get_parts(self, number_of_parts, part_start):
        return self.data_access.select_request("""SELECT partNumber, description, standardPurchasePrice
                FROM part
                ORDER BY partNumber
                LIMIT %s, %s""",
                (number_of_parts, part_start))

    def get_part_status_list(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT id, statusName
                FROM partStatus"""
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_part_unit_list(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT id, description
                FROM partUnitType"""
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_part_type_list(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT a.id, a.description, a.family, (SELECT MAX(partNumber)+1 as newMaxPart FROM part
                WHERE LEFT(partNumber, 3) = a.id) as maxPart
                FROM partType as a"""
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_part_family_list(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT id, description
                FROM partFamily"""
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_parents(self, part_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT bom.parent, part.description
                    FROM bom
                    INNER JOIN part
                    ON part.partNumber = bom.parent
                    WHERE child=%s"""
                cursor.execute(sql, part_number)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_parts_count(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT COUNT(*) as numberOfParts from part
                """
                cursor.execute(sql)
                result = cursor.fetchone()
                return result['numberOfParts']
        finally:
            connection.close()

    def get_max_partNumber(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT COUNT(*) as numberOfParts FROM part"
                cursor.execute(sql)
                result = cursor.fetchone()
                return result['numberOfParts']
        finally:
            connection.close()

    def get_part_description(self, part_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT description FROM part WHERE partNumber = %s"
                cursor.execute(sql, part_number)
                result = cursor.fetchone()
                return result['description']
        finally:
            connection.close()

    def set_part_supplier_update(self, supplier_id, part_number, supplier_part_number, supplier_link, purchase_unit_price, purchase_MOQ):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO supplierPart
                (supplierid, orgPartNumber, supplierPartNumber, supplierLink, purchaseUnitPrice, purchaseMOQ, dateUpdated)
                VALUES(%s, %s, %s, %s, %s, %s, CURDATE())
                """
                cursor.execute(sql, (supplier_id, part_number, supplier_part_number, supplier_link, purchase_unit_price, purchase_MOQ))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def set_new_part(self, part_number, part_description, PTSC1, PTSC2, PTSC3, part_unit, part_status):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO part
                (partNumber, description, partTypeSubClass1, partTypeSubClass2, partTypeSubClass3, dateAdded, unit, status)
                VALUES(%s, %s, %s, %s, %s, CURDATE(), %s, %s)
                """
                cursor.execute(sql, (part_number, part_description, PTSC1, PTSC2, PTSC3, part_unit, part_status))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()





    def update_part(self, part_description, PTSC1, PTSC2, PTSC3, part_status, part_unit, part_purchase_price, part_sell_price, part_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                UPDATE part
                SET description = %s,
                partTypeSubClass1 = %s,
                partTypeSubClass2 = %s,
                partTypeSubClass3 = %s,
                status = %s,
                unit = %s,
                standardPurchasePrice = %s,
                standardSellPrice = %s
                WHERE partNumber = %s
                """
                cursor.execute(sql, (part_description, PTSC1, PTSC2, PTSC3, part_status, part_unit, part_purchase_price, part_sell_price, part_number))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def update_standard_purchase_price(self, part_number, part_price):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    UPDATE part
                    SET standardPurchasePrice = %s
                    WHERE partNumber = %s
                    """
                cursor.execute(sql, (part_price, part_number))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()