import csv

import requests
from loguru import logger
from tabulate import tabulate
from fake_useragent import UserAgent


class Client:
    def __init__(self, address: str) -> None:
        self.address = address
        self.user_agent = UserAgent().random

    def make_request(self) -> dict:
        headers = {
            'accept': 'application/json',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://murinxda.budibase.app',
            'priority': 'u=1, i',
            'referer': 'https://murinxda.budibase.app/app/mitosis-tools',
            'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-budibase-api-version': '1',
            'x-budibase-app-id': 'app_murinxda_21594ff11071456a9652335fdd643be8',
            'x-budibase-session-id': 'cd19d9af1a25746209e2347694db3bb3b',
            'x-budibase-type': 'client',
        }

        json_data = {
            'parameters': {
                'address': self.address,
            },
        }

        response = requests.post(
            'https://murinxda.budibase.app/api/v2/queries/query_datasource_0816da2f776f4244b69b7f9493007c29_29f5218b6a26483db1ed710d650e9827',
            headers=headers,
            json=json_data,
        )

        if response.status_code == 200:
            res = response.json()
            result_dict = {key: value for key, value in res.items() if key != 'count'}
            if result_dict['code'] == 200:
                return result_dict
            else:
                logger.warning(f'Getting data failed with status: {result_dict["code"]}. Probably not eligible.')
                return None
        else:
            logger.error(f'Request failed with status: {response.status_code}.')
            return None
    
    def print_table(self, data: dict) -> list:
        logger.info(f"Data for wallet {self.address}:")

        table_data = []
        csv_data = []
        
        wallet_data = data['data'][0]

        mito = f"{wallet_data['mito']:.2f}" if isinstance(wallet_data['mito'], (float, int)) else 'N/A'
        wmito = f"{wallet_data['wmito']:.2f}" if isinstance(wallet_data['wmito'], (float, int)) else 'N/A'
        rank = str(wallet_data['rank']) if wallet_data['rank'] != -1 else 'N/A'

        table_data.append(['$MITO Holdings', mito])
        table_data.append(['$WMITO Holdings', wmito])
        table_data.append(['Your MITO Rank', rank])

        csv_data.append([self.address, mito, wmito, rank])
        
        print(tabulate(table_data, headers=['Metric', 'Value'], tablefmt='pretty', stralign='left'))

        return csv_data

    def write_to_csv(self, csv_data: list, csv_path: str):
        with open(csv_path, 'a', newline='', encoding='utf-8-sig') as output_file:
            csv_writer = csv.writer(output_file, delimiter=';')
            if output_file.tell() == 0:
                csv_writer.writerow(['Address', 'MITO Holdings', 'WMITO Holdings', 'Your MITO Rank'])
            csv_writer.writerows(csv_data)
