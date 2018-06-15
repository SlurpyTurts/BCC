# All things that have to do with accessing and manipulating inventory go here

import db_connection

class InventoryRepository:

    def get_inventory_list(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT partsIn.partNumber, IF(qtyOut IS NULL,partsIn.qtyIn,partsIn.qtyIn - partsOut.qtyOut) as quantity, part.description
                        FROM (
                            SELECT partNumber, sum(quantity) as qtyIn
                            FROM inventory
                            WHERE locationFrom IS NULL AND locationTo IS NOT NULL
                            GROUP BY partNumber
                            )as partsIn
                        LEFT JOIN (
                            SELECT partNumber, sum(quantity) as qtyOut
                            FROM inventory
                            WHERE locationFrom IS NOT NULL AND locationTo = 8 OR locationTo = 5
                            GROUP BY partNumber
                            ) as partsOut
                        ON partsIn.partNumber = partsOut.partNumber
                        LEFT JOIN part
                        ON part.partNumber = partsIn.partNumber
                        GROUP BY partNumber"""
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_inventory_list_by_loc(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT partsIn.partNumber, IF(qtyOut IS NULL,partsIn.qtyIn,partsIn.qtyIn - partsOut.qtyOut) as quantity, part.description
                        FROM (
                            SELECT partNumber, sum(quantity) as qtyIn
                            FROM inventory
                            WHERE locationFrom IS NULL AND locationTo IS NOT NULL
                            GROUP BY partNumber
                            )as partsIn
                        LEFT JOIN (
                            SELECT partNumber, sum(quantity) as qtyOut
                            FROM inventory
                            WHERE locationFrom IS NOT NULL AND locationTo IS NULL
                            GROUP BY partNumber
                            ) as partsOut
                        ON partsIn.partNumber = partsOut.partNumber
                        LEFT JOIN part
                        ON part.partNumber = partsIn.partNumber
                        GROUP BY partNumber"""
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_part_transactions(self, part_number):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT inventory.quantity, invFrom.locationName as locationFrom, invTo.locationName as locationTo, transactionDate, note
                        FROM inventory
                        LEFT JOIN inventoryLocation as invFrom
                        ON inventory.locationFrom = invFrom.id
                        LEFT JOIN inventoryLocation as invTo
                        ON inventory.locationto = invTo.id
                        WHERE partNumber=%s
                        ORDER BY transactionDate ASC"""
                cursor.execute(sql, part_number)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_inventory_location_list(self):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT DISTINCT id, locationName FROM inventoryLocation"""
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            connection.close()

    def set_inv_transaction(self, part_number, quantity, inventory_from, inventory_to, note, transaction_date):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """INSERT INTO inventory
                (partNumber, quantity, locationFrom, locationTo, note, transactionDate)
                VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (part_number, quantity, inventory_from, inventory_to, note, transaction_date))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()