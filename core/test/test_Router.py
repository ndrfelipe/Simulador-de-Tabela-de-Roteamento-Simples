import pytest
from core.rota import Rota
import ipaddress

def test_criacao_rota():
    """
    Testa se a Rota é criada corretamente com os atributos esperados.
    """
    rota = Rota("192.168.1.0/24", "192.168.1.1", 1, 10)
    assert isinstance(rota.rede, ipaddress.IPv4Network)
    assert str(rota.rede) == "192.168.1.0/24"
    assert rota.proximo_salto == "192.168.1.1"
    assert rota.ad == 1
    assert rota.metrica == 10
    assert rota.prefixo_len == 24

def test_repr_rota():
    """
    Testa a representação em string (__repr__) da Rota.
    """
    rota = Rota("10.0.0.0/8", "Conectada", 0, 0)
    repr_str = repr(rota)
    assert "10.0.0.0/8" in repr_str
    assert "Conectada" in repr_str
    assert "AD=0" in repr_str
    assert "Métrica=0" in repr_str

def test_rota_ipv6():
    """
    Testa se a classe suporta IPv6.
    """
    rota = Rota("2001:db8::/32", "Conectada", 1, 5)
    assert str(rota.rede) == "2001:db8::/32"
    assert rota.proximo_salto == "Conectada"
    assert rota.ad == 1
    assert rota.metrica == 5
    assert rota.prefixo_len == 32
