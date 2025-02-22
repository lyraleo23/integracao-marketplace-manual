import os
import re
import time
import datetime
import pandas as pd
from dotenv import load_dotenv
from api_manual import obter_pedidos
from api_tiny import pesquisar_produtos, pesquisar_pedidos, incluir_pedido
import json

load_dotenv()
TOKEN_TINY = os.getenv('TOKEN_TINY')
TOKEN_MANUAL = os.getenv('TOKEN_MANUAL')

def main():
    os.system('cls')

    # Obter o access_token da tiny 
    id_integrador = 15575

    download_list = [
        ['data_pedido', 'Tiny', 'Patient Name', 'Order ID', 'Prescription PDF', 'Receipt Link', 'doctors_crm', 'CPF']
    ]

    lista_pedidos_manual = []

    while len(lista_pedidos_manual) == 0:
        year = '2025'
        month = '01'
        day = '15'
        lista_pedidos_manual = obter_pedidos(TOKEN_MANUAL, year, month, day)

        # Salva o arquivo json da requisição
        with open('lista_pedidos_manual.json', 'w') as json_file:
            json.dump(lista_pedidos_manual, json_file, ensure_ascii=True, indent=4)

        # Obtém a quantidade de pedidos na lista
        lista_pedidos_manual = lista_pedidos_manual['data']
        print(f'Quantidade de pedidos: {len(lista_pedidos_manual)}')

    k=1
    for pedido_manual in lista_pedidos_manual:
        print(f'====== {k}/{len(lista_pedidos_manual)} ======')
        print(f"Pedido Manual: {pedido_manual['Order ID']}")
        k=k+1

        # Data do pedido
        data_pedido = pedido_manual['Added to CSV Date'].split()[0]
        data_pedido = data_pedido.replace('-','/')

        try:
            # Busca o pedido na Tiny
            while True:
                busca_pedido = pesquisar_pedidos(TOKEN_TINY, pedido_manual['Order ID'])
                busca_pedido = busca_pedido['retorno']
                busca_pedido_status = busca_pedido['status']
                time.sleep(1)
                break
            
            # Se já houver pedido, segue para o próximo
            if busca_pedido_status == 'OK':
                if len(busca_pedido['pedidos']) > 0:
                    print('continue')
                    # Adiciona o pedido na lista de downloads
                    download_list.append([data_pedido, busca_pedido['pedidos'][0]['pedido']['numero'], pedido_manual['Patient Name'], pedido_manual['Order ID'], pedido_manual['Prescription PDF'], pedido_manual['Receipt Link'], pedido_manual['doctors_crm'], re.sub(r'\D', '', pedido_manual['CPF'])])
                    continue
        except Exception as e:
            print(f'Erro ao buscar pedido na tiny: {e}')

        # Gera a lista de itens para a Tiny
        itens_tiny = []
        for produto in pedido_manual['Items']:

            pesquisa = produto['sku']
            while True:
                try:
                    produto_tiny = pesquisar_produtos(TOKEN_TINY, pesquisa)
                    time.sleep(2)
                    produto_tiny = produto_tiny['retorno']['produtos'][0]['produto']
                    descricao = produto_tiny['nome']
                    unidade = produto_tiny['unidade']
                    valor_unitario = produto_tiny['preco']
                    id_produto = produto_tiny['id']
                    break
                except:
                    print(f"Tentando novamente pesquisar produto... pedido {pedido_manual['Order ID']}")

            item = {
                'item' :{
                    'id_produto': id_produto,
                    'codigo': produto['sku'],
                    'descricao': descricao,
                    'unidade': unidade,
                    'quantidade': 1,
                    'valor_unitario': valor_unitario
                }
            }
            itens_tiny.append(item)

        # Gera o json do pedido que será criado na Tiny
        pedido = {
            'pedido': {
                'data_pedido': data_pedido,
                'cliente': {
                    'nome': pedido_manual['Patient Name'],
                    'tipo_pessoa': 'F',
                    'cpf_cnpj': pedido_manual['CPF'],
                    'endereco': pedido_manual['Address'],
                    'numero': '-',
                    'complemento': pedido_manual['Apt'].replace('&', 'e'),
                    'bairro': '---',   #não tem pedido_manual['']
                    'cep': pedido_manual['Postcode'],
                    'cidade': pedido_manual['City'],
                    'uf': pedido_manual['County'],
                    'pais': 'Brasil',
                    'fone': pedido_manual['Phone'],
                    'email': pedido_manual['Email'],
                    'atualizar_cliente': 'S',
                    'itens': itens_tiny
                },
                'itens': itens_tiny,
                'marcadores': [
                    {
                        'marcador': {
                            'descricao': 'Produto Manual'
                        }
                    },
                    {
                        'marcador': {
                            'descricao': 'Projetos Especiais'
                        }
                    },
                    {
                        'marcador': {
                            'descricao': 'Manual'
                        }
                    }
                ],
                'forma_pagamento': 'Marketplace',
                'frete_por_conta': 'D',
                'forma_frete': 'Total Express - Manual',
                'numero_ordem_compra': pedido_manual['Order ID'],
                'obs': pedido_manual['doctors_crm'],
                'obs_internas': f"Prescription PDF: {pedido_manual['Prescription PDF']}",
                'situacao': 'aprovado',
                'numero_pedido_ecommerce': pedido_manual['Order ID'],
                'id_ecommerce': 15575,
                'ecommerce': 'Manual'
            }
        }

        while True:
            try:
                # Busca o pedido na Tiny
                busca_pedido = pesquisar_pedidos(TOKEN_TINY, pedido_manual['Order ID'])
                busca_pedido = busca_pedido['retorno']
                time.sleep(1)

                if busca_pedido['status'] == 'Erro':
                    # Cria o pedido na Tiny
                    try:
                        response = incluir_pedido(TOKEN_TINY, pedido)
                        response = response['retorno']['registros']['registro']

                        if response['erros']:
                            print(response['erros'][0]['erro'])
                            if response['erros'][0]['erro'] == 'Registro em duplicidade - Pedido de Venda já cadastrado':
                                break

                        # for item in itens_tiny:
                        #     codigo_sku = item['item']['descricao'][:7]
                        #     print(codigo_sku)
                        break
                    except Exception as e:
                        print(f'Erro na inclusao do pedido: {e}')
                        time.sleep(2)

                    # Adiciona o pedido na lista de downloads
                    download_list.append([data_pedido, response['numero'], pedido_manual['Patient Name'], pedido_manual['Order ID'], pedido_manual['Prescription PDF'], pedido_manual['Receipt Link'], pedido_manual['doctors_crm'], re.sub(r'\D', '', pedido_manual['CPF'])])
                    break
                elif busca_pedido['status'] == 'OK':
                    if len(busca_pedido['pedidos']) > 0:
                        # Adiciona o pedido na lista de downloads
                        download_list.append([data_pedido, busca_pedido['pedidos'][0]['pedido']['numero'], pedido_manual['Patient Name'], pedido_manual['Order ID'], pedido_manual['Prescription PDF'], pedido_manual['Receipt Link'], pedido_manual['doctors_crm'], re.sub(r'\D', '', pedido_manual['CPF'])])
                        break
            except Exception as e:
                print(f"Tentando novamente... pedido {pedido_manual['Order ID']}")
                print(e)
                time.sleep(2)

    df2 = pd.DataFrame(download_list)
    df2.to_excel('.\output\download_list.xlsx', index=True, header=False)
    df2.to_excel('.\output\download_list_backup.xlsx', index=True, header=False)


main()
