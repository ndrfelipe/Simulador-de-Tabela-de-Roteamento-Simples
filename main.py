from core.Router import Roteador

def main():
    """
    Função principal que executa a simulação.
    """
    print("Iniciando Simulador de Roteador...")
    
    roteador = Roteador()
    roteador.carregar_rotas_estaticas("routes.json")
    
    # 3. Simula a chegada de pacotes (IPs de destino)
    ips_para_testar = [
        "192.168.1.50",    # Deve usar /24
        "10.1.1.100",      # Deve usar /16
        "192.168.1.70",    # Deve usar /32 (mais específica)
        "172.16.10.1",     # Deve testar AD (escolher estática sobre OSPF)
        "8.8.8.8"          # Deve usar a rota padrão /0
    ]
    
    for ip in ips_para_testar:
        roteador.simular_pacote(ip)

if __name__ == "__main__":
    main()