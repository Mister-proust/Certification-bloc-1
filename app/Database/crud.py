from Database.db import connection_postgres
from typing import Optional
from collections import defaultdict
from decimal import Decimal

def lecture_fichier_sql(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def test_fonction_sql():
    conn = connection_postgres()
    cursor = conn.cursor()
    cursor.execute('SELECT amm, "Nom_produit", titulaire FROM "Pollution_Cancer"."amm_produits";')
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "nom": r[1], "titulaire": r[2]} for r in rows]


def generalite_data(dept_code: str, annee: Optional[int] = None, type_cancer: Optional[str] = None):
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
    if isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimal(v) for v in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj
    

def data_sexe(dept_code: str, annee: Optional[int] = None, type_cancer: Optional[str] = None, sexe: Optional[str] = None):
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
