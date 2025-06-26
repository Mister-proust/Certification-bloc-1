from Database.db import connection_postgres
from typing import Optional
from collections import defaultdict
from decimal import Decimal

def lecture_fichier_sql(filename: str) -> str:
    """
    Lit et retourne le contenu d'un fichier SQL donné.

    Args:
        filename (str): Chemin vers le fichier SQL à lire.

    Returns:
        str: Contenu texte du fichier SQL.
    """
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

def generalite_data(dept_code: str, annee: Optional[int] = None, type_cancer: Optional[str] = None):
    """
    Récupère les données générales sur les cancers et l'utilisation de pesticides pour un département donné,
    avec des filtres optionnels par année et type de cancer.

    Args:
        dept_code (str): Code du département.
        annee (Optional[int]): Année de filtrage (optionnel).
        type_cancer (Optional[str]): Type de cancer (optionnel).

    Returns:
        list[dict]: Liste de dictionnaires avec les données suivantes :
            - annee
            - departement
            - nom_departement
            - type_cancer
            - classe_age
            - sexe
            - effectif_patients
            - effectif_total
            - prevalence_pourcentage (float ou None)
            - quantite_en_kg (pesticides)
    """
    sql = lecture_fichier_sql("Database/sql/generalite_sql.sql")
    filtres = []
    filtres.append(f"ec.\"Departement\" = '{dept_code}'")
    if annee:
        filtres.append(f"ec.\"Annee\" = {annee}")
    if type_cancer:
        filtres.append(f"ec.\"Type_cancer\" = '{type_cancer}'")
    sql_parts = sql.split("WHERE")
    sql = sql_parts[0] + "WHERE " + " AND ".join(filtres) + " AND " + sql_parts[1]
    conn = connection_postgres()
    cursor = conn.cursor()
    cursor.execute(sql, {"dept_code": dept_code})
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "annee": r[0],
            "departement": r[1],
            "nom_departement": r[2],
            "type_cancer": r[3],
            "classe_age": r[4],
            "sexe": r[5],
            "effectif_patients": r[6],
            "effectif_total": r[7],
            "prevalence_pourcentage": float(r[8]) if r[8] is not None else None,
            "quantite_en_kg": r[9],
        }
        for r in rows
    ]

def graphiques_generalites(data):
    """
    Prépare les données agrégées pour générer des graphiques de prévalence et de substances
    par type de cancer et année à partir des données brutes.

    Args:
        data (list[dict]): Liste des données renvoyées par `generalite_data`.

    Returns:
        dict: Structure regroupant pour chaque type de cancer :
            - annees (list)
            - prevalences (list) : en pourcentage
            - substances (list) : quantité totale en kg
    """
    types = {
        "global": lambda x: True,
        "autres": lambda x: x["type_cancer"] == "Autres cancers",
        "sein": lambda x: x["type_cancer"] == "Cancer du sein de la femme",
        "prostate": lambda x: x["type_cancer"] == "Cancer de la prostate",
        "broncho": lambda x: x["type_cancer"] == "Cancer bronchopulmonaire",
        "colorectal": lambda x: x["type_cancer"] == "Cancer colorectal"
    }

    result = {}

    for key, filt in types.items():
        stats = defaultdict(lambda: {
            "patients": 0,
            "population": 0,
            "substances": set()  # ✅ correction ici
        })

        for row in filter(filt, data):
            y = row["annee"]
            stats[y]["patients"] += row["effectif_patients"]
            stats[y]["population"] += row["effectif_total"]
            stats[y]["substances"].add(row["quantite_en_kg"])

        annees = sorted(stats)
        result[key] = {
            "annees": annees,
            "prevalences": [
                round(100 * stats[y]["patients"] / stats[y]["population"], 2)
                if stats[y]["population"] else 0
                for y in annees
            ],
            "substances": [
                round(sum(q for q in stats[y]["substances"] if q is not None), 2)
                for y in annees
            ]
        }
    return result


