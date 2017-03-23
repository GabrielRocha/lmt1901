from estacoes import ESTACOES


class TestEstacoes():
    def test_total_ESTACOES(self):
        assert len(ESTACOES.keys()) == 6

    def test_type_ESTACOES(self):
        assert type(ESTACOES) is dict

    def test_keys(self):
        assert ("83049", 'AVELAR (P.DO ALFERES)') in ESTACOES.items()
        assert ("83698", 'CAMPOS') in ESTACOES.items()
        assert ("83718", 'CORDEIRO') in ESTACOES.items()
        assert ("83695", 'ITAPERUNA') in ESTACOES.items()
        assert ("83738", 'RESENDE') in ESTACOES.items()
        assert ("83743", 'RIO DE JANEIRO') in ESTACOES.items()