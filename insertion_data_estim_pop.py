import pandas as pd
import json
import io

# --- 1. Simuler le contenu du fichier CSV ---
# Dans un cas réel, vous liriez directement depuis un fichier CSV.
# Ici, nous utilisons StringIO pour simuler un fichier à partir de la chaîne fournie.
csv_data = """GEO	GEO_OBJECT	SEX	AGE	EP_MEASURE	OBS_STATUS_FR	TIME_PERIOD	OBS_VALUE
78	DEP	M	Y50T54	POP	D	2007	44919
85	DEP	M	Y60T64	POP	D	2007	15680
82	DEP	F	Y15T19	POP	D	2007	6516
79	DEP	_T	Y25T29	POP	D	2007	19285
62	DEP	F	Y_LT5	POP	D	2007	47222
80	DEP	F	Y25T29	POP	D	2007	17497
81	DEP	F	Y70T74	POP	D	2007	10206
90	DEP	M	Y10T14	POP	D	2007	4411
80	DEP	F	Y75T79	POP	D	2007	12127
79	DEP	_T	Y_GE_0	POP	D	2007	600000 # Ajout d'une ligne avec AGE=_GE_0 pour le total
85	DEP	_T	Y_GE_0	POP	D	2008	700000 # Ajout d'une ligne pour une autre année
"""

# Utilisez io.StringIO pour lire la chaîne comme un fichier
df = pd.read_csv(io.StringIO(csv_data), sep='\t')

print("--- DataFrame initial ---")
print(df)
print("\n" + "="*30 + "\n")

# --- 2. Application des filtres ---
# GEO_OBJECT doit être "DEP"
# SEX doit être "_T"
df_filtered = df[(df['GEO_OBJECT'] == 'DEP') & (df['SEX'] == '_T')].copy()

print("--- DataFrame après filtrage ---")
print(df_filtered)
print("\n" + "="*30 + "\n")

# --- 3. Suppression des colonnes non désirées ---
columns_to_drop = ['GEO_OBJECT', 'SEX', 'EP_MEASURE', 'OBS_STATUS_FR']
df_transformed = df_filtered.drop(columns=columns_to_drop)

print("--- DataFrame après suppression de colonnes ---")
print(df_transformed)
print("\n" + "="*30 + "\n")

# --- 4. Restructuration pour le format JSON de MongoDB ---
# L'objectif est d'avoir:
# {
#   "GEO": "département_code",
#   "annees": [
#     {
#       "TIME_PERIOD": année,
#       "ages": [
#         { "AGE": "tranche_age", "OBS_VALUE": population },
#         ...
#       ]
#     },
#     ...
#   ]
# }

# Créer un dictionnaire pour stocker les données sous la forme souhaitée
mongo_docs = {}

for index, row in df_transformed.iterrows():
    geo = str(row['GEO']) # Convertir en string pour s'assurer d'un ID de département
    time_period = int(row['TIME_PERIOD'])
    age = str(row['AGE'])
    obs_value = int(row['OBS_VALUE'])

    if geo not in mongo_docs:
        mongo_docs[geo] = {
            "GEO": geo,
            "annees": []
        }

    # Chercher si l'année existe déjà pour ce GEO
    annee_found = False
    for annee_entry in mongo_docs[geo]['annees']:
        if annee_entry['TIME_PERIOD'] == time_period:
            # Ajouter la tranche d'âge et sa population à cette année
            if 'ages' not in annee_entry: # S'assurer que le tableau 'ages' existe
                annee_entry['ages'] = []
            annee_entry['ages'].append({"AGE": age, "OBS_VALUE": obs_value})
            annee_found = True
            break
    
    # Si l'année n'a pas été trouvée, la créer et ajouter la première tranche d'âge
    if not annee_found:
        mongo_docs[geo]['annees'].append({
            "TIME_PERIOD": time_period,
            "ages": [{"AGE": age, "OBS_VALUE": obs_value}]
        })

# Convertir le dictionnaire de documents en une liste de documents
final_json_output = list(mongo_docs.values())

# --- 5. Affichage du JSON résultant ---
print("--- JSON final pour MongoDB (extrait du premier document) ---")
if final_json_output:
    print(json.dumps(final_json_output[0], indent=2)) # Afficher le premier document pour l'exemple
    print(f"\nTotal des documents JSON générés : {len(final_json_output)}")
else:
    print("Aucun document JSON généré après transformation.")

# --- 6. (Optionnel) Sauvegarder le JSON dans un fichier ---
output_filename = "demographie_estimation.json"
with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(final_json_output, f, ensure_ascii=False, indent=2)

print(f"\nLe JSON complet a été sauvegardé dans '{output_filename}'")

# --- 7. (Optionnel) Code pour l'insertion directe dans MongoDB ---
# Assurez-vous que MongoDB est en cours d'exécution (dbeaver connecté ne suffit pas toujours, le serveur doit tourner).
# client = MongoClient("mongodb://localhost:27017/") # Remplacez si votre URI est différente
# db = client["Bloc1"]
# collection = db["demographie_estimation"]

# # Supprimer les anciens documents si vous voulez un rechargement propre
# # collection.delete_many({})

# # Insérer les documents
# collection.insert_many(final_json_output)
# print(f"\nDonnées insérées dans la collection 'demographie_estimation' de la base 'Bloc1'.")

# # N'oubliez pas de fermer la connexion
# client.close()