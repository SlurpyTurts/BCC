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
                sql = "SELECT * FROM bcc.bom WHERE parent = %s;"
                cursor.execute(sql, parent_part_number)
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
