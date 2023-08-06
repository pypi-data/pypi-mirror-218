from stringstandard import stringstd


def test_full_name():
    name = "Kelly Frazão"
    std_name = stringstd.padronizar(name)
    assert len(std_name.split(' ')) > 1
