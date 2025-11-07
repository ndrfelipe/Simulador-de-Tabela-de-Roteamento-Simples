import sys
from pathlib import Path
import json
import pytest

# Ajusta o sys.path para importar do core
sys.path.append(str(Path(__file__).resolve().parents[2]))

from core.rota import Rota
from core.Table import TabelaRoteamento


# ---------------------------------------------------------------
# Testes principais do roteamento
# ---------------------------------------------------------------

def test_encontrar_melhor_rota_prefixo():
    tabela = TabelaRoteamento()
    tabela.add_rota(Rota("192.168.1.0/24", "10.0.0.1", ad=1, metrica=10))
    tabela.add_rota(Rota("192.168.1.0/25", "10.0.0.2", ad=1, metrica=10))

    melhor = tabela.encontrar_melhor_rota("192.168.1.50")
    assert melhor.proximo_salto == "10.0.0.2"


def test_encontrar_melhor_rota_por_ad():
    tabela = TabelaRoteamento()
    tabela.add_rota(Rota("10.0.0.0/8", "via1", ad=90, metrica=10))
    tabela.add_rota(Rota("10.0.0.0/8", "via2", ad=100, metrica=5))

    melhor = tabela.encontrar_melhor_rota("10.1.2.3")
    assert melhor.proximo_salto == "via1"


def test_encontrar_melhor_rota_por_metrica():
    tabela = TabelaRoteamento()
    tabela.add_rota(Rota("172.16.0.0/16", "viaA", ad=110, metrica=30))
    tabela.add_rota(Rota("172.16.0.0/16", "viaB", ad=110, metrica=20))

    melhor = tabela.encontrar_melhor_rota("172.16.10.5")
    assert melhor.proximo_salto == "viaB"


def test_sem_rota_correspondente():
    tabela = TabelaRoteamento()
    tabela.add_rota(Rota("192.168.0.0/24", "viaX", ad=1, metrica=10))

    melhor = tabela.encontrar_melhor_rota("10.0.0.1")
    assert melhor is None


# ---------------------------------------------------------------
# Testes adicionais de funcionalidades
# ---------------------------------------------------------------

def test_adicionar_rota():
    tabela = TabelaRoteamento()
    rota = Rota("10.0.0.0/8", "via1", ad=1, metrica=10)
    tabela.add_rota(rota)
    assert rota in tabela.rotas


def test_carregar_json(tmp_path):
    tabela = TabelaRoteamento()
    arquivo = tmp_path / "rotas.json"
    rotas_data = [
        {"rede": "192.168.1.0/24", "proximo_salto": "10.0.0.1", "ad": 1, "metrica": 10},
        {"rede": "10.0.0.0/8", "proximo_salto": "via1", "ad": 90, "metrica": 5}
    ]
    arquivo.write_text(json.dumps(rotas_data))

    tabela.carregar_json(str(arquivo))
    assert len(tabela.rotas) == 2
    assert any(r.proximo_salto == "10.0.0.1" for r in tabela.rotas)
    assert any(r.proximo_salto == "via1" for r in tabela.rotas)


def test_empate_ad_e_metrica():
    tabela = TabelaRoteamento()
    r1 = Rota("192.168.0.0/16", "via1", ad=10, metrica=5)
    r2 = Rota("192.168.0.0/16", "via2", ad=10, metrica=5)
    tabela.add_rota(r1)
    tabela.add_rota(r2)

    melhor = tabela.encontrar_melhor_rota("192.168.1.1")
    assert melhor.proximo_salto == "via1"
