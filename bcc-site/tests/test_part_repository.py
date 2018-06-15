from bcc.dataaccess import part_repository

def test_get_part_detail():
    part_repo = part_repository.PartRepository()
    part = part_repo.get_part_by_part_number('1010020')
    assert part['partNumber'] == 1010020
    assert part['description'] == 'M3-0.5 X 14MM BLACK OXIDE SOCKET FLAT HEAD MACHINE'

def test_part_not_found_returns_null():
    part_repo = part_repository.PartRepository()
    part = part_repo.get_part_by_part_number('shouldnotexist')
    assert not part

def test_part_has_part_prefix():
    part_repo = part_repository.PartRepository()
    parts = part_repo.get_parts_by_part_number_prefix('101')
    assert len(parts) > 2

def test_get_part():
    part_repo = part_repository.PartRepository()
    page = 2
    number_of_parts = 20
    part_start = (page - 1) * number_of_parts
    parts = part_repo.get_parts(part_start, number_of_parts)
    assert len(parts) < 21
