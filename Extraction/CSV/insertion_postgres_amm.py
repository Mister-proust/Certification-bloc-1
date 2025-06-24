import pandas as pd
from sqlmodel import Session
from model.db_init import engine
from model.models import AmmMentionDanger, AmmProduits
from datetime import datetime

def parse_date_safe(date_str):
    """
    Tente de parser une date depuis une chaîne de caractères.
    Si le parsing échoue, retourne None.

    Args:
        date_str (str): Date sous forme de chaîne.

    Returns:
        datetime.date or None: Date formatée ou None si parsing impossible.
    """
    try:
        return pd.to_datetime(date_str, dayfirst=True).date()
    except Exception:
        return None


def run() : 
    """
    Fonction principale qui :
    - Charge et nettoie les fichiers AMM et mentions de danger.
    - Formate les dates et les colonnes.
    - Insère les données dans la base PostgreSQL.
    """

    # Chargement des données sur les mentions de danger
    df_amm_danger = pd.read_csv("../data/produits_classe_et_mention_danger_utf8.csv", sep=";")

    # Suppression des colonnes inutiles
    df_amm_danger = df_amm_danger.drop(columns=["Unnamed: 4"])

    # Renommage des colonnes pour harmonisation
    df_amm_danger= df_amm_danger.rename(columns={
        "numero AMM": "amm",
        "nom produit" : "Nom_produit",
        "Libellé court": "Libellé_court",
        "Libellé long": "Toxicite_produit"
        })

    # Chargement des données sur les produits AMM
    df_produits = pd.read_csv("../data/produits_utf8.csv", sep=";")

    # Suppression des colonnes inutiles
    df_produits = df_produits.drop(columns=["type produit"])
    df_produits = df_produits.drop(columns=["Unnamed: 18"])

    # Renommage des colonnes pour harmonisation
    df_produits= df_produits.rename(columns={
        "numero AMM": "amm",
        "nom produit" : "Nom_produit",
        "seconds noms commerciaux" : "Second_noms_commerciaux",
        "type commercial" : "Type_commercial",
        "gamme usage" : "Gamme_usage",
        "mentions autorisees" : "Mentions_autorisees",
        "restrictions usage" : "Restrictions_usage", 
        "restrictions usage libelle" : "Restrictions_usage_libelle",
        "Substances actives" : "Substances_actives",
        "fonctions" : "Fonctions",
        "formulations" : "Formulations",
        "Etat d’autorisation" : "Etat_d_autorisation",
        "Date de retrait du produit" : "Date_de_retrait",
        "Date de première autorisation" : "Date_première_autorisation",
        "Numéro AMM du produit de référence" : "Numero_AMM_reference",
        "Nom du produit de référence" : "Nom_produit_reference"
        })

    # Conversion des colonnes de date avec gestion des erreurs
    df_produits["Date_première_autorisation"] = df_produits["Date_première_autorisation"].apply(parse_date_safe)
    df_produits["Date_de_retrait"] = df_produits["Date_de_retrait"].apply(parse_date_safe)
    
    # Remplacement des valeurs NaN par None
    df_produits = df_produits.where(pd.notnull(df_produits), None)

    # Nettoyage et conversion des AMM
    df_produits['amm'] = pd.to_numeric(df_produits['amm'], errors='coerce')  
    df_produits = df_produits.dropna(subset=['amm'])                         
    df_produits['amm'] = df_produits['amm'].astype(int)          

    # Création d'une clé primaire id_amm_danger pour les mentions de danger
    df_amm_danger = df_amm_danger.reset_index(drop=False)
    df_amm_danger = df_amm_danger.rename(columns={"index":"id_amm_danger"})
    cols = df_amm_danger.columns.tolist()
    cols = ['id_amm_danger'] + [col for col in cols if col != 'id_amm_danger']
    df_amm_danger = df_amm_danger[cols]

    # Conversion des DataFrames en objets SQLModel
    liste_amm_danger = [
        AmmMentionDanger(**row) for row in df_amm_danger.to_dict(orient="records")
    ]

    liste_produits = [
        AmmProduits(**row) for row in df_produits.to_dict(orient="records")
    ]

    # Insertion des données dans la base PostgreSQL
    with Session(engine) as session:
        session.add_all(liste_produits)
        session.commit()
        session.add_all(liste_amm_danger)
        session.commit()


    print(f"Données AMM insérées avec succès, veuillez vérifier.")

if __name__ == "__main__":
    run()
