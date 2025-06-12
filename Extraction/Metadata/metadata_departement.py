from sqlalchemy import create_engine, MetaData, Table, Column, String
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../../.env", override=True)

USER = os.getenv("USER_POSTGRES")
PASSWORD = os.getenv("PASSWORD_POSTGRES")
HOST = os.getenv("HOST_POSTGRES")
PORT = os.getenv("PORT_POSTGRES")
DATABASE = os.getenv("DATABASE_POSTGRES")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(DATABASE_URL)

metadata = MetaData(schema="Pollution_Cancer")

metadata_departement = Table(
    "metadata_departement", metadata,
    Column("Code", String, primary_key=True),
    Column("Libelle", String)
)

metadata.create_all(engine, checkfirst=True)

# Ajout des lignes dans la table. 
def run(): 
    with engine.begin() as conn:
        conn.execute(metadata_departement.insert().values([
            {"Code": "1", "Libelle": "Ain"},
            {"Code": "2", "Libelle": "Aisne"},
            {"Code": "3", "Libelle": "Allier"},
            {"Code": "4", "Libelle": "Alpes-de-Haute-Provence"},
            {"Code": "5", "Libelle": "Hautes-Alpes"},
            {"Code": "6", "Libelle": "Alpes-Maritimes"},
            {"Code": "7", "Libelle": "Ardèche"},
            {"Code": "9", "Libelle": "Ariège"},
            {"Code": "8", "Libelle": "Ardennes"},
            {"Code": "10", "Libelle": "Aube"},
            {"Code": "11", "Libelle": "Aude"},
            {"Code": "12", "Libelle": "Aveyron"},
            {"Code": "13", "Libelle": "Bouches-du-Rhône"},
            {"Code": "14", "Libelle": "Calvados"},
            {"Code": "15", "Libelle": "Cantal"},
            {"Code": "16", "Libelle": "Charente"},
            {"Code": "17", "Libelle": "Charente-Maritime"},
            {"Code": "18", "Libelle": "Cher"},
            {"Code": "19", "Libelle": "Corrèze"},
            {"Code": "2A", "Libelle": "Corse-du-Sud"},
            {"Code": "2B", "Libelle": "Haute-Corse"},
            {"Code": "21", "Libelle": "Côte-d'Or"},
            {"Code": "22", "Libelle": "Côtes-d'Armor"},
            {"Code": "23", "Libelle": "Creuse"},
            {"Code": "24", "Libelle": "Dordogne"},
            {"Code": "25", "Libelle": "Doubs"},
            {"Code": "26", "Libelle": "Drôme"},
            {"Code": "27", "Libelle": "Eure"},
            {"Code": "28", "Libelle": "Eure-et-Loir"},
            {"Code": "29", "Libelle": "Finistère"},
            {"Code": "30", "Libelle": "Gard"},
            {"Code": "31", "Libelle": "Haute-Garonne"},
            {"Code": "32", "Libelle": "Gers"},
            {"Code": "33", "Libelle": "Gironde"},
            {"Code": "34", "Libelle": "Hérault"},
            {"Code": "35", "Libelle": "Ille-et-Vilaine"},
            {"Code": "36", "Libelle": "Indre"},
            {"Code": "37", "Libelle": "Indre-et-Loire"},
            {"Code": "38", "Libelle": "Isère"},
            {"Code": "39", "Libelle": "Jura"},
            {"Code": "40", "Libelle": "Landes"},
            {"Code": "41", "Libelle": "Loir-et-Cher"},
            {"Code": "42", "Libelle": "Loire"},
            {"Code": "43", "Libelle": "Haute-Loire"},
            {"Code": "44", "Libelle": "Loire-Atlantique"},
            {"Code": "45", "Libelle": "Loiret"},
            {"Code": "46", "Libelle": "Lot"},
            {"Code": "47", "Libelle": "Lot-et-Garonne"},
            {"Code": "48", "Libelle": "Lozère"},
            {"Code": "49", "Libelle": "Maine-et-Loire"},
            {"Code": "50", "Libelle": "Manche"},
            {"Code": "51", "Libelle": "Marne"},
            {"Code": "52", "Libelle": "Haute-Marne"},
            {"Code": "53", "Libelle": "Mayenne"},
            {"Code": "54", "Libelle": "Meurthe-et-Moselle"},
            {"Code": "55", "Libelle": "Meuse"},
            {"Code": "56", "Libelle": "Morbihan"},
            {"Code": "57", "Libelle": "Moselle"},
            {"Code": "58", "Libelle": "Nièvre"},
            {"Code": "59", "Libelle": "Nord"},
            {"Code": "60", "Libelle": "Oise"},
            {"Code": "61", "Libelle": "Orne"},
            {"Code": "62", "Libelle": "Pas-de-Calais"},
            {"Code": "63", "Libelle": "Puy-de-Dôme"},
            {"Code": "64", "Libelle": "Pyrénées-Atlantiques"},
            {"Code": "65", "Libelle": "Hautes-Pyrénées"},
            {"Code": "66", "Libelle": "Pyrénées-Orientales"},
            {"Code": "67", "Libelle": "Bas-Rhin"},
            {"Code": "68", "Libelle": "Haut-Rhin"},
            {"Code": "69", "Libelle": "Rhône"},
            {"Code": "70", "Libelle": "Haute-Saône"},
            {"Code": "71", "Libelle": "Saône-et-Loire"},
            {"Code": "72", "Libelle": "Sarthe"},
            {"Code": "73", "Libelle": "Savoie"},
            {"Code": "74", "Libelle": "Haute-Savoie"},
            {"Code": "75", "Libelle": "Paris"},
            {"Code": "76", "Libelle": "Seine-Maritime"},
            {"Code": "77", "Libelle": "Seine-et-Marne"},
            {"Code": "78", "Libelle": "Yvelines"},
            {"Code": "79", "Libelle": "Deux-Sèvres"},
            {"Code": "80", "Libelle": "Somme"},
            {"Code": "81", "Libelle": "Tarn"},
            {"Code": "82", "Libelle": "Tarn-et-Garonne"},
            {"Code": "83", "Libelle": "Var"},
            {"Code": "84", "Libelle": "Vaucluse"},
            {"Code": "85", "Libelle": "Vendée"},
            {"Code": "86", "Libelle": "Vienne"},
            {"Code": "87", "Libelle": "Haute-Vienne"},
            {"Code": "88", "Libelle": "Vosges"},
            {"Code": "89", "Libelle": "Yonne"},
            {"Code": "90", "Libelle": "Territoire de Belfort"},
            {"Code": "91", "Libelle": "Essonne"},
            {"Code": "92", "Libelle": "Hauts-de-Seine"},
            {"Code": "93", "Libelle": "Seine-Saint-Denis"},
            {"Code": "94", "Libelle": "Val-de-Marne"},
            {"Code": "95", "Libelle": "Val-d'Oise"},
            {"Code": "FM", "Libelle": "France métropolitaine"},
            {"Code": "971", "Libelle": "Guadeloupe"},
            {"Code": "972", "Libelle": "Martinique"},
            {"Code": "973", "Libelle": "Guyane"},
            {"Code": "974", "Libelle": "La Réunion"},
            {"Code": "DOM", "Libelle": "Départements d'Outre-mer"},
            {"Code": "F", "Libelle": "France"}
        ]))
        conn.commit()
        print("metadata_departement inséré avec succès")


if __name__ == "__main__":
    run()

