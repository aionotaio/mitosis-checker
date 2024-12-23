from loguru import logger

from src.utils import Utils
from src.client import Client
from src.vars import WALLETS_PATH, LOGS_PATH, RESULTS_PATH


logger.add(sink=LOGS_PATH, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", level="INFO", rotation="100 MB")

def process_wallets(addresses):
    for address in addresses:
        logger.info(f'Processing wallet: {address}...')
        client = Client(address=address)
        res = client.make_request()
        
        if res is None:
            continue
        
        csv_data = client.print_table(res)
        client.write_to_csv(csv_data, RESULTS_PATH)
        logger.success(f'Data for wallet {address} processed and written to CSV.')

def main():
    logger.info('Start checking...')
    addresses = Utils.read_strings_from_file(WALLETS_PATH)
    process_wallets(addresses)
    logger.info('Ended checking.')

if __name__ == '__main__':
    main()