def convert_decimal(obj):
    """
    Convertit récursivement les objets Decimal en float dans une structure dict/liste.

    Args:
        obj: Objet pouvant être un dict, list, Decimal ou autre.

    Returns:
        Objet équivalent avec Decimal convertis en float.
    """
    if isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimal(v) for v in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj
    

def data_sexe(dept_code: str, annee: Optional[int] = None, type_cancer: Optional[str] = None, sexe: Optional[str] = None):
    """
    Récupère les données segmentées par sexe sur un département donné, avec filtres optionnels.

    Args:
        dept_code (str): Code département.
        annee (Optional[int]): Année (optionnel).
        type_cancer (Optional[str]): Type de cancer (optionnel).
        sexe (Optional[str]): Sexe ("M" ou "F", optionnel).

    Returns:
        list[dict]: Données similaires à `generalite_data` avec filtre sexe.
    """
    sql = lecture_fichier_sql("Database/sql/sexe.sql")
    filtres = []
    filtres.append(f"ec.\"Departement\" = '{dept_code}'")
    if annee:
        filtres.append(f"ec.\"Annee\" = {annee}")
    if type_cancer:
        filtres.append(f"ec.\"Type_cancer\" = '{type_cancer}'")
    if sexe:
        filtres.append(f"ec.\"Sexe\" = '{sexe}'")
    sql_parts = sql.split("WHERE")
    sql = sql_parts[0] + "WHERE " + " AND ".join(filtres) + " AND " + sql_parts[1]
    conn = connection_postgres()
    cursor = conn.cursor()
    cursor.execute(sql, {"dept_code": dept_code})
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "annee": r[0],
            "departement": r[1],
            "nom_departement": r[2],
            "type_cancer": r[3],
            "classe_age": r[4],
            "sexe": r[5],
            "effectif_patients": r[6],
            "effectif_total": r[7],
            "prevalence_pourcentage": float(r[8]) if r[8] is not None else None,
            "quantite_en_kg": r[9],
        }
        for r in rows
    ]


def graphiques_sexe(data):
    """
    Prépare les données agrégées pour des graphiques segmentés par sexe et type de cancer,
    incluant prévalences et quantités de substances.

    Args:
        data (list[dict]): Données issues de `data_sexe`.

    Returns:
        dict: Pour chaque type de cancer, liste des années, prévalences hommes, prévalences femmes et substances.
    """
    types = {
        "global": lambda x: True,
        "autres": lambda x: x["type_cancer"] == "Autres cancers",
        "sein": lambda x: x["type_cancer"] == "Cancer du sein de la femme",
        "prostate": lambda x: x["type_cancer"] == "Cancer de la prostate",
        "broncho": lambda x: x["type_cancer"] == "Cancer bronchopulmonaire",
        "colorectal": lambda x: x["type_cancer"] == "Cancer colorectal"
    }

    result = {}

    for key, filt in types.items():
        stats = defaultdict(lambda: {
            "M": {"patients": 0, "population": 0},
            "F": {"patients": 0, "population": 0},
            "substances": set()  # utiliser un set pour ne pas additionner plusieurs fois
        })

        for row in filter(filt, data):
            y = row["annee"]
            sexe = row["sexe"]
            stats[y][sexe]["patients"] += row["effectif_patients"]
            stats[y][sexe]["population"] += row["effectif_total"]
            # Ajout unique d'une valeur de substance par an
            stats[y]["substances"].add((row["annee"], row["quantite_en_kg"]))

        annees = sorted(stats)
        result[key] = {
            "annees": annees,
            "prevalences_homme": [
                round(100 * stats[y]["M"]["patients"] / stats[y]["M"]["population"], 2)
                if stats[y]["M"]["population"] else 0
                for y in annees
            ],
            "prevalences_femme": [
                round(100 * stats[y]["F"]["patients"] / stats[y]["F"]["population"], 2)
                if stats[y]["F"]["population"] else 0
                for y in annees
            ],
            "substances": [
                round(sum(q for _, q in stats[y]["substances"]), 2) if stats[y]["substances"] else 0
                for y in annees
            ]
        }

    return result


