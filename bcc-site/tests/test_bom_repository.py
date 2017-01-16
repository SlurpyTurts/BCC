
from bcc.dataaccess import bom_repository

def test_get_children():
    bom_repo = bom_repository.BomRepository()
    results = bom_repo.get_children_of_parent(8000049, 0)
    assert len(results) > 2
    first_bom_level = results[0]
    assert first_bom_level.bom['quantity'] > 0


def test_build_simple_bom():
    bom_repo = bom_repository.BomRepository()
    results = bom_repo.get_bom_of_parent(8000119, 3)
    assert len(results) > 2
    assert results[0].bom['child'] == 8000129


def test_only_shows_bom_as_given_level():
    bom_repo = bom_repository.BomRepository()
    results = bom_repo.get_bom_of_parent(8000119, 1)
    assert len(results) > 2
    for result in results:
        assert result.level == 1