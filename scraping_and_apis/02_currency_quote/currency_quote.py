import requests
import backoff

@backoff.on_exception(backoff.expo, (requests.exceptions.RequestException), max_tries=5)
def quote(value, currency):
    response = requests.get(f'https://economia.awesomeapi.com.br//{currency}')
    if response:
        raw_data = response.json()
        dollar = raw_data[currency.replace('-', '')]['bid']
        return f"{value} {currency[:3]} costs {(float(dollar)*value):.2f} {currency[4:]} today."
    else:
        return "Error"

def main():
    value = float(input("Value: "))
    currency = input("Currency: ")
    print(quote(value, currency))

if __name__ == '__main__':
    main()