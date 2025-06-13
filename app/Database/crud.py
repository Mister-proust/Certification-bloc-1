from Database.db import connection_postgres

def test_fonction_sql():
    conn = connection_postgres()
    cursor = conn.cursor()
    cursor.execute('SELECT amm, "Nom_produit", titulaire FROM "Pollution_Cancer"."amm_produits";')
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "nom": r[1], "toxicite": r[2]} for r in rows]
