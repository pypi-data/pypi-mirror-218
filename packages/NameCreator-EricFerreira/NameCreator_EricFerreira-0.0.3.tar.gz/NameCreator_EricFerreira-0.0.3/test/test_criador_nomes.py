from src.criador_nomes import RandomNames


def test_generate_name():
    random_names = RandomNames()
    name = random_names.generate_name()
    assert name in ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Eric']


def test_generate_surname():
    random_names = RandomNames()
    surname = random_names.generate_surname()
    assert surname in ['Smith', 'Johnson', 'Brown',
                       'Taylor', 'Miller', 'Bryan']
