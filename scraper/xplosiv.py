import requests
from bs4 import BeautifulSoup
import sys

def scrape_products(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'
    }
    
    response = requests.get(url, headers=headers)

    # Only proceed if we got a successful response
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        products = soup.find_all('li', class_='product-item')

        product_data = []

        for product in products:
            # Find the image URL
            image_tag = product.find('img', class_='product-image-photo')
            image_url = image_tag['src'] if image_tag else 'No Image Found'

            # Find the product name
            name_tag = product.find('a', class_='product-item-link')
            product_name = name_tag.text.strip() if name_tag else 'No Name Found'
            product_link = name_tag['href'] if name_tag and name_tag.has_attr('href') else 'No Link Found'

            # Find the lowest price
            price_tag = product.find('span', class_='price')
            price = price_tag.text[1:] if price_tag else 0

            product_data.append({
                'companyid': 1,
                'productname': product_name,
                'price': price,
                'image': image_url,
                'link': product_link
            })

        url = "http://localhost:8080/api/products"

        response = requests.post(url, headers=headers, json=product_data)

        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")

        return product_data
    

    else:
        print("Failed to retrieve the webpage")
        return []

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    products = scrape_products(url)

    for product in products:
        print(product)
