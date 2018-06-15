# All things that have to do with accessing and manipulating inventory go here

import db_connection

#BomItem represents an item of a bom at a particular level from the parent
class BomItem:
    def __init__(self, bom, level):
        self.bom=bom
        self.level=level


class BomRepository:

    # TODO: We need to add a version indicator here
    def get_children_of_parent(self, parent_part_number, level):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                    SELECT DISTINCT %s as level, bom.parent as parent, bom.child as child, part.description as description, bom.quantity as qty, bom.referenceDesignator as refDes, (SELECT standardPurchasePrice FROM part WHERE partNumber = bom.child) as standardPurchasePrice, bom.quantity * (SELECT standardPurchasePrice FROM part WHERE partNumber = bom.child) as linePrice
                    FROM bom
                    INNER JOIN part ON bom.child = part.partNumber
                    LEFT JOIN supplierPart ON bom.child = supplierPart.orgPartNumber
                    WHERE parent = %s
                    """
                cursor.execute(sql, (level, parent_part_number))
                bom_items = []
                for result in cursor.fetchall():
                    bom_items.append(BomItem(result, level))
                return bom_items
        finally:
            connection.close()

    def get_bom_of_parent(self, part_number, levels_to_show):
        # Using the queue make sure to use pop() and insert(0,X)
        # This way, we always insert at the front and remove from the end
        # Each item is of type bom item
        bom_item_queue = self.get_children_of_parent(part_number, 1) # The parent is the start
        completed_bom_items = []
        while len(bom_item_queue) > 0:
            bom_item = bom_item_queue.pop()
            if bom_item.level < levels_to_show:
                for result in self.get_children_of_parent(bom_item.bom['child'], bom_item.level + 1):
                    bom_item_queue.append(result)
            completed_bom_items.append(bom_item)
        return completed_bom_items

    def set_new_bom_child(self, parent, child, qty, refDes):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                        INSERT INTO bom
                        (parent, child, quantity, referenceDesignator, dateUpdated)
                        VALUES(%s, %s, %s, %s, CURDATE())
                        """
                cursor.execute(sql, (parent, child, qty, refDes))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def get_bom_relationship(self, parent, child):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """SELECT * FROM bom WHERE parent = %s AND child = %s"""
                cursor.execute(sql, (parent, child))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def update_bom_relationship(self, parent, child, qty, ref_des):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                UPDATE bom
                SET quantity = %s, referenceDesignator = %s, dateUpdated = CURDATE()
                WHERE parent = %s AND child = %s
                """
                cursor.execute(sql, (qty, ref_des, parent, child ))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def remove_bom_relationship(self, parent, child):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                DELETE FROM bom
                WHERE parent = %s AND child = %s
                """
                cursor.execute(sql, (parent, child))
                connection.commit()
                return cursor.fetchall()
        finally:
            connection.close()

    def get_bom_cost(self, parent):
        connection = db_connection.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT SUM(bom.linePrice) as bomPrice
                FROM (SELECT DISTINCT bom.parent as parent, bom.child as child, part.description as description, bom.quantity as qty, bom.referenceDesignator as refDes, (SELECT standardPurchasePrice FROM part WHERE partNumber = bom.child) as standardPurchasePrice, bom.quantity * (SELECT standardPurchasePrice FROM part WHERE partNumber = bom.child) as linePrice
                    FROM bom
                    INNER JOIN part ON bom.child = part.partNumber
                    LEFT JOIN supplierPart ON bom.child = supplierPart.orgPartNumber
                    WHERE parent = %s)
                as bom;
                """
                cursor.execute(sql, parent)
                result = cursor.fetchone()
                return result['bomPrice']
        finally:
            connection.close()