def data_age(dept_code: str, annee: Optional[int] = None, type_cancer: Optional[str] = None, classe_age: Optional[str] = None):
    """
    Récupère les données segmentées par classe d'âge, avec filtres sur département, année, type de cancer et classe d'âge.

    Args:
        dept_code (str): Code département.
        annee (Optional[int]): Année (optionnel).
        type_cancer (Optional[str]): Type de cancer (optionnel).
        classe_age (Optional[str]): Classe d'âge (optionnel).

    Returns:
        list[dict]: Données avec clés similaires aux autres fonctions, ajout de "classe_age" et "Code_âge".
    """
    sql = lecture_fichier_sql("Database/sql/age.sql")
    filtres = []
    filtres.append(f"ec.\"Departement\" = '{dept_code}'")
    if annee:
        filtres.append(f"ec.\"Annee\" = {annee}")
    if type_cancer:
        filtres.append(f"ec.\"Type_cancer\" = '{type_cancer}'")
    if classe_age:
        filtres.append(f"ma.\"Libelle\" = '{classe_age}'")
    sql_parts = sql.split("WHERE")
    sql = sql_parts[0] + "WHERE " + " AND ".join(filtres) + " AND " + sql_parts[1]
    conn = connection_postgres()
    cursor = conn.cursor()
    cursor.execute(sql, {"dept_code": dept_code})
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "annee": r[0],
            "departement": r[1],
            "nom_departement": r[2],
            "type_cancer": r[3],
            "Code_âge": r[4],
            "classe_age" : r[5],
            "sexe": r[6],
            "effectif_patients": r[7],
            "effectif_total": r[8],
            "prevalence_pourcentage": float(r[9]) if r[8] is not None else None,
            "quantite_en_kg": r[10],
        }
        for r in rows
    ]


def graphiques_age(data):
    """
    Prépare les données pour des graphiques détaillés selon classes d'âge et types de cancer,
    avec calcul des prévalences et quantités de substances pour chaque combinaison année-classe d'âge-type de cancer.

    Args:
        data (list[dict]): Données issues de `data_age`.

    Returns:
        dict: Contient
            - annees (list)
            - classes_age (list)
            - types_cancer (list)
            - substances (list) : quantités totales par année
            - data (dict) : clés "classeAge_typeCancer" avec listes des prévalences par année
    """
    stats = defaultdict(lambda: defaultdict(lambda: {
        "patients": 0, 
        "population": 0
    }))
    substances_by_year = {}
    classes_age = set()
    types_cancer = set()
    
    for row in data:
        annee = row["annee"]
        classe_age = row["classe_age"]
        type_cancer = row["type_cancer"]
        
        classes_age.add(classe_age)
        types_cancer.add(type_cancer)
        
        key = f"{classe_age}_{type_cancer}"
        stats[annee][key]["patients"] += row["effectif_patients"]
        stats[annee][key]["population"] += row["effectif_total"]
        if annee not in substances_by_year:
            quantite = row["quantite_en_kg"]
            substances_by_year[annee] = float(quantite) if quantite is not None else 0.0

    annees = sorted(stats.keys())
    result = {
        "annees": annees,
        "classes_age": sorted(list(classes_age)),
        "types_cancer": sorted(list(types_cancer)),
        "substances": [round(substances_by_year.get(annee, 0), 2) for annee in annees],
        "data": {}
    }
    for classe_age in classes_age:
        for type_cancer in types_cancer:
            key = f"{classe_age}_{type_cancer}"
            
            prevalences = []
            
            for annee in annees:
                if key in stats[annee] and stats[annee][key]["population"] > 0:
                    prevalence = (stats[annee][key]["patients"] / stats[annee][key]["population"]) * 100
                    prevalences.append(round(prevalence, 2))
                else:
                    prevalences.append(0)
            
            result["data"][key] = {
                "classe_age": classe_age,
                "type_cancer": type_cancer,
                "prevalences": prevalences
            }
    
    return result