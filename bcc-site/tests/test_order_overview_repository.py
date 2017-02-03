from bcc.dataaccess import order_repository

def test_get_order_list():
    order_detail_repo = order_repository.OrderOverviewRepository()
    results = order_detail_repo.get_order_overview()
    assert len(results) == 51