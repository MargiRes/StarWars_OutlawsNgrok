from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def scrape_star_wars_outlaws_data():
    url = "https://en.wikipedia.org/wiki/Star_Wars_Outlaws"

    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        def extract_text(selector):
            element = soup.select_one(selector)
            return element.get_text(strip=True) if element else "Not available"

        def extract_paragraph_text(section_name):
            headers = soup.find_all("h2")
            for header in headers:
                header_text = header.get_text(strip=True).lower()
                if section_name.lower() in header_text:
                    paragraph = header.find_next("p")
                    if paragraph:
                        text = paragraph.get_text(strip=True)

                        cleaned_text = re.sub(r'\[\d+\]', '', text)
                        return cleaned_text
                    else:
                        return "Not available"
            return "Not available"

        game_title = extract_text("h1#firstHeading")
        release_date = extract_text  ("th:-soup-contains('Release') + td")
        developer = extract_text("th:-soup-contains('Developer(s)') + td")
        publisher = extract_text("th:-soup-contains('Publisher(s)') + td")
        platforms = extract_text("th:-soup-contains('Platform(s)') + td")
        key_features = extract_paragraph_text("Gameplay")

        return {
            "game_title": game_title,
            "release_date": release_date,
            "developer": developer,
            "publisher": publisher,
            "platforms": platforms,
            "key_features": key_features,
        }

    except Exception as e:
        print(f"Error: {e}") 
        return {    
            "game_title": "Error",
            "release_date": "Error",
            "developer": "Error",
            "publisher": "Error",
            "platforms": "Error",
            "key_features": "Error",
        }


@app.route("/")
def index():
    data = scrape_star_wars_outlaws_data()
    return render_template("index.html", game_data=data)

if __name__ == "__main__":
    app.run(debug=True)