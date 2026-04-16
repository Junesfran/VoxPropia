import requests
from bs4 import BeautifulSoup

# 1. URL de la página principal
url = "https://iescomercio.com/convozpropia/actividades/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 2. Encontrar los divs que contienen enlaces
ul = soup.find("ul", class_="wp-block-archives-list wp-block-archives")  # ajusta esto

links = []

for a in ul.find_all('a'):
    if a and a.get("href"):
        links.append(a["href"])

# 3. Recorrer cada enlace
with open("actividades.txt", "w", encoding="utf-8") as f:
    f.write("Actividades\n\n")
    for link in links:
        print(f"Entrando en: {link}")
        
        r = requests.get(link, headers=headers)
        s = BeautifulSoup(r.text, "html.parser")
        
        # 4. Extraer contenido
        
        for div in s.find_all('div',class_="read-more-button"):

            r2 = requests.get(div.find('a').get("href"))
            s2 = BeautifulSoup(r2.text, "html.parser")

            titulo = s2.find("h1",class_="single-title").get_text(strip=True)

            fecha = s2.find('span',class_="posted-date").get_text(strip=True)

            # Informacion
            container = s2.find("div",class_="single-content")
            paragraphs = container.find_all("p")
            info = ""
            for p in paragraphs:
                info += p.get_text(separator=" ",strip=True)

            container_cat = s2.find("div", class_="cat-links")
            cat = []
            for a in container_cat.find_all('a'):
                cat.append(a.get_text(strip=True))
                
            
            f.write(f"Titulo: {titulo}\n")
            f.write(f"Fecha: {fecha}\n")
            f.write(f"Categorías: {', '.join(cat)}\n")
            f.write(f"Información: {info}\n\n")
            