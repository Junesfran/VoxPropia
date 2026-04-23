import json
import requests
import os
import boto3
from bs4 import BeautifulSoup
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def lambda_handler(event, context):
    # 1. Definir rutas temporales obligatorias en AWS Lambda
    txt_path = "/tmp/actividades.txt"
    pdf_path = "/tmp/actividades.pdf"
    
    url = "https://iescomercio.com/convozpropia/actividades/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        ul = soup.find("ul", class_="wp-block-archives-list wp-block-archives")
        links = []
        
        if ul:
            for a in ul.find_all('a'):
                if a and a.get("href"):
                    links.append(a["href"])

        # 2. Recorrer enlaces y generar archivos en /tmp/
        with open(txt_path, "w", encoding="utf-8") as f:
            doc = SimpleDocTemplate(pdf_path)
            styles = getSampleStyleSheet()
            contenido = []

            f.write("Actividades\n\n")
            contenido.append(Paragraph("Actividades\n", styles["Normal"]))
            
            for link in links:
                print(f"Entrando en: {link}") # Esto aparecerá en CloudWatch Logs
                
                r = requests.get(link, headers=headers)
                s = BeautifulSoup(r.text, "html.parser")
                
                for div in s.find_all('div', class_="read-more-button"):
                    r2 = requests.get(div.find('a').get("href"))
                    s2 = BeautifulSoup(r2.text, "html.parser")

                    # Uso de .get_text() seguro por si cambia el HTML
                    titulo_elem = s2.find("h1", class_="single-title")
                    titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Sin título"

                    fecha_elem = s2.find('span', class_="posted-date")
                    fecha = fecha_elem.get_text(strip=True) if fecha_elem else "Sin fecha"

                    container = s2.find("div", class_="single-content")
                    info = ""
                    if container:
                        for p in container.find_all("p"):
                            info += p.get_text(separator=" ", strip=True)

                    container_cat = s2.find("div", class_="cat-links")
                    cat = []
                    if container_cat:
                        for a in container_cat.find_all('a'):
                            cat.append(a.get_text(strip=True))

                    f.write(f"Titulo: {titulo}\n")
                    f.write(f"Fecha: {fecha}\n")
                    f.write(f"Categorías: {', '.join(cat)}\n")
                    f.write(f"Información: {info}\n\n")

                    contenido.append(Paragraph(f"Titulo: {titulo}", styles["Normal"]))
                    contenido.append(Paragraph(f"Fecha: {fecha}", styles["Normal"]))
                    contenido.append(Paragraph(f"Categorías: {', '.join(cat)}", styles["Normal"]))
                    contenido.append(Paragraph(f"Información: {info}\n", styles["Normal"]))

            doc.build(contenido)

        # 3. Subir los archivos generados a Amazon S3
        s3 = boto3.client('s3')
        bucket_name = "voxpropia"
        
        print("Subiendo archivos a S3...")
        s3.upload_file(txt_path, bucket_name, "fuentes/actividades.txt")
        s3.upload_file(pdf_path, bucket_name, "fuentes/actividades.pdf")
        print("Subida exitosa.")

        return {
            'statusCode': 200,
            'body': json.dumps('Scraping y subida a S3 completados con éxito')
        }

    except Exception as e:
        print(f"Error durante la ejecución: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }