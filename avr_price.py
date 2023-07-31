import json

with open('OUT_FILE_NAME', 'r') as f:
    templates = json.load(f)

print(templates)


def avr_price():
    amount_of_products = len(templates)
    price_of_all_products = 0

    for item in templates:
        price_of_all_products += item['amount']
    avr = price_of_all_products / amount_of_products
    print(f"Average price is {int(avr)}")
    return avr


avr_price()