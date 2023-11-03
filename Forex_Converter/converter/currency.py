import requests

def get_currency_conversion(from_currency, to_currency, amount):
    try:
        response = requests.get('http://api.exchangerate.host/convert', params={
            'access_key': '843972097aca4e981f111f810627a70b',
            'from': from_currency,
            'to': to_currency,
            'amount': amount,
        })
        data = response.json()
        if 'result' in data:
            return data['result']
        else:
            return None
    except Exception as e:
        print(str(e))
        return None