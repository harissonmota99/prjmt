# prjmt

## Descrição geral

Este projeto é um script de automação em Python que interage com um switch Cisco real ou simulado para configurar o hostname e VLANs através de um frontend web simples desenvolvido com Flask.

A aplicação permite que o usuário informe os dados das VLANs pelo navegador. Depois disso, o script gera os comandos Cisco, conecta ao switch usando a biblioteca Netmiko, aplica a configuração, salva a configuração na NVRAM e gera um backup local da configuração atual do switch.

## Funcionalidades

- Frontend web com Flask
- Configuração do hostname do switch
- Configuração das VLANs:
  - VLAN 10: VLAN_DADOS
  - VLAN 20: VLAN_VOZ
  - VLAN 50: VLAN_SEGURANCA
- Aplicação da configuração no switch via SSH
- Salvamento da configuração com `write memory`
- Geração de backup local com `show running-config`
- Gerenciamento do projeto com Git e GitHub

## Tecnologias utilizadas

- Python
- Flask
- Netmiko
- Git
- GitHub
- Switch Cisco real ou simulado

## Instalação das dependências

Antes de executar o projeto, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
