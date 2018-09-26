
import datetime
from bcc.dataaccess import inventory_repository

def test_get_basic_inventory():
    inv_repo = inventory_repository.InventoryRepository()
    results = inv_repo.get_inventory_list()
    assert len(results) > 2
    first_inventory = results[0]
    transaction_date =  first_inventory['transactionDate']
    assert type(transaction_date) == datetime.date
    assert transaction_date.year == 2016

def test_get_inv_for_part_by_inv():
    inv_repo = inventory_repository.InventoryRepository()
    parts = inv_repo.get_inv_parts_list()
    inv_list = inv_repo.get_inv_location_id_list()
    part_list_len = len(parts)
    inv_max_count = len(inv_list)
    count=0
    array_len = part_list_len*inv_max_count;
    results = [0 for x in range(array_len)]

    for part in range(0, part_list_len):
        for inv_count in range(0,inv_max_count):
            part_number = parts[part]['partNumber']
            inv_location = inv_list[inv_count]['id']
            results[count] = inv_repo.get_inventory_values_by_location(part_number, inv_location)
            print results
            count = count + 1


    assert len(results) < 100