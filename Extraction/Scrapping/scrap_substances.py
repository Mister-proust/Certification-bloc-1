import requests
from bs4 import BeautifulSoup
import json
import time
import re
import os
from urllib.parse import urljoin, quote
import logging
from datetime import datetime


def setup_logging():
    """
    Configure le système de logging pour enregistrer les logs dans un fichier et dans la console.
    
    Retourne:
        logger (Logger): Instance de logger configurée.
    """
    os.makedirs("../logs", exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"../logs/scraper_{timestamp}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Script lancé, début du scrapping - {datetime.now()} ===")
    logger.info(f"Les logs sont sauvegardés dans : {log_filename}")
    
    return logger

class SagePesticidesScraper:
    """
    Scraper pour extraire les informations des substances actives depuis le site Sage Pesticides.
    """

    def __init__(self):
        """
        Initialise la session de scraping avec des headers personnalisés.
        """
        self.base_url = "https://www.sagepesticides.qc.ca"
        self.search_url = f"{self.base_url}/Recherche/RechercheMatiere"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Certif-bloc1/1.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        })

        self.logger = logging.getLogger(__name__)

    def get_substances_actives(self):
        """
        Récupère la liste des substances actives disponibles sur le site.

        Retourne:
            list: Liste des substances sous forme de dictionnaires {id, nom}.
        """
        self.logger.info("Récupération des substances actives...")
        try:
            response = self.session.get(self.search_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            select = soup.find('select', {'id': 'MatiereActiveId'})
            if not select:
                self.logger.error("Élément <select> introuvable.")
                return []

            substances = [
                {'id': option.get('value'), 'nom': option.text.strip()}
                for option in select.find_all('option')
                if option.get('value')
            ]
            self.logger.info(f"{len(substances)} substances actives trouvées.")
            return substances
        except requests.RequestException as e:
            self.logger.error(f"Erreur lors de la récupération : {e}")
            return []

    def extract_table_data(self, table):
        """
        Extrait les données structurées d'un tableau HTML.

        Args:
            table (Tag): Élément BeautifulSoup correspondant à un tableau HTML.

        Retourne:
            dict: Structure du tableau sous forme de dictionnaire.
        """
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
        """
        Extrait les blocs d'information textuels présents sur la page de détail d'une substance.

        Args:
            soup (BeautifulSoup): Contenu HTML de la page.

        Retourne:
            list: Liste des blocs d'informations avec leur titre, contenu et liens associés.
        """
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
        """
        Récupère toutes les informations détaillées d'une substance donnée.

        Args:
            substance_id (str): Identifiant de la substance.
            substance_name (str): Nom de la substance.

        Retourne:
            dict: Dictionnaire contenant les informations textuelles et tabulaires de la substance.
        """
        self.logger.info(f"Récupération des données textuelles de : {substance_name}")
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
            self.logger.info(f"Données de {substance_name} bien récupérées.")
            return data
        except requests.RequestException as e:
            self.logger.error(f"Erreur de récupération des données pour {substance_name} : {e}")
            return None

    def scrape_all(self, max_substances=None, delay=1):
        """
        Scrape toutes les substances actives disponibles.

        Args:
            max_substances (int, optionnel): Nombre maximum de substances à scraper. Si None, toutes les substances sont récupérées.
            delay (int, optionnel): Temps de pause entre chaque requête pour éviter de surcharger le serveur.

        Retourne:
            list: Liste des données collectées pour chaque substance.
        """
        self.logger.info("Début du scraping complet...")
        substances = self.get_substances_actives()
        if not substances:
            return []

        if max_substances:
            substances = substances[:max_substances]

        results = []
        for i, substance in enumerate(substances):
            self.logger.info(f"{i+1}/{len(substances)} - {substance['nom']}")
            data = self.get_substance_details(substance['id'], substance['nom'])
            if data:
                results.append(data)
            if delay and i < len(substances) - 1:
                time.sleep(delay)
        
        self.logger.info(f" Scrapping terminé, {len(results)} substances récupérées.")
        return results

    def save_to_json(self, data, filename="infos_substances.json"):
        """
        Sauvegarde les données récupérées dans un fichier JSON.

        Args:
            data (list): Liste des substances récupérées.
            filename (str, optionnel): Nom du fichier JSON.
        """
        try:
            os.makedirs("../data", exist_ok=True)
            filepath = os.path.join("../data", filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.info(f"Données sauvegardées dans {filepath}")
        except Exception as e:
            self.logger.error(f"Erreur de sauvegarde : {e}")

def main():
    """
    Fonction principale : initialise le logger, exécute le scraping et sauvegarde les résultats.
    """
    logger = setup_logging()
    try:
        scraper = SagePesticidesScraper()
        data = scraper.scrape_all(delay=2)
        
        if data:
            scraper.save_to_json(data)
            logger.info("Scraping terminé avec succès")
        else:
            logger.error("Aucune donnée récupérée")
            
    except Exception as e:
        logger.error(f"Erreur critique : {e}")
        raise
    finally:
        logger.info(f"Scrapping terminé. - {datetime.now()} ===")
        
    print("Tout est terminé, veuillez consulter le fichier dans /data et les logs dans /logs.")


if __name__ == "__main__":
    main()
