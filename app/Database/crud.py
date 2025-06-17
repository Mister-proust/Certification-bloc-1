from Database.db import connection_postgres


def read_sql_file(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def test_fonction_sql():
    conn = connection_postgres()
    cursor = conn.cursor()
    cursor.execute('SELECT amm, "Nom_produit", titulaire FROM "Pollution_Cancer"."amm_produits";')
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "nom": r[1], "titulaire": r[2]} for r in rows]


def get_cancer_data():
    sql = read_sql_file("sql/generalite_sql.sql")
    conn = connection_postgres()
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "annee": row[0],
            "departement": row[1],
            "type_cancer": row[2],
            "classe_age": row[3],
            "sexe": row[4],
            "effectif_patients": row[5],
            "effectif_total": row[6],
            "quantite_en_kg": row[7],
        })
    return result