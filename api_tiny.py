import requests
import json
import time

def obter_lista_pedidos(TOKEN_TINY):
    print_list = []
    pagina = 1
    numero_paginas = 1

    while pagina <= numero_paginas:
        status = 0

        while status != '3':
            try:
                response = pesquisar_pedidos(TOKEN_TINY, pagina)
                status = response['status_processamento']

                if status == '3':
                    numero_paginas = response['numero_paginas']
                    print(f'Montando lista de impressão: {pagina}/{numero_paginas}')
                    pagina = pagina + 1
                    pedidos = response['pedidos']
                    qtd_pedidos = len(pedidos)
                    print(f'qtd_pedidos: {qtd_pedidos}')

                    for pedido_ in pedidos:
                        pedido = pedido_['pedido']
                        print_list.append(pedido)
                else:
                    time.sleep(10)
            except:
                time.sleep(10)
    
    return print_list

def obter_pedido_tiny(TOKEN_TINY, id_pedido):
    url = f'https://api.tiny.com.br/api2/pedido.obter.php?token={TOKEN_TINY}&id={id_pedido}&formato=json'

    payload = ''
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def pesquisar_pedidos(TOKEN_TINY, numeroEcommerce):
    situacao = 'aprovado'
    url = f'https://api.tiny.com.br/api2/pedidos.pesquisa.php?token={TOKEN_TINY}&formato=json&numeroEcommerce={numeroEcommerce}'

    payload = ''
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def alterar_pedido(TOKEN_TINY, id_pedido, pedido):
    url = f'https://api.tiny.com.br/api2/pedido.alterar.php?token={TOKEN_TINY}&formato=json&id={id_pedido}'

    payload = json.dumps(pedido)
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def atualizar_situacao(TOKEN_TINY, id_pedido, situacao):
    url = f'https://api.tiny.com.br/api2/pedido.alterar.situacao?token={TOKEN_TINY}&id={id_pedido}&formato=json&situacao={situacao}'

    payload = ''
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def incluir_marcadores(TOKEN_TINY, id_pedido, marcadores):
    url = f'https://api.tiny.com.br/api2/pedido.marcadores.incluir?token={TOKEN_TINY}&marcadores={json.dumps(marcadores)}&idPedido={id_pedido}&formato=JSON'

    payload = ''
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()
    
def incluir_pedido(TOKEN_TINY, pedido):
    url_params = ''
    for key, value in pedido.items():
        url_params += f'{key}={value}&'

    url = f'https://api.tiny.com.br/api2/pedido.incluir.php?token={TOKEN_TINY}&formato=json&pedido={json.dumps(pedido)}'
    # print(url)
    payload = ''
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url=url, headers=headers, data=payload)
    return response.json()

def pesquisar_produtos(TOKEN_TINY, pesquisa):
    url = f'https://api.tiny.com.br/api2/produtos.pesquisa.php?token={TOKEN_TINY}&formato=json&pesquisa={pesquisa}'

    payload = ''
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()
