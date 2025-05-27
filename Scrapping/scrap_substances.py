import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, quote
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SagePesticidesScraper:
    def __init__(self):
        self.base_url = "https://www.sagepesticides.qc.ca"
        self.search_url = "https://www.sagepesticides.qc.ca/Recherche/RechercheMatiere"
        self.session = requests.Session()
        # Headers pour simuler un navigateur
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-CA,fr;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
    def get_substances_actives(self):
        """Récupère la liste de toutes les substances actives"""
        logger.info("Récupération de la liste des substances actives...")
        
        try:
            response = self.session.get(self.search_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Trouver le select avec l'id MatiereActiveId
            select_element = soup.find('select', {'id': 'MatiereActiveId'})
            
            if not select_element:
                logger.error("Impossible de trouver l'élément select MatiereActiveId")
                return []
            
            substances = []
            options = select_element.find_all('option')
            
            for option in options:
                value = option.get('value')
                text = option.get_text().strip()
                
                # Ignorer l'option vide
                if value and value != "":
                    substances.append({
                        'id': value,
                        'nom': text
                    })
            
            logger.info(f"Trouvé {len(substances)} substances actives")
            return substances
            
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la récupération des substances: {e}")
            return []
    
    def extract_table_data(self, table):
        """Extrait les données d'un tableau HTML"""
        if not table:
            return []
        
        data = []
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            row_data = []
            for cell in cells:
                # Nettoyer le texte de la cellule
                text = cell.get_text().strip()
                text = ' '.join(text.split())  # Normaliser les espaces
                row_data.append(text)
            
            if row_data:  # Ignorer les lignes vides
                data.append(row_data)
        
        return data
    
    def extract_info_blocks(self, soup):
        """Extrait les informations des blocs d'infos"""
        info_blocks = []
        blocks = soup.find_all('div', class_=['form-group border-green blocInfos'])
        
        for block in blocks:
            block_data = {}
            
            # Extraire le titre si présent
            title_elem = block.find(['h3', 'h4', 'h5', 'strong'])
            if title_elem:
                block_data['titre'] = title_elem.get_text().strip()
            
            # Extraire tout le texte du bloc
            text_content = block.get_text().strip()
            text_content = ' '.join(text_content.split())
            block_data['contenu'] = text_content
            
            # Extraire les liens s'il y en a
            links = block.find_all('a')
            if links:
                block_data['liens'] = []
                for link in links:
                    href = link.get('href')
                    if href:
                        full_url = urljoin(self.base_url, href)
                        block_data['liens'].append({
                            'texte': link.get_text().strip(),
                            'url': full_url
                        })
            
            info_blocks.append(block_data)
        
        return info_blocks
    
    def get_substance_details(self, substance_id, substance_name):
        """Récupère les détails d'une substance active"""
        logger.info(f"Récupération des détails pour: {substance_name}")
        
        # Construire l'URL avec les paramètres
        search_text = quote(substance_name)
        detail_url = f"{self.base_url}/Recherche/RechercheMatiere/DisplayMatiere?MatiereActiveID={substance_id}&searchText={search_text}&isProduct=False"
        
        try:
            response = self.session.get(detail_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraire les données demandées
            substance_data = {
                'id': substance_id,
                'nom': substance_name,
                'url': detail_url,
                'info_blocks': self.extract_info_blocks(soup),
                'tableaux': []
            }
            
            # Extraire les tableaux
            tables = soup.find_all('table', class_=['table table-bordered', 'table table-bordered '])
            
            for i, table in enumerate(tables):
                table_data = self.extract_table_data(table)
                if table_data:
                    substance_data['tableaux'].append({
                        'index': i + 1,
                        'donnees': table_data
                    })
            
            logger.info(f"Données extraites pour {substance_name}: {len(substance_data['info_blocks'])} blocs info, {len(substance_data['tableaux'])} tableaux")
            return substance_data
            
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la récupération des détails pour {substance_name}: {e}")
            return None
    
    def scrape_all(self, max_substances=None, delay=1):
        """Scrape toutes les substances actives"""
        logger.info("Début du scraping complet...")
        
        # Récupérer la liste des substances
        substances = self.get_substances_actives()
        
        if not substances:
            logger.error("Aucune substance trouvée")
            return []
        
        # Limiter le nombre de substances pour les tests
        if max_substances:
            substances = substances[:max_substances]
            logger.info(f"Limitation à {max_substances} substances pour test")
        
        all_data = []
        
        for i, substance in enumerate(substances):
            logger.info(f"Traitement {i+1}/{len(substances)}: {substance['nom']}")
            
            # Récupérer les détails
            details = self.get_substance_details(substance['id'], substance['nom'])
            
            if details:
                all_data.append(details)
            
            # Pause entre les requêtes pour éviter de surcharger le serveur
            if delay > 0 and i < len(substances) - 1:
                time.sleep(delay)
        
        logger.info(f"Scraping terminé. {len(all_data)} substances traitées avec succès.")
        return all_data
    
    def save_to_json(self, data, filename="sage_pesticides_data.json"):
        """Sauvegarde les données en JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Données sauvegardées dans {filename}")
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {e}")

def main():
    scraper = SagePesticidesScraper()
    
    # Pour tester, limiter à 5 substances
    # Retirez max_substances=5 pour scraper toutes les substances
    data = scraper.scrape_all(max_substances=5, delay=2)
    
    if data:
        # Sauvegarder en JSON
        scraper.save_to_json(data)
        
        # Afficher un exemple de structure
        print("\n=== EXEMPLE DE STRUCTURE DES DONNÉES ===")
        if data:
            exemple = data[0]
            print(f"Substance: {exemple['nom']}")
            print(f"ID: {exemple['id']}")
            print(f"Nombre de blocs info: {len(exemple['info_blocks'])}")
            print(f"Nombre de tableaux: {len(exemple['tableaux'])}")
            
            if exemple['info_blocks']:
                print(f"\nPremier bloc info: {exemple['info_blocks'][0].get('contenu', '')[:100]}...")
            
            if exemple['tableaux']:
                print(f"\nPremier tableau: {len(exemple['tableaux'][0]['donnees'])} lignes")
    
    print("\nScraping terminé!")

if __name__ == "__main__":
    main()