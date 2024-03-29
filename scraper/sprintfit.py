import requests
from bs4 import BeautifulSoup
import sys
import os
from dotenv import load_dotenv
    
def scrape_products(url):

    load_dotenv()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        products = soup.find_all('div', class_='product')

        product_data = []

        for product in products:
            # Find the image URL
            image_tag = product.find('img', class_='img-responsive')
            image_url = image_tag['src'] if image_tag else 'No Image Found'

            # Find the product link
            link_tag = product.find('a', class_='product-content')
            product_link = 'https://www.sprintfit.co.nz/' + link_tag['href'] if link_tag and link_tag.has_attr('href') else 'No Link Found'

            # Find the product name
            name_tag = product.find('div', class_='name')
            if name_tag:
                # Assuming the direct text within the 'name' class div is the brand
                brand = name_tag.text.strip() if name_tag else ''
                # Find the 'strong' tag for the product name
                product_name_element = name_tag.find('strong')
                if product_name_element:
                    product_name = product_name_element.text.strip()
                    # Remove the product_name from the brand text
                    brand = brand.replace(product_name, '').strip()
            else:
                brand = ''
                product_name = ''

            full_name = f"{brand} {product_name}".strip()

            # Find the lowest price (special price if available, else normal price)
            price_tag = product.find('span', class_='price special')
            if not price_tag:  # If no special price is found, use the regular price
                price_tag = product.find('span', class_='price')
            if price_tag:
                price_text = price_tag.get_text(" ", strip=True)
                prices = [p.strip() for p in price_text.split() if p.startswith('$')]
                lowest_price = min(prices, key=lambda x: float(x.strip('$').replace(',', '')))[1:] if prices else 'No Price Found'
            else:
                lowest_price = 'No Price Found'

            product_data.append({
                'companyid': 3,  
                'productname': full_name,
                'price': lowest_price,
                'image': image_url,
                'link': product_link
            })

        
        api_key = os.getenv('API_KEY')
        headers['api-key'] = api_key

        api_url = os.getenv('API_URL')
        url = api_url + "/products/update-price"

        response = requests.put(url, headers=headers, json=product_data)
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

