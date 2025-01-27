import os
import re
import time
import datetime
import pandas as pd
from dotenv import load_dotenv
from api_manual import obter_pedidos
from api_tiny import pesquisar_produtos, pesquisar_pedidos, incluir_pedido
import csv

load_dotenv()
TOKEN_TINY = os.getenv('TOKEN_TINY')
TOKEN_MANUAL = os.getenv('TOKEN_MANUAL')

def main():
    os.system('cls')

    # Obter o access_token da tiny 
    id_integrador = 15575

    planilha_tiny = [
        ['ID', 'Número do pedido', 'Data', 'Data prevista', 'ID contato', 'Nome do contato*', 'Tipo de Pessoa', 'CPF/CNPJ', 'RG/IE', 'CEP', 'Município', 'UF', 'Endereço', 'Endereço Nro', 'Complemento', 'Bairro', 'Fone', 'Celular', 'e-mail', 'Desconto pedido (% ou valor)', 'Frete', 'Observações', 'Situação', 'ID produto', 'Descrição', 'Quantidade', 'Valor unitário', 'Desconto item %', 'Código de rastreamento', 'Número da ordem de compra', 'Vendedor', 'Despesas', 'Desconto do pedido rateado', 'Frete pedido rateado', 'Despesas pedido rateado', 'Destinatário', 'CPF/CNPJ entrega', 'CEP entrega', 'Município entrega', 'UF entrega', 'Endereço entrega', 'Endereço Nro entrega', 'Complemento entrega', 'Bairro entrega', 'Fone entrega', 'Código (SKU)']
    ]

    download_list = [
        ['Tiny', 'Patient Name', 'Order ID', 'Prescription PDF', 'Receipt Link', 'doctors_crm', 'doctors_crm_province']
    ]

    lista_pedidos_manual = []

    while len(lista_pedidos_manual) == 0:
        year = '2024'
        month = '01'
        day = '22'
        lista_pedidos_manual = obter_pedidos(TOKEN_MANUAL, year, month, day)
        lista_pedidos_manual = lista_pedidos_manual['data']
        print(f'Quantidade de pedidos: {len(lista_pedidos_manual)}')

    k=1
    for pedido_manual in lista_pedidos_manual:
        print(f'====== {k}/{len(lista_pedidos_manual)} ======')
        k=k+1
        print(f"Pedido Manual: {pedido_manual['Order ID']}")
        data_pedido = pedido_manual['Payment Date'].split()[0]
        data_pedido = data_pedido.replace('-','/')

        try:
            while True:
                busca_pedido = pesquisar_pedidos(TOKEN_TINY, pedido_manual['Order ID'])
                busca_pedido = busca_pedido['retorno']
                busca_pedido_status = busca_pedido['status']
                time.sleep(1)
                break

            if busca_pedido_status == 'OK':
                if len(busca_pedido['pedidos']) > 0:
                    print('continue')
                    
                    download_list.append([busca_pedido['pedidos'][0]['pedido']['numero'], pedido_manual['Patient Name'], pedido_manual['Order ID'], pedido_manual['Prescription PDF'], pedido_manual['Receipt Link'], pedido_manual['doctors_crm'], pedido_manual['doctors_crm_province']])
                    
                    continue
        except Exception as e:
            print(f'Erro ao buscar pedido na tiny: {e}')


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
                    print(pesquisa)

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

        pedido = {
            'pedido': {
                'data_pedido': data_pedido,
                'cliente': {
                    'nome': pedido_manual['Patient Name'],
                    'tipo_pessoa': 'F',
                    'cpf_cnpj': pedido_manual['CPF'],
                    'endereco': pedido_manual['Address'],
                    'numero': re.sub("[^0-9]", "", pedido_manual['Address']),
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
                busca_pedido = pesquisar_pedidos(TOKEN_TINY, pedido_manual['Order ID'])
                busca_pedido = busca_pedido['retorno']
                time.sleep(1)

                if busca_pedido['status'] == 'Erro':
                    try:
                        response = incluir_pedido(TOKEN_TINY, pedido)
                        print(response)
                        response = response['retorno']['registros']['registro']

                        if response['erros']:
                            print(response['erros'][0]['erro'])
                            if response['erros'][0]['erro'] == 'Registro em duplicidade - Pedido de Venda já cadastrado':
                                break

                        for item in itens_tiny:
                            codigo_sku = item['item']['descricao'][:7]
                            print(codigo_sku)

                            new_line = [response['id'], response['numero'], data_pedido, '', '', pedido_manual['Patient Name'], 'F', pedido_manual['CPF'], '', pedido_manual['Postcode'], pedido_manual['City'], pedido_manual['County'], pedido_manual['Address'], re.sub("[^0-9 ] ", "", pedido_manual['Address']), pedido_manual['Apt'], '-', pedido_manual['Phone'], '', pedido_manual['Email'], '', '', pedido_manual['Prescription PDF'], 'aprovado', item['item']['id_produto'], item['item']['descricao'], item['item']['quantidade'], item['item']['valor_unitario'], '', '', pedido_manual['Order ID'], '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', codigo_sku]
                            print(new_line)

                            planilha_tiny.append(new_line)
                            df = pd.DataFrame(planilha_tiny)
                            df.to_excel(f'pedidos_manual.xlsx', index=True, header=False)
                        break
                    except Exception as e:
                        print(f'Erro na inclusao do pedido: {e}')
                        time.sleep(2)

                    download_list.append([response['numero'], pedido_manual['Patient Name'], pedido_manual['Order ID'], pedido_manual['Prescription PDF'], pedido_manual['Receipt Link'], pedido_manual['doctors_crm'], pedido_manual['doctors_crm_province']])
                    break
                elif busca_pedido['status'] == 'OK':
                    if len(busca_pedido['pedidos']) > 0:
                        download_list.append([busca_pedido['pedidos'][0]['pedido']['numero'], pedido_manual['Patient Name'], pedido_manual['Order ID'], pedido_manual['Prescription PDF'], pedido_manual['Receipt Link'], pedido_manual['doctors_crm'], pedido_manual['doctors_crm_province']])
                        break

                    for item in itens_tiny:
                        codigo_sku = item['item']['descricao'][:7]
                        print(codigo_sku)

                        new_line = [response['id'], response['numero'], data_pedido, '', '', pedido_manual['Patient Name'], 'F', pedido_manual['CPF'], '', pedido_manual['Postcode'], pedido_manual['City'], pedido_manual['County'], pedido_manual['Address'], re.sub("[^0-9 ] ", "", pedido_manual['Address']), pedido_manual['Apt'], '-', pedido_manual['Phone'], '', pedido_manual['Email'], '', '', pedido_manual['Prescription PDF'], 'aprovado', item['item']['id_produto'], item['item']['descricao'], item['item']['quantidade'], item['item']['valor_unitario'], '', '', pedido_manual['Order ID'], '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', codigo_sku]
                        print(new_line)

                        planilha_tiny.append(new_line)
                        df = pd.DataFrame(planilha_tiny)
                        df.to_excel(f'pedidos_manual.xlsx', index=True, header=False)
            except Exception as e:
                print(f"Tentando novamente... pedido {pedido_manual['Order ID']}")
                print(e)
                print(pedido)
                time.sleep(2)


    # Horário da impressão
    now = datetime.datetime.now()
    now = str(now)
    now = now.split(' ')
    data = now[0]
    hora = now[1].split('.')
    hora = hora[0].replace(':','_')
    df = pd.DataFrame(planilha_tiny)
    df.to_excel(f'pedidos_manual.xlsx', index=True, header=False)

    df2 = pd.DataFrame(download_list)
    df2.to_excel('download_list.xlsx', index=True, header=False)
    df2.to_excel('download_list_backup.xlsx', index=True, header=False)


main()
