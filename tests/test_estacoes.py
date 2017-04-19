from core.estacoes import ESTACOES
import pytest


def test_total_estacoes():
    assert len(ESTACOES.keys()) == 6

def test_type_estacoes():
    assert type(ESTACOES) is dict

@pytest.mark.parametrize("input", [
    ("83049", 'AVELAR (P.DO ALFERES)'),
    ("83698", 'CAMPOS'),
    ("83718", 'CORDEIRO'),
    ("83695", 'ITAPERUNA'),
    ("83738", 'RESENDE'),
    ("83743", 'RIO DE JANEIRO')
])
def test_contains_keys(input):
    assert input in ESTACOES.items()
