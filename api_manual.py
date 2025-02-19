import requests
import json

def obter_pedidos(TOKEN_MANUAL, year, month, day):
    # url = f'https://backend.manual.co/proxy/integration/vsm/miligrama?fromDate={year}-{month}-{day} 00:00:00&toDate={year}-{month}-{day} 23:59:59'
    url = f'https://backend.manual.co/proxy/integration/vsm/miligrama?fromDate={year}-{month}-{day} 00:00:00'

    payload = {}
    headers = {
        'Authorization': f'Bearer {TOKEN_MANUAL}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response)

    return response.json()
