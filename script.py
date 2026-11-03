import requests
from bs4 import BeautifulSoup

# Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

def main():
    url = "https://habr.com/ru/articles/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка при запросе к сайту: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Находим все карточки статей на странице
    articles = soup.find_all("article", class_="tm-articles-list__item")

    for article in articles:
        # Извлекаем заголовок и ссылку
        title_tag = article.find("h2", class_="tm-title")
        if not title_tag:
            continue

        link_tag = title_tag.find("a")
        if not link_tag:
            continue
        title = link_tag.text.strip()
        link = "https://habr.com" + link_tag.get("href", "")

        # Извлекаем дату публикации
        date_tag = article.find("time")
        if date_tag:
            date = date_tag.get("datetime", date_tag.text.strip())
        else:
            date = "Дата не найдена"

        # Собираем preview-информацию: заголовок + текст превью + теги (если есть)
        preview_parts = [title]

        # Текст превью (lead)
        lead_tag = article.find("div", class_="tm-article-snippet__lead")
        if lead_tag:
            preview_parts.append(lead_tag.text.strip())

        # Теги (хабы)
        hubs_tags = article.find_all("a", class_="tm-tags-list__link")
        for hub in hubs_tags:
            preview_parts.append(hub.text.strip())

        preview_text = " ".join(preview_parts).lower()

        # Проверяем наличие хотя бы одного ключевого слова
        if any(keyword.lower() in preview_text for keyword in KEYWORDS):
            print(f"{date} – {title} – {link}")

if __name__ == "__main__":
    main()