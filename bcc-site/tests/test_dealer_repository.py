
from bcc.dataaccess import dealer_repository


def test_get_all_dealers():
    dealer_repo = dealer_repository.DealerRepository()
    results = dealer_repo.get_dealer_list(0, 5)
    assert len(results) == 5
