import ipaddress
import json
from .rota import Rota
from typing import List, Optional

class TabelaRoteamento:
    """
    Simula a tabela de roteamento (FIB) de um roteador.

    Armazena uma lista de objetos Rota e contém a lógica
    para encontrar a melhor correspondência.
    """

    def __init__(self):
        self.rotas: List[Rota] = []

    def add_rota(self, rota: Rota):
        """
            Adiciona uma rota à tabela.
        """
        self.rotas.append(rota)

    def carregar_json(self, caminho: str):
        """
        Carrega rotas estáticas de um arquivo JSON.

        O JSON deve ser uma lista de objetos, cada um com:
        "rede", "proximo_salto", "ad", "metrica".
        """

        print(f"Carregando rotas de {caminho}")

        try:
            with open(caminho, 'r') as f:
                dados_rotas = json.load(f)
                for r in dados_rotas:
                    nova_rota = Rota(
                        rede_str=r['rede'],
                        proximo_salto=r['proximo_salto'],
                        ad=r['ad'],
                        metrica=r['metrica']
                    )
                    self.add_rota(nova_rota)
            print(f"Total de {len(self.rotas)} rotas carregadas.")
        except FileNotFoundError:
            print(f"ERRO: Arquivo {caminho} não encontrado.")
        except Exception as e:
            print(f"ERRO ao ler o arquivo JSON: {e}")

    def encontrar_melhor_rota(self, ip_destino_str: str) -> Optional[Rota]:
        """
        Executa a lógica de decisão de roteamento.

        1. Encontra todas as rotas correspondentes (IP dentro da rede).
        2. Filtra pela correspondência de prefixo mais longa (Longest Prefix Match).
        3. Se houver empate, filtra pela menor Distância Administrativa (AD).
        4. Se houver empate, filtra pela menor Métrica.

        Retorna a melhor Rota ou None se nenhuma corresponder.
        """

        # Esse é apenas um esqueleto da lógica
        print(f"\n Procurando melhor rota para: {ip_destino_str}")
        try:
            ip_destino = ipaddress.ip_address(ip_destino_str)
        except:
            print(f"ERRO: IP de destino '{ip_destino_str}' inválido.")
            return None
        

        # Passo 1: Encontrar todas as rotas correspondentes
        rotas_correspondentes = [r for r in self.rotas if ip_destino in r.rede]

        if not rotas_correspondentes:
            print("Nenhuma rota encontrada (nem mesmo padrão). Pacote descartado.")
            return None
        
        print(f"Rotas correspondentes encontradas: {len(rotas_correspondentes)}")

        for r in rotas_correspondentes:
            print(F" -> {r}")
        
        # A lógica principal ainda será implementada, nas futuras demandas.

        # Base:

        # Passo 2: Encontrar o prefixo mais longo

        melhor_prefixo = max(r.prefixo_len for r in rotas_correspondentes)
        candidatas_prefixo = [r for r in rotas_correspondentes if r.prefixo_len == melhor_prefixo]

        # Passo 3: Encontrar a menor AD
        menor_ad = min(r.ad for r in candidatas_prefixo)
        candidatas_ad = [r for r in candidatas_prefixo if r.ad == menor_ad]

        # Passo 4: Encontrar a menor Métrica
        menor_metrica = min(r.metrica for r in candidatas_ad)
        candidatas_metrica = [r for r in candidatas_ad if r.metrica == menor_metrica]

        melhor_rota = candidatas_metrica[0]

        print(f"MELHOR ROTA: {melhor_rota.rede} via {melhor_rota.proximo_salto}")
        return melhor_rota