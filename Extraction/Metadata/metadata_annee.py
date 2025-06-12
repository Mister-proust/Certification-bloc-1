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

metadata_annee = Table(
    "metadata_annee", metadata,
    Column("Code", String, primary_key=True),
    Column("Libelle", String)
)

metadata.create_all(engine, checkfirst=True)

# Ajout des lignes dans la table.
def run(): 
    with engine.begin() as conn: 
        conn.execute(metadata_annee.insert().values([
            {"Code": "1990", "Libelle": "1990"},
            {"Code": "1991", "Libelle": "1991"},
            {"Code": "1992", "Libelle": "1992"},
            {"Code": "1993", "Libelle": "1993"},
            {"Code": "1994", "Libelle": "1994"},
            {"Code": "1995", "Libelle": "1995"},
            {"Code": "1996", "Libelle": "1996"},
            {"Code": "1997", "Libelle": "1997"},
            {"Code": "1998", "Libelle": "1998"},
            {"Code": "1999", "Libelle": "1999"},
            {"Code": "2000", "Libelle": "2000"},
            {"Code": "2001", "Libelle": "2001"},
            {"Code": "2002", "Libelle": "2002"},
            {"Code": "2003", "Libelle": "2003"},
            {"Code": "2004", "Libelle": "2004"},
            {"Code": "2005", "Libelle": "2005"},
            {"Code": "2006", "Libelle": "2006"},
            {"Code": "2007", "Libelle": "2007"},
            {"Code": "2008", "Libelle": "2008"},
            {"Code": "2009", "Libelle": "2009"},
            {"Code": "2010", "Libelle": "2010"},
            {"Code": "2011", "Libelle": "2011"},
            {"Code": "2012", "Libelle": "2012"},
            {"Code": "2013", "Libelle": "2013"},
            {"Code": "2014", "Libelle": "2014"},
            {"Code": "2015", "Libelle": "2015"},
            {"Code": "2016", "Libelle": "2016"},
            {"Code": "2017", "Libelle": "2017"},
            {"Code": "2018", "Libelle": "2018"},
            {"Code": "2019", "Libelle": "2019"},
            {"Code": "2020", "Libelle": "2020"},
            {"Code": "2021", "Libelle": "2021"},
            {"Code": "2022", "Libelle": "2022"},
            {"Code": "2023", "Libelle": "2023"},
            {"Code": "2024", "Libelle": "2024"},
            {"Code": "2025", "Libelle": "2025"}
        ]))
        conn.commit()
        print("metadata_annee inséré avec succès")


if __name__ == "__main__":
    run()


