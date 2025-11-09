
import requests
from bs4 import BeautifulSoup
def scrape_books(is_save: bool = False) -> list:
    """
    Собирает данные о всех книгах с сайта Books to Scrape.
    
    Args:
        is_save (bool): Если True, сохраняет данные в файл 'books_data.txt'
        
    Returns:
        list: Список словарей с информацией о книгах
    """
    
    all_books_data = []
    page_number = 1
    
    while True:
        # Формируем URL страницы
        if page_number == 1:
            page_url = "http://books.toscrape.com/index.html"
            base_url = "http://books.toscrape.com/"
        else:
            page_url = f"http://books.toscrape.com/catalogue/page-{page_number}.html"
            base_url = "http://books.toscrape.com/catalogue/"
        
        print(f"Парсим страницу {page_number}...")
        
        try:
            response = requests.get(page_url)
            
            # Проверяем успешность запроса
            if response.status_code != 200:
                print(f"Страница {page_number} не найдена (статус {response.status_code})")
                break
                
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Находим все карточки книг на странице
            book_cards = soup.find_all('article', class_='product_pod')
            
            # Если на странице нет книг, выходим
            if not book_cards:
                print("На странице нет книг - достигнут конец каталога")
                break
            
            # Парсим каждую книгу на странице
            successful_books = 0
            for card in book_cards:
                # Получаем ссылку на страницу книги
                book_relative_link = card.find('h3').find('a')['href']
                
                # ОБРАБАТЫВАЕМ ССЫЛКИ ДЛЯ ПЕРВОЙ И ОСТАЛЬНЫХ СТРАНИЦ ПО-РАЗНОМУ
                if page_number == 1:
                    # На первой странице ссылки вида: catalogue/a-light-in-the-attic_1000/index.html
                    full_book_url = "http://books.toscrape.com/" + book_relative_link
                else:
                    # На остальных страницах ссылки уже правильные
                    full_book_url = "http://books.toscrape.com/catalogue/" + book_relative_link
                
                # Получаем данные книги
                try:
                    book_data = get_book_data(full_book_url)
                    if 'error' not in book_data:
                        all_books_data.append(book_data)
                        successful_books += 1
                        print(f"  Собрана книга: {book_data['title']}")
                    else:
                        print(f"  Ошибка: {book_data['error']}")
                    
                    
                except Exception as e:
                    print(f"  Ошибка при парсинге книги: {e}")
                    continue
            
            print(f"  На странице {page_number} успешно собрано: {successful_books}/{len(book_cards)} книг")
            
            # Проверяем есть ли следующая страница
            next_button = soup.find('li', class_='next')
            if not next_button:
                print("Достигнута последняя страница каталога")
                break
                
            # Переходим к следующей странице
            page_number += 1
            
        except Exception as e:
            print(f"Ошибка при парсинге страницы {page_number}: {e}")
            break
    
    # Сохранение в файл, если нужно
    if is_save and all_books_data:
        try:
            with open('books_data.txt', 'w', encoding='utf-8') as f:
                for i, book in enumerate(all_books_data, 1):
                    f.write(f"Книга #{i}
")
                    f.write(f"Название: {book.get('title', 'N/A')}
")
                    f.write(f"Цена: {book.get('price', 'N/A')}
")
                    f.write(f"Рейтинг: {book.get('rating', 'N/A')}
")
                    f.write(f"Описание: {book.get('description', 'N/A')[:100]}...
")
                    f.write("-" * 50 + "

")
            print(f" Данные сохранены в файл 'books_data.txt'")
        except Exception as e:
            print(f" Ошибка при сохранении файла: {e}")
    
    print(f"ИТОГО собрано книг: {len(all_books_data)}")
    return all_books_data
