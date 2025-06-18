from Database.db import connection_postgres


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


def generalite_data(dept_code: str):
    sql = lecture_fichier_sql("Database/sql/generalite_sql.sql")
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

