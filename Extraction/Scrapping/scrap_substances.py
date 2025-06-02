import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os
from urllib.parse import urljoin, quote
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SagePesticidesScraper:
    def __init__(self):
        self.base_url = "https://www.sagepesticides.qc.ca"
        self.search_url = f"{self.base_url}/Recherche/RechercheMatiere"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Certif-bloc1/1.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        })

    def get_substances_actives(self):
        logger.info("Récupération des substances actives...")
        try:
            response = self.session.get(self.search_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            select = soup.find('select', {'id': 'MatiereActiveId'})
            if not select:
                logger.error("Élément <select> introuvable.")
                return []

            substances = [
                {'id': option.get('value'), 'nom': option.text.strip()}
                for option in select.find_all('option')
                if option.get('value')
            ]
            logger.info(f"{len(substances)} substances actives trouvées.")
            return substances
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la récupération : {e}")
            return []

    def extract_table_data(self, table):
        if not table:
            return {}
        rows = table.find_all('tr')
        if not rows:
            return {}

        header_row = None
        data_rows = []

        for i, row in enumerate(rows):
            cells = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
            if cells and any(cells):
                if header_row is None and (row.find_all('th') or i == 0):
                    header_row = cells
                else:
                    data_rows.append(cells)

        if not header_row:
            return {}

        title = header_row[0]
        structured = {title: {}}
        for row in data_rows:
            key = row[0]
            structured[title][key] = {
                header_row[i]: row[i]
                for i in range(1, min(len(header_row), len(row)))
                if row[i]
            }
        return structured

    def extract_info_blocks(self, soup):
        blocks = soup.find_all('div', class_='form-group border-green blocInfos')
        infos = []

        for block in blocks:
            titre_elem = block.find(['h3', 'h4', 'h5', 'strong'])
            titre = titre_elem.get_text(strip=True) if titre_elem else None
            contenu = ' '.join(block.get_text(strip=True).split())

            liens = [
                {'texte': link.get_text(strip=True), 'url': urljoin(self.base_url, link.get('href'))}
                for link in block.find_all('a') if link.get('href')
            ]

            block_data = {'titre': titre, 'contenu': contenu}
            if liens:
                block_data['liens'] = liens
            infos.append(block_data)
        return infos

    def get_substance_details(self, substance_id, substance_name):
        logger.info(f"Récupération des données textuelles de : {substance_name}")
        try:
            url = f"{self.base_url}/Recherche/RechercheMatiere/DisplayMatiere?MatiereActiveID={substance_id}&searchText={quote(substance_name)}&isProduct=False"
            response = self.session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            tables = soup.find_all('table', class_='table table-bordered')

            data = {
                'id': substance_id,
                'nom': substance_name,
                'url': url,
                'info_blocks': self.extract_info_blocks(soup),
                'tableaux': [
                    {'index': i + 1, 'structure': self.extract_table_data(table)}
                    for i, table in enumerate(tables)
                    if self.extract_table_data(table)
                ]
            }
            return data
        except requests.RequestException as e:
            logger.error(f"Erreur pour {substance_name} : {e}")
            return None

    def scrape_all(self, max_substances=None, delay=1):
        logger.info("Début du scraping complet...")
        substances = self.get_substances_actives()
        if not substances:
            return []

        if max_substances:
            substances = substances[:max_substances]

        results = []
        for i, substance in enumerate(substances):
            logger.info(f"{i+1}/{len(substances)} - {substance['nom']}")
            data = self.get_substance_details(substance['id'], substance['nom'])
            if data:
                results.append(data)
            if delay and i < len(substances) - 1:
                time.sleep(delay)
        return results

    def save_to_json(self, data, filename="infos_substances.json"):
        try:
            os.makedirs("../data", exist_ok=True)
            filepath = os.path.join("../data", filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Données sauvegardées dans {filepath}")
        except Exception as e:
            logger.error(f"Erreur de sauvegarde : {e}")

def main():
    scraper = SagePesticidesScraper()
    data = scraper.scrape_all(delay=2)
    if data:
        scraper.save_to_json(data)
    print("Tout est terminé, veuillez consulter le fichier dans /data.")

if __name__ == "__main__":
    main()
