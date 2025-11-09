
import pytest
import requests
from bs4 import BeautifulSoup

def get_book_data(book_url: str) -> dict:
    """
    Извлекает данные о книге с веб-страницы.
    """
    try:
        response = requests.get(book_url)
        if response.status_code != 200:
            return {"error": "Страница не доступна"}
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title_element = soup.find('h1')
        title = title_element.text if title_element else "Название не найдено"
        
        price_element = soup.find('p', class_='price_color')
        price = price_element.text if price_element else "Цена не найдена"
        
        rating_element = soup.find('p', class_='star-rating')
        rating = "Рейтинг не найден"
        if rating_element and 'class' in rating_element.attrs:
            rating_classes = rating_element['class']
            rating_words = [cls for cls in rating_classes if cls != 'star-rating']
            rating = rating_words[0] if rating_words else "Рейтинг не найден"
        
        description_element = soup.find('meta', attrs={'name': 'description'})
        description = description_element['content'].strip() if description_element else "Описание не найдено"
        
        book_data = {
            'title': title,
            'price': price,
            'rating': rating,
            'description': description
        }
        
        return book_data
        
    except Exception as e:
        return {"error": f"Ошибка при парсинге: {str(e)}"}

def test_returns_dict():
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    result = get_book_data(url)
    assert isinstance(result, dict), "Функция должна возвращать словарь"
    print("Тест 1 пройден")

def test_has_required_fields():
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    result = get_book_data(url)
    assert "title" in result, "Должен быть ключ 'title'"
    assert "price" in result, "Должен быть ключ 'price'" 
    assert "rating" in result, "Должен быть ключ 'rating'"
    print("Тест 2 пройден")

def test_title_not_empty():
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    result = get_book_data(url)
    assert "title" in result, "Должен быть ключ 'title'"
    assert result["title"] != "", "Название не должно быть пустым"
    print("Тест 3 пройден")
