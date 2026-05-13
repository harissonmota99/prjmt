from flask import Flask, request
from netmiko import ConnectHandler

app = Flask(__name__)


def gerar_comandos(hostname, vlans):
    comandos = []

    comandos.append(f"hostname {hostname}")

    for vlan_id, vlan_nome in vlans:
        comandos.append(f"vlan {vlan_id}")
        comandos.append(f"name {vlan_nome}")
        comandos.append("exit")

    return comandos
def aplicar_no_switch(comandos):
    switch = {
        "device_type": "cisco_ios",
        "host": "192.168.254.34",
        "username": "harisson",
        "password": "m0t@2026",
    }

    conexao = ConnectHandler(**switch)
    resultado = conexao.send_config_set(comandos)
    conexao.save_config()
    conexao.disconnect()

    return resultado


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = ""

    if request.method == "POST":
        hostname = request.form["hostname"]

        vlans = [
            (request.form["vlan10_id"], request.form["vlan10_nome"]),
            (request.form["vlan20_id"], request.form["vlan20_nome"]),
            (request.form["vlan50_id"], request.form["vlan50_nome"]),
        ]

        comandos = gerar_comandos(hostname, vlans)

        resultado = "\n".join(comandos)
    try:
        retorno_switch = aplicar_no_switch(comandos)
        resultado += "\n\nConfiguração aplicada no switch com sucesso!\n\n"
        resultado += retorno_switch
    except Exception as erro:
        resultado += f"\n\nErro ao aplicar no switch:\n{erro}"

    return f"""
    <html>
    <head>
        <title>Configuração de VLANs Cisco</title>
    </head>
    <body>
        <h1>Configuração de VLANs Cisco</h1>

        <form method="POST">
            <label>Hostname do Switch:</label><br>
            <input type="text" name="hostname" value="SWITCH_AUTOMATIZADO"><br><br>

            <h3>VLAN 10</h3>
            <label>ID:</label><br>
            <input type="text" name="vlan10_id" value="10"><br>
            <label>Nome:</label><br>
            <input type="text" name="vlan10_nome" value="VLAN_DADOS"><br><br>

            <h3>VLAN 20</h3>
            <label>ID:</label><br>
            <input type="text" name="vlan20_id" value="20"><br>
            <label>Nome:</label><br>
            <input type="text" name="vlan20_nome" value="VLAN_VOZ"><br><br>

            <h3>VLAN 50</h3>
            <label>ID:</label><br>
            <input type="text" name="vlan50_id" value="50"><br>
            <label>Nome:</label><br>
            <input type="text" name="vlan50_nome" value="VLAN_SEGURANCA"><br><br>

            <button type="submit">Gerar Configuração</button>
        </form>

        <h2>Comandos Gerados:</h2>
        <pre>{resultado}</pre>
    </body>
    </html>
    """


app.run(host="0.0.0.0", port=5000, debug=True)
