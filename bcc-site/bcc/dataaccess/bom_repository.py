# All things that have to do with accessing and manipulating inventory go here

import db_connection, base_data_access

data_access = base_data_access.BaseDataAccess()

#BomItem represents an item of a bom at a particular level from the parent
class BomItem:
    def __init__(self, bom, level):
        self.bom=bom
        self.level=level


class BomRepository:

    # TODO: We need to add a version indicator here
    def get_children_of_parent(self, parent_part_number, level):
        results = data_access.select_request("""
                    SELECT DISTINCT %s as level, bom.parent as parent, bom.child as child, part.description as description, bom.quantity as qty, bom.referenceDesignator as refDes, (SELECT standardPurchasePrice FROM part WHERE partNumber = bom.child) as standardPurchasePrice, bom.quantity * (SELECT standardPurchasePrice FROM part WHERE partNumber = bom.child) as linePrice
                    FROM bom
                    INNER JOIN part ON bom.child = part.partNumber
                    LEFT JOIN supplierPart ON bom.child = supplierPart.orgPartNumber
                    WHERE parent = %s
                    """, (level, parent_part_number))
        bom_items = []
        for result in results:
            bom_items.append(BomItem(result, level))
        return bom_items

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
        return data_access.select_request("""SELECT * FROM bom WHERE parent = %s AND child = %s""", (parent, child))

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
        return data_access.select_one("""
                SELECT SUM(bom.linePrice) as bomPrice
                FROM (SELECT DISTINCT bom.parent as parent, bom.child as child, part.description as description, bom.quantity as qty, bom.referenceDesignator as refDes, (SELECT standardPurchasePrice FROM part WHERE partNumber = bom.child) as standardPurchasePrice, bom.quantity * (SELECT standardPurchasePrice FROM part WHERE partNumber = bom.child) as linePrice
                    FROM bom
                    INNER JOIN part ON bom.child = part.partNumber
                    LEFT JOIN supplierPart ON bom.child = supplierPart.orgPartNumber
                    WHERE parent = %s)
                as bom;
                """, parent)['bomPrice']