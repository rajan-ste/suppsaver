import requests
from bs4 import BeautifulSoup
import sys

def scrape_products(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        products = soup.find_all('div', class_='product-wrap')

        product_data = []

        for product in products:
            # Find the image URL
            image_tag = product.find('noscript')
            image_url = "https:" + image_tag.img.get('src') if image_tag else 'No Image Found'

            # Find the product name and link
            name_tag = product.find('a', class_='product-thumbnail__title')
            product_name = name_tag.text.strip() if name_tag else 'No Name Found'
            product_link = name_tag['href'] if name_tag and name_tag.has_attr('href') else 'No Link Found'
            product_link = "https://www.supplements.co.nz" + product_link if product_link else 'No Link Found'

            price_tag = product.find('span', class_='product-thumbnail__price')
            if price_tag:
                price_text = price_tag.text.strip()
                if "sold" in price_text.lower():  # Assuming 'sold out' status is indicated in the text
                    price = 0
                else:
                    # Extract the price value, remove the currency symbol
                    price = price_text[1:]  
            else:
                price = 'No Price Found' 


            product_data.append({
                'companyid': 2,
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