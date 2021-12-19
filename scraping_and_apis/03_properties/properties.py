import logging
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup as bs

def set_log() -> logging.Logger:
    # Get de logging object with the app name
    log = logging.getLogger()
    # Set the logging level
    log.setLevel(logging.INFO)
    # Set the logging format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Set logging channel to console
    ch = logging.StreamHandler()
    # Add the logging format to console channel
    ch.setFormatter(formatter)
    # Add the output channel to the logger
    log.addHandler(ch)

    return log

def get_total_items(url) -> int:
    """
    """
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    return int(soup.find('strong', {
               'class': 'results-summary__count js-total-records'}).text.replace('.', ''))


def get_raw_items(url):
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    return soup.find_all(
        'a', {'class': 'property-card__content-link js-card-title'})


def parse_items(raw_item) -> list:
    """
    """
    description = raw_item.find(
        'span', {'class': 'property-card__title js-cardLink js-card-title'})
    address = raw_item.find('span', {'class': 'property-card__address'})
    area = raw_item.find(
        'span', {
            'class': 'js-property-card-detail-area'}).text.strip() + raw_item.find(
        'span', {
            'class': 'property-card__detail-text js-property-card-detail-text'}).text.strip()
    rooms = raw_item.find(
        'li', {
            'class': 'property-card__detail-item property-card__detail-room js-property-detail-rooms'})
    bathrooms = raw_item.find('li', {'class': 'js-property-detail-bathroom'})
    garages = raw_item.find('li', {'class': 'js-property-detail-garages'})
    price = raw_item.find('div', {'class': 'js-property-card__price-small'})
    condo_price = raw_item.find('strong', {'class': 'js-condo-price'})
    url = 'https://www.vivareal.com.br' + raw_item['href'].strip()

    item_parsed = [
        description.text.strip() if description else None,
        address.text.strip() if address else None,
        area.strip() if area else None,
        rooms.text.strip() if rooms else None,
        bathrooms.text.strip() if bathrooms else None,
        garages.text.strip() if garages else None,
        price.text.strip() if price else None,
        condo_price.text.strip() if condo_price else None,
        url
    ]

    return item_parsed


def main():
    log = set_log()

    BASE_URL = 'https://www.vivareal.com.br/venda/parana/curitiba/?pagina={}'

    df = pd.DataFrame(
        columns=[
            'description',
            'address',
            'area',
            'rooms',
            'bathrooms',
            'garages',
            'price',
            'condo_price',
            'url'
        ]
    )

    i = 1
    url = BASE_URL.format(i)
    total_items = get_total_items(url)
    log.info(f'Starting process to get {total_items} items...')

    while total_items > df.shape[0]:
        log.info(f'Getting data from page {url}')
        raw_items = get_raw_items(url)

        for raw_item in raw_items:
            item_parsed = parse_items(raw_item)
            log.debug(f'Item parsed: {item_parsed}')
            df.loc[len(df)] = item_parsed

        log.debug(f'{len(raw_items)} items on page {i}')
        i += 1

        url = BASE_URL.format(i)
        time.sleep(1.5)

    log.info(f'{df.shape[0]} items parsed on {i} pages')

    log.info('Saving dataframe to file...')
    filename = 'vivareal_properties_data.csv'
    df.to_csv(filename, sep=';', index=False)
    log.info(f'Dataframe saved to {filename} file.')

if __name__ == '__main__':
    main()
