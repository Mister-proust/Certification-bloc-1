from typing import Optional
from sqlmodel import Field, SQLModel 
from datetime import date

class EffectifCancer(SQLModel, table=True):
    __tablename__ = "Effectif_cancer"

    id_effectif_cancer: int = Field(default = None, primary_key=True)

    Annee: int
    Pathologie: str = Field(max_length = 64)
    Type_cancer: str = Field(max_length = 128)
    Suivi_patho: str = Field(max_length = 128)
    Classe_age: str = Field(max_length = 12)
    Sexe: int
    Departement: str = Field(foreign_key="Pollution_Cancer.Metadata_effectif_departement.COD_MOD", max_length = 4)
    Effectif_patients: Optional[int] = Field(default=None)
    Effectif_total: Optional[int] = Field(default=None)


    __table_args__ = {"schema": "Pollution_Cancer"}

    def __repr__(self):
        return f"EffectifCancer(id={self.id_effectif_cancer}, Annee={self.Annee}, Departement={self.Departement})"

class Effectifdepartement(SQLModel, table=True):
    __tablename__="Effectif_departement"

    id_effectif_departement : int = Field(default = None, primary_key=True)

    Num_dep : str=Field(foreign_key="Pollution_Cancer.Metadata_effectif_departement.COD_MOD", max_length = 4)
    Carac_dep : str = Field(default= None, max_length = 8)
    Sexe : str = Field(max_length = 2, foreign_key="Pollution_Cancer.Metadata_effectif_departement.COD_MOD")
    Age : str = Field(max_length = 8, foreign_key="Pollution_Cancer.Metadata_effectif_departement.COD_MOD")
    Carac_mesure : str = Field(default= None, max_length = 8, foreign_key="Pollution_Cancer.Metadata_effectif_departement.COD_MOD")
    Chiffre_def : str = Field(default= None, max_length = 2)
    Annee : int = Field(default= None)
    Effectif : int = Field(default= None)


    __table_args__ = {"schema": "Pollution_Cancer"}

    def __repr__(self):
        return f"Effectifdepartement(id={self.id_effectif_departement}, Num_dep={self.Num_dep}, Annee={self.Annee})"


class Metadataeffectifdepartement(SQLModel, table=True):
    __tablename__="Metadata_effectif_departement"

    COD_VAR: str = Field(max_length = 12)
    LIB_VAR: str = Field(max_length = 12)
    COD_MOD : str = Field(max_length = 128, primary_key=True)
    LIB_MOD: str = Field(max_length = 24)


    __table_args__ = {"schema": "Pollution_Cancer"}

    def __repr__(self):
        return f"Metadataeffectifdepartement(COD_MOD={self.COD_MOD}, LIB_MOD={self.LIB_MOD})"


class Produitsvente(SQLModel, table=True): 
    __tablename__="Produits_vente"

    id_produits_vente: int = Field(default = None, primary_key=True)
    amm: int = Field(foreign_key="Pollution_Cancer.amm_produits.amm")
    annee: int = Field(default= None)
    num_departement: str=Field(foreign_key="Pollution_Cancer.Metadata_effectif_departement.COD_MOD", max_length = 4)
    autorise_jardin : Optional[bool]=Field(default=None) 
    département : str = Field(default= None, max_length = 64)
    quantité_en_kg : int = Field(default=None)
    unite: str = Field(default= None, max_length = 2)


    __table_args__ = {"schema": "Pollution_Cancer"}

    def __repr__(self):
        return f"Produitsvente(id={self.id_produits_vente}, amm={self.amm}, quantité_en_kg={self.quantité_en_kg})"


class Substancecmrvente(SQLModel, table=True): 
    __tablename__="Substance_cmr_vente"

    id_substance: int = Field(default = None, primary_key=True)
    amm: int = Field(foreign_key="Pollution_Cancer.amm_produits.amm")
    annee : int = Field(default= None)
    classification_mention: str=Field(default= None, max_length = 20)
    code_cas: str=Field(default= None, max_length = 20)
    code_substance: str=Field(default= None, max_length = 20)
    num_departement: str=Field(foreign_key="Pollution_Cancer.Metadata_effectif_departement.COD_MOD", max_length = 4)
    fonction: str=Field(default= None, max_length = 32)
    nom_substance: str=Field(default= None, max_length = 64)
    département: str=Field(default= None, max_length = 32)
    quantite_en_kg: int = Field(default=None)


    __table_args__ = {"schema": "Pollution_Cancer"}

    def __repr__(self):
        return f"Substancecmrvente(id={self.id_substance}, amm={self.amm}, classification_mention={self.classification_mention})"


class Ammmentiondanger(SQLModel, table=True): 
    __tablename__="amm_mention_danger"

    id_amm_danger : int = Field(default = None, primary_key=True)
    amm: int = Field(foreign_key="Pollution_Cancer.amm_produits.amm")
    Nom_produit: Optional[str]=Field(default= None, max_length = 64, nullable=True)
    Libellé_court: Optional[str]=Field(default= None, max_length = 64, nullable=True)
    Toxicite_produit: Optional[str]=Field(default= None, max_length = 260, nullable=True)


    __table_args__ = {"schema": "Pollution_Cancer"}

    def __repr__(self):
        return f"Ammmentiondanger(id={self.id_amm_danger}, amm={self.amm}, Toxicite_produit={self.Toxicite_produit})"


class Ammproduits(SQLModel, table=True): 
    __tablename__="amm_produits"

    amm: int = Field(primary_key=True)
    Nom_produit: Optional[str]=Field(default= None, max_length = 64, nullable=True)
    Second_noms_commerciaux: Optional[str]=Field(default= None, max_length = 64, nullable=True)
    titulaire: Optional[str]=Field(default= None, max_length = 64, nullable=True)
    Type_commercial: Optional[str]=Field(default= None, max_length = 64, nullable=True)
    Gamme_usage: Optional[str]=Field(default= None, max_length = 128, nullable=True)
    Mentions_autorisees: Optional[str]=Field(default= None, max_length = 128, nullable=True)
    Restrictions_usage: Optional[str]=Field(default= None, max_length = 128, nullable=True)
    Restrictions_usage_libelle: Optional[str]=Field(default= None, max_length = 128, nullable=True)
    Substances_actives: Optional[str]=Field(default= None, max_length = 256, nullable=True)
    Fonctions: Optional[str]=Field(default= None, max_length = 64, nullable=True)
    Formulations: Optional[str]=Field(default= None, max_length = 64, nullable=True)
    Etat_d_autorisation: Optional[str]=Field(default= None, max_length = 64, nullable=True)
    Date_de_retrait: Optional[date] = Field(default=None, nullable=True)
    Date_première_autorisation: Optional[date] = Field(default=None, nullable=True)
    Numero_AMM_reference:Optional[str]=Field(default= None, max_length = 64, nullable=True)
    Nom_produit_reference: Optional[str]=Field(default= None, max_length = 64, nullable=True)


    __table_args__ = {"schema": "Pollution_Cancer"}
    
    def __repr__(self):
        return f"Ammproduits(amm={self.amm}, Nom_produit={self.Nom_produit}, Substances_actives={self.Substances_actives})"


    