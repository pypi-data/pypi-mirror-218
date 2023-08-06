from stringstandardization import stringstd


def test_full_name():
    name = 'Sylvio Rúbens'
    std_name = stringstd.standardize(name)
    assert len(std_name.split(' ')) > 1
