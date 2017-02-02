from bcc.dataaccess import order_detail_repository

def test_get_order_list():
    order_detail_repo = order_detail_repository.OrderDetailRepository()
    results = order_detail_repo.get_order_detail(1038)
    assert len(results) == 3