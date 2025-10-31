from .Table import TabelaRoteamento

class Roteador:
    """
    Simula o roteador.

    Ele "possui" uma tabela de roteamento e sua principal
    função é receber um IP de destino e consultar a tabela.
    """
    def __init__(self):
        self.tabela_roteamento = TabelaRoteamento()

    def carregar_rotas_estaticas(self, caminho_arquivo: str):
        """Instrui a tabela a se carregar a partir de um arquivo."""
        self.tabela_roteamento.carregar_json(caminho_arquivo)

    def simular_pacote(self, ip_destino: str):
        """Simula a chegada de um pacote."""
        self.tabela_roteamento.encontrar_melhor_rota(ip_destino)