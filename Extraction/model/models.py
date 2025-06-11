from typing import Optional
from sqlmodel import Field, SQLModel 

class EffectifCancer(SQLModel, table=True):
    __tablename__ = "Effectif_cancer"

    id_effectif_cancer: int = Field(default = None, primary_key=True)

    Annee: int
    Pathologie: str = Field(max_length = 64)
    Type_cancer: str = Field(max_length = 128)
    Suivi_patho: str = Field(max_length = 128)
    Classe_age: str = Field(max_length = 12)
    Sexe: int
    Departement: int = Field(foreign_key="Metadata_effectif_departement.COD_MOD")
    Effectif_patients: Optional[int] = Field(default=None)
    Effectif_total: Optional[int] = Field(default=None)

    def __repr__(self):
        return f"EffectifCancer(id={self.id_effectif_cancer}, Annee={self.Annee}, Departement={self.Departement})"

class Effectifdepartement(SQLModel, table=True):
    __tablename__="Effectif_departement"

    id_effectif_departement : int = Field(default = None, primary_key=True)

    Num_dep : int=Field(foreign_key="Metadata_effectif_departement.COD_MOD")
    Carac_dep : str = Field(default= None, max_length = 8)
    Sexe : str = Field(max_length = 2, foreign_key="Metadata_effectif_departement.COD_MOD")
    Age : str = Field(max_length = 8, foreign_key="Metadata_effectif_departement.COD_MOD")
    Carac_mesure : str = Field(default= None, max_length = 8, foreign_key="Metadata_effectif_departement.COD_MOD")
    Chiffre_def : str = Field(default= None, max_length = 2)
    Annee : int = Field(default= None)
    Effectif int = Field(default= None)

    def __repr__(self):
        return f"Effectifdepartement(id={self.id_effectif_departement}, Num_dep={self.Num_dep}, Annee={self.Annee})"


class Metadataeffectifdepartement(SQLModel, table=True):
    __tablename__="Metadata_effectif_departement"

    COD_VAR: str = Field(max_length = 12)
    LIB_VAR: str = Field(max_length = 12)
    COD_MOD : str = Filed(max_length = 128, primary_key=True)
    LIB_MOD: str = Field(max_length = 24)

    def__repr__(self):
        return f"Metadataeffectifdepartement(COD_MOD={self.COD_MOD}, LIB_MOD={self.LIB_MOD})"


class Produitsvente(SQLModel, table=True): 
    __tablename__="Produits_vente"

    id_produits_vente: int = Field(default = None, primary_key=True)
    amm: int = Field(foreign_key="amm_produits.amm")
    annee: int = Field(default= None)
    num_departement: int=Field(foreign_key="Metadata_effectif_departement.COD_MOD")
    autorise_jardin : Optionnal[bool]=Field(default=None) 
    département : str = Field(default= None, max_length = 64)
    quantité_en_kg : int = Field(default=None)
    unite: str = Field(default= None, max_length = 2)

    def__repr__(self):
        return f"Produitsvente(id={self.id_produits_vente}, amm={self.amm}, quantité_en_kg={self.quantité_en_kg})"


class Substancecmrvente(SQLModel, table=True): 
    __tablename__="Substance_cmr_vente"

    id_substance: int = Field(default = None, primary_key=True)
    amm: int = Field(foreign_key="amm_produits.amm")
    annee : int = Field(default= None)
    classification_mention: str=Field(default= None, max_length = 20)
    code_cas: str=Field(default= None, max_length = 20)
    code_substance: str=Field(default= None, max_length = 20)
    num_departement: int=Field(foreign_key="Metadata_effectif_departement.COD_MOD")
    fonction: str=Field(default= None, max_length = 32)
    nom_substance: str=Field(default= None, max_length = 64)
    département: str=Field(default= None, max_length = 32)
    quantite_en_kg: int = Field(default=None)

    def__repr__(self):
        return f"Substancecmrvente(id={self.id_substance}, amm={self.amm}, classification_mention={self.classification_mention})"


class Ammmentiondanger(SQLModel, table=True): 
    __tablename__="amm_mention_danger"

    id_amm_danger = Field(default = None, primary_key=True)
    amm: int = Field(foreign_key="amm_produits.amm")
    Nom_produit: str=Field(default= None, max_length = 64)
    Libellé_court: str=Field(default= None, max_length = 8)
    Toxicite_produit: str=Field(default= None, max_length = 260)

    def __repr__(self):
        return f"Ammmentiondanger(id={self.id_amm_danger}, amm={self.amm}, Toxicite_produit={self.Toxicite_produit})"


class Ammproduits(SQLModel, table=True): 
    __tablename__="amm_produits"

    amm: int = Field(primary_key=True)
    Nom_produit: str=Field(default= None, max_length = 32)
    Second_noms_commerciaux: str=Field(default= None, max_length = 32)
    titulaire: str=Field(default= None, max_length = 32)
    Type_commercial: str=Field(default= None, max_length = 32)
    Gamme_usage: str=Field(default= None, max_length = 16)
    Mentions_autorisees: str=Field(default= None, max_length = 128)
    Restrictions_usage: str=Field(default= None, max_length = 128)
    Restrictions_usage_libelle: str=Field(default= None, max_length = 128)
    Substances_actives: str=Field(default= None, max_length = 256)
    Fonctions: str=Field(default= None, max_length = 32)
    Formulations: str=Field(default= None, max_length = 32)
    Etat_d_autorisation: str=Field(default= None, max_length = 16)
    Date_de_retrait: Optional[date] = Field(default=None)
    Date_première_autorisation: Optional[date] = Field(default=None)
    Numero_AMM_reference: str=Field(default= None, max_length = 32)
    Nom_produit_reference: str=Field(default= None, max_length = 32)
    
    def__repr__(self):
        return f"Ammproduits(amm={self.amm}, Nom_produit={self.Nom_produit}, Substances_actives={self.Substances_actives})"


    