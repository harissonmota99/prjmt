# Plano de Automação de VPN IPSec entre Fortigate e Palo Alto

## 1. Descrição geral

Este documento apresenta um plano para automatizar a configuração de uma VPN IPSec site-to-site entre um firewall Fortigate e um firewall Palo Alto.

O objetivo é documentar os parâmetros necessários, as ferramentas que poderiam ser utilizadas, os passos lógicos da automação, as validações da configuração e os alertas em caso de falha ou divergência.

Neste planejamento, não serão consideradas as configurações iniciais das interfaces WAN e LAN, pois entende-se que os firewalls já estão configurados como gateways das respectivas redes locais.

---

## 2. Endereçamento proposto

### Firewall Palo Alto

- Equipamento: FW-PA
- IP público WAN: `200.200.200.2/30`
- Rede local lado PA: `192.168.10.0/24`
- IP do túnel PTP: `169.254.1.1/30`

### Firewall Fortigate

- Equipamento: FW-FGT
- IP público WAN: `200.100.100.2/30`
- Rede local lado FGT: `192.168.20.0/24`
- IP do túnel PTP: `169.254.1.2/30`

### Rede de túnel

- Rede PTP do túnel: `169.254.1.0/30`
- Palo Alto: `169.254.1.1`
- Fortigate: `169.254.1.2`

### Chave pré-compartilhada

- PSK: `m0t@2026`

---

## 3. Parâmetros necessários para a VPN

O script de automação deverá carregar os seguintes parâmetros:

1. IPs públicos WAN dos firewalls.
2. Redes locais de cada lado.
3. IPs /30 do túnel entre os firewalls.
4. Parâmetros da Fase 1.
5. Parâmetros da Fase 2.
6. Chave pré-compartilhada.
7. Credenciais de acesso aos firewalls.
8. Nome da VPN e das interfaces de túnel.
9. Rotas e políticas de segurança.

---

## 4. Proposta de Phase 1

A Phase 1 será responsável por criar um canal seguro entre os dois firewalls. Nessa fase ainda não ocorre a criptografia do tráfego das redes internas; ela serve para estabelecer a negociação segura entre os pares VPN.

Parâmetros sugeridos:

| Parâmetro | Valor |
|---|---|
| Versão IKE | IKEv2 |
| Autenticação | Pre-shared key |
| Chave pré-compartilhada | `m0t@2026` |
| Criptografia | AES-256 |
| Hash / Autenticação | SHA-256 |
| Grupo Diffie-Hellman | 14 |
| Lifetime | 28800 segundos |
| NAT-T | Habilitado |
| DPD | Habilitado |

---

## 5. Proposta de Phase 2

A Phase 2 será responsável por definir os parâmetros de criptografia aplicados ao tráfego entre as redes locais dos dois firewalls.

Parâmetros sugeridos:

| Parâmetro | Valor |
|---|---|
| Criptografia | AES-256 |
| Hash / Autenticação | SHA-256 |
| PFS | Habilitado |
| Grupo PFS | 14 |
| Lifetime | 3600 segundos |
| Rede local lado PA | `192.168.10.0/24` |
| Rede local lado FGT | `192.168.20.0/24` |

---

## 6. Ferramentas e APIs possíveis

### 6.1 Fortigate

Para automatizar a configuração no Fortigate, poderiam ser utilizadas as seguintes opções:

- FortiOS REST API
- SSH com Python
- Biblioteca Netmiko

Me baseei aqui nesta doc:

- FortiOS REST API: `https://docs.fortinet.com/document/fortigate/7.2.0/secgw-for-mobile-networks-deployment/238243/fortios-rest-api`

### 6.2 Palo Alto

Para automatizar a configuração no Palo Alto, poderiam ser utilizadas as seguintes opções:

- PAN-OS REST API
- PAN-OS XML API
- SSH com bibliotecas Python

Referência:

- PAN-OS REST API: `https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-panorama-api/get-started-with-the-pan-os-rest-api`

---

## 7. Passos de automação no Fortigate

No lado do Fortigate, o script deveria executar as seguintes tarefas:

1. Criar os objetos de endereço para a rede local e a rede remota.
2. Criar a configuração de Phase 1.
3. Criar a configuração de Phase 2.
4. Criar ou associar uma interface de túnel.
5. Configurar o IP da interface de túnel como `169.254.1.2/30`.
6. Criar rota estática para a rede remota `192.168.10.0/24`.
7. Criar política de firewall permitindo tráfego entre a LAN local e a VPN.
8. Salvar a configuração.

---

## 8. Passos de automação no Palo Alto

No lado do Palo Alto, o script deveria executar as seguintes tarefas:

1. Criar objetos de endereço para as redes locais e remotas.
2. Criar o IKE Crypto Profile.
3. Criar o IPSec Crypto Profile.
4. Criar o IKE Gateway apontando para o IP WAN do Fortigate.
5. Criar a interface de túnel.
6. Configurar o IP da interface de túnel como `169.254.1.1/30`.
7. Criar o IPSec Tunnel.
8. Criar rota estática para a rede remota `192.168.20.0/24`.
9. Criar políticas de segurança permitindo tráfego entre as zonas.
10. Realizar commit da configuração.

---

## 9. Fluxo geral do script

O fluxo lógico do script de automação seria:

1. Ler os parâmetros da VPN.
2. Validar se os parâmetros obrigatórios foram preenchidos.
3. Conectar ao Fortigate.
4. Aplicar a configuração da VPN no Fortigate.
5. Conectar ao Palo Alto.
6. Aplicar a configuração da VPN no Palo Alto.
7. Salvar ou realizar commit das configurações.
8. Validar se a VPN foi criada nos dois firewalls.
9. Testar conectividade entre as redes.
10. Gerar relatório de sucesso ou alerta.

---

## 10. Validação da configuração

Após aplicar a configuração, o script deverá validar se a VPN foi configurada corretamente nos dois firewalls.

A validação deverá verificar:

- Se a Phase 1 foi criada.
- Se a Phase 2 foi criada.
- Se a interface de túnel foi criada.
- Se o IP do túnel foi configurado corretamente.
- Se as rotas estáticas foram criadas.
- Se as políticas de firewall foram aplicadas.
- Se o túnel IPSec está ativo.
- Se existe conectividade entre as redes locais.

---

## 11. Comandos de validação no Fortigate

No Fortigate, poderiam ser utilizados comandos como:

show vpn ipsec phase1-interface
show vpn ipsec phase2-interface
get vpn ipsec tunnel summary
get router info routing-table all
show firewall policy

No PA seria os seguintes comandos:

show vpn ike-sa
show vpn ipsec-sa
show routing route
show interface tunnel
show running security-policy

12. Conclusão:
Este plano descreve a automação da configuração de uma VPN IPSec site-to-site entre um firewall Fortigate e um firewall Palo Alto.

O planejamento inclui a definição dos parâmetros da VPN, identificação das ferramentas e APIs possíveis, passos de configuração em cada firewall, estratégia de validação, tratamento de alertas e rollback em caso de falha.
