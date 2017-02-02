
# All things that have to do with accessing and manipulating inventory go here

import db_connection

class PartRepository:

    def get_part_by_part_number(self, part_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT part.partNumber, part.description, part.partTypeSubClass1, part.partTypeSubClass2, part.partTypeSubClass3, part.partTypeSubClass1, part.dateAdded, part.unit, part.status, partStatus.statusName FROM part INNER JOIN partStatus ON part.status = partStatus.id WHERE partNumber = %s;"
                cursor.execute(sql, part_number)

                return cursor.fetchone()
        finally:
            connection.close()

    def get_parts_by_part_number_prefix(self, part_number_prefix):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM bcc.part where partNumber like %s"
                cursor.execute(sql, part_number_prefix + '%' )

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