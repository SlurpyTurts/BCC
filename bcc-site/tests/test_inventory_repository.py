
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

