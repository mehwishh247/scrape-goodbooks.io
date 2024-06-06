from bs4 import BeautifulSoup
import requests
import json

def scrape_books():
    book_data = []
    response = requests.get('https://www.goodbooks.io/books')
    soup = BeautifulSoup(response.content, 'html.parser')

    pages = int(soup.find('div', class_='w-page-count page-count').text.split('/')[1].strip())

    serial = 1
    for page in range(1, pages + 1):
        section = soup.find('div', class_='collection')
        books = section.find_all('div', class_='book-wrap')

        for book in books:
            name = book.find('h5', class_='grid-item-title').text.strip()
            author = book.find('h6', class_='grid-item-subtitle').text.strip()
            book_detail = 'https://www.goodbooks.io' + book.find('a')['href']
            
            buy_button = book.find('div', class_='row-btn-books')
            purchase_link = buy_button.find('a')['href']

            print({'Sr.': serial,'Name': name, 'Author\'s name': author, 'Details': book_detail, 'Amazon purchase link': purchase_link})
            
            book_data.append(
                {'Sr.': serial,
                 'Name': name, 
                 'Author\'s name': author, 
                 'Details': book_detail, 
                 'Amazon link': purchase_link
                 })
            serial += 1

        link = f'https://www.goodbooks.io/books?216112dc_page={page+1}'
        soup = BeautifulSoup(requests.get(link).content, 'html.parser')

    return book_data

if __name__ =='__main__':
    data = scrape_books()

    with open('book-data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=3)