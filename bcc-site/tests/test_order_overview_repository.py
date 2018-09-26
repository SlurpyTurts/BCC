from bcc.dataaccess import order_repository

def test_get_order_list():
    order_repo=order_repository.OrderRepository()
    results = order_repo.get_order_overview(21,20)
    assert len(results) == 51