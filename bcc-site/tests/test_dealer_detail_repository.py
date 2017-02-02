
from bcc.dataaccess import dealer_detail_repository


def test_get_all_dealers():
    dealer_detail_repo = dealer_detail_repository.DealerDetailRepository()
    results = dealer_detail_repo.get_dealer_detail(1)
    assert len(results) == 1

def test_get_order_list():
    dealer_detail_repo = dealer_detail_repository.DealerDetailRepository()
    results = dealer_detail_repo.get_order_list(1)
    assert len(results) == 11