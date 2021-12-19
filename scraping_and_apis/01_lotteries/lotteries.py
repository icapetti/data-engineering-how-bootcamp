import requests
import collections
import pandas as pd

def get_lotofacil_data() -> pd.DataFrame:
    """
    Request the url of Loto Fácil and transform the content of the response into a dataframe
    """
    url = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbz8vTxNDRy9_Y2NQ13CDA0sTIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN_FydLAGAgNTKEK8DkRrACPGwpyQyMMMj0VAcySpRM!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K85260Q5OIRSC42046/res/id=historicoHTML/c=cacheLevelPage/=/'
    r = requests.get(url)

    return pd.read_html(r.text, header=0)[0] if r.status_code == 200 else None

def even_or_odd(number: int) -> str:
    """
    Checks whether a number is odd or even.
    """
    return 'even' if number % 2 == 0 else 'odd'

def is_prime(number: int) -> bool:
    """
    Checks if a number is prime. 0, 1 and negative numbers are discarded in the first check.
    It is then checked whether the number is divisible by any number other than itself.
    """
    if number < 2:
        return False

    for i in range(2, number):
        if number % i == 0:
            return False

    return True

COLUMNS_DRAWN_NUMBERS = [
    'Bola1',
    'Bola2',
    'Bola3',
    'Bola4',
    'Bola5',
    'Bola6',
    'Bola7',
    'Bola8',
    'Bola9',
    'Bola10',
    'Bola11',
    'Bola12',
    'Bola13',
    'Bola14',
    'Bola15']

def main():
    df = get_lotofacil_data()
    if df is None:
        print('Error while requesting the data')
        return

    numbers_drawn = []
    stats = []
    total_stats = {
        'even': 0,
        'odd': 0,
        'prime': 0,
    }
    
    for index, row in df.iterrows():
        even_numbers = [number for number in row[COLUMNS_DRAWN_NUMBERS] if even_or_odd(number) == 'even']
        odd_numbers = [number for number in row[COLUMNS_DRAWN_NUMBERS] if even_or_odd(number) == 'odd']
        prime_numbers = [number for number in row[COLUMNS_DRAWN_NUMBERS] if is_prime(number)]

        for n in row[COLUMNS_DRAWN_NUMBERS]:
            numbers_drawn.append(n)

        stats.append(
            f"{len(even_numbers)}even-{len(odd_numbers)}odd-{len(prime_numbers)}prime"
        )

        total_stats = {
            'even': total_stats['even'] + len(even_numbers),
            'odd': total_stats['odd'] + len(odd_numbers),
            'prime': total_stats['prime'] + len(prime_numbers),
        }

    combinations = pd.DataFrame(collections.Counter(stats).items(), columns=['combination', 'count'])
    combinations['frequency'] = combinations['count'] / combinations['count'].sum()
    combinations.sort_values(by='frequency', ascending=False, inplace=True)

    numbers_drawn_sorted = collections.Counter(numbers_drawn).most_common()

    print(
        f"""
        Lottery Statistics
        {'='*70}
        Most drawn number: {numbers_drawn_sorted[0][0]}
        Least drawn number: {numbers_drawn_sorted[-1][0]}
        Most frequent combination: {combinations.iloc[0]['combination']} - {(combinations.iloc[0]['frequency']*100):.2f}%
        Least frequent combination: {combinations.iloc[-1]['combination']} - {(combinations.iloc[-1]['frequency']*100):.2f}%
        Total even numbers: {total_stats['even']} - {(total_stats['even']/len(numbers_drawn)*100):.2f}%
        Total Odd numbers: {total_stats['odd']} - {(total_stats['odd']/len(numbers_drawn)*100):.2f}%
        Total Prime numbers: {total_stats['prime']} - {(total_stats['prime']/len(numbers_drawn)*100):.2f}%
        """
    )

if __name__ == '__main__':
    main()
