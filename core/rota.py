import ipaddress

class Rota:
    """
        Representa uma única entrada de roteamento.
        Armazena a rede de destino, o próximo salto e os critérios de decisão (AD e Métrica).
    """

    def __init__(self, rede_str: str, proximo_salto: str, ad: int, metrica: int):
        """
            Inicializa uma Rota.

            Args:
                rede_str (str): A rede de destino em formato CIDR (ex: "192.168.1.0/24").
                proximo_salto (str): O IP do próximo salto ou "Conectada".
                ad (int): A Distância Administrativa (confiabilidade).
                metrica (int): O custo para alcançar a rede.
        """

        self.rede           = ipaddress.ip_network(rede_str)
        self.proximo_salto  = proximo_salto
        self.ad             = ad
        self.metrica        = metrica
        self.prefixo_len    = self.rede.prefixlen

    def __repr__(self):
        """Representação em string amigável para debug."""
        return f"Rota(Rede={self.rede}, Salto={self.proximo_salto}, AD={self.ad}, Métrica={self.metrica})"