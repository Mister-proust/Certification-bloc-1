from typing import Optional
from sqlmodel import Field, SQLModel 
from datetime import date
from decimal import Decimal


class MetadataAge(SQLModel, table=True): 
    __tablename__="metadata_age"
    Code : str = Field(max_length = 32, primary_key=True)
    Libelle : str = Field(max_length=64)
    Age_median : Optional[int] = Field(nullable=True)
    __table_args__ = {"schema": "Pollution_Cancer"}
    def __repr__(self):
        return f"MetadataAge(id={self.code}, libelle={self.Libelle})"

class MetadataAnnee(SQLModel, table=True): 
    __tablename__="metadata_annee"
    Code : int = Field(primary_key=True)
    Libelle : str = Field(max_length=64)
    __table_args__ = {"schema": "Pollution_Cancer"}
    def __repr__(self):
        return f"MetadataAnnee(id={self.code}, libelle={self.Libelle})"

class MetadataSexe(SQLModel, table=True): 
    __tablename__="metadata_sexe"
    Code : str = Field(max_length = 32, primary_key=True)
    Libelle : str = Field(max_length=64)
    __table_args__ = {"schema": "Pollution_Cancer"}
    def __repr__(self):
        return f"MetadataSexe(id={self.code}, libelle={self.Libelle})"

class MetadataDepartement(SQLModel, table=True): 
    __tablename__="metadata_departement"
    Code : str = Field(max_length = 32, primary_key=True)
    Libelle : str = Field(max_length=64)
    __table_args__ = {"schema": "Pollution_Cancer"}
    def __repr__(self):
        return f"MetadataDepartement(id={self.code}, libelle={self.Libelle})"

class MetadataObsStatus(SQLModel, table=True): 
    __tablename__="metadata_obs_status"
    Code : str = Field(max_length = 32, primary_key=True)
    Libelle : str = Field(max_length=64)
    __table_args__ = {"schema": "Pollution_Cancer"}
    def __repr__(self):
        return f"MetadataObsStatus(id={self.code}, libelle={self.Libelle})"

class MetadataStats(SQLModel, table=True): 
    __tablename__="metadata_stats"
    Code : str = Field(max_length = 32, primary_key=True)
    Libelle : str = Field(max_length=256)
    __table_args__ = {"schema": "Pollution_Cancer"}
    def __repr__(self):
        return f"MetadataStats(id={self.code}, libelle={self.Libelle})"

class EffectifCancer(SQLModel, table=True):
    __tablename__ = "Effectif_cancer"
    id_effectif_cancer: int = Field(default = None, primary_key=True)
    Annee: int = Field(foreign_key="Pollution_Cancer.metadata_annee.Code")
    Pathologie: str = Field(max_length = 16)
    Type_cancer: str = Field(max_length = 64)
    Suivi_patho: str = Field(max_length = 64)
    Classe_age: str = Field(max_length = 32, foreign_key="Pollution_Cancer.metadata_age.Code")
    Sexe: str = Field(max_length = 4, foreign_key="Pollution_Cancer.metadata_sexe.Code")
    Departement: str = Field(foreign_key="Pollution_Cancer.metadata_departement.Code", max_length = 4)
    Effectif_patients: Optional[Decimal] = Field(default=None, nullable=True)
    Effectif_total: Optional[int] = Field(default=None, nullable=True)
    __table_args__ = {"schema": "Pollution_Cancer"}
    def __repr__(self):
        return f"EffectifCancer(id={self.id_effectif_cancer}, Annee={self.Annee}, Departement={self.Departement})"

class EffectifDepartement(SQLModel, table=True):
    __tablename__="Effectif_departement"
    id_effectif_departement : int = Field(default = None, primary_key=True)
    Num_dep : str=Field(foreign_key="Pollution_Cancer.metadata_departement.Code", max_length = 12)
    Carac_dep : Optional[str] = Field(default= None, max_length = 8, nullable=True)
    Sexe : str = Field(max_length = 2, foreign_key="Pollution_Cancer.metadata_sexe.Code")
    Age : str = Field(max_length = 16, foreign_key="Pollution_Cancer.metadata_age.Code")
    Carac_mesure : Optional[str] = Field(default= None, max_length = 32, foreign_key="Pollution_Cancer.metadata_stats.Code", nullable=True)
    Chiffre_def : Optional[str] = Field(default= None, max_length = 16, foreign_key="Pollution_Cancer.metadata_obs_status.Code", nullable=True)
    Annee : int = Field(default= None)
    Effectif : Optional[Decimal] = Field(default= None, nullable=True)
    __table_args__ = {"schema": "Pollution_Cancer"}
    def __repr__(self):
        return f"EffectifDepartement(id={self.id_effectif_departement}, Num_dep={self.Num_dep}, Annee={self.Annee})"


class ProduitsVente(SQLModel, table=True): 
    __tablename__="Produits_vente"
    id_produits_vente: int = Field(default = None, primary_key=True)
    amm: int = Field(foreign_key="Pollution_Cancer.amm_produits.amm")
    annee: int = Field(default= None, foreign_key="Pollution_Cancer.metadata_annee.Code")
    num_departement: str=Field(foreign_key="Pollution_Cancer.metadata_departement.Code", max_length = 4)
    autorise_jardin : Optional[str]=Field(default=None, max_length=8, nullable=True) 
    quantite_en_kg : Optional[Decimal] = Field(default=None, nullable=True)
    unite: Optional[str] = Field(default= None, max_length = 2, nullable=True)
    __table_args__ = {"schema": "Pollution_Cancer"}
    def __repr__(self):
        return f"Produitsvente(id={self.id_produits_vente}, amm={self.amm}, quantité_en_kg={self.quantité_en_kg})"


class SubstanceCMRVente(SQLModel, table=True): 
    __tablename__="Substance_cmr_vente"
    id_substance: int = Field(default = None, primary_key=True)
    amm: int = Field(foreign_key="Pollution_Cancer.amm_produits.amm")
    annee : int = Field(default= None, foreign_key="Pollution_Cancer.metadata_annee.Code")
    classification_mention: Optional[str]=Field(default= None, max_length = 20, nullable=True)
    code_cas: Optional[str]=Field(default= None, max_length = 32, nullable=True)
    code_substance: Optional[int]=Field(default= None, nullable=True)
    num_departement: str=Field(foreign_key="Pollution_Cancer.metadata_departement.Code", max_length = 4)
    fonction: Optional[str]=Field(default= None, max_length = 128, nullable=True)
    nom_substance: Optional[str]=Field(default= None, max_length = 256, nullable=True)
    quantite_en_kg: Optional[Decimal] = Field(default=None, nullable=True)
    __table_args__ = {"schema": "Pollution_Cancer"}
    def __repr__(self):
        return f"Substancecmrvente(id={self.id_substance}, amm={self.amm}, classification_mention={self.classification_mention})"


class AmmMentionDanger(SQLModel, table=True): 
    __tablename__="amm_mention_danger"
    id_amm_danger : int = Field(default = None, primary_key=True)
    amm: int = Field(foreign_key="Pollution_Cancer.amm_produits.amm")
    Nom_produit: Optional[str]=Field(default= None, max_length = 64, nullable=True)
    Libellé_court: Optional[str]=Field(default= None, max_length = 36, nullable=True)
    Toxicite_produit: Optional[str]=Field(default= None, max_length = 260, nullable=True)
    __table_args__ = {"schema": "Pollution_Cancer"}
    def __repr__(self):
        return f"Ammmentiondanger(id={self.id_amm_danger}, amm={self.amm}, Toxicite_produit={self.Toxicite_produit})"


class AmmProduits(SQLModel, table=True): 
    __tablename__="amm_produits"
    amm: int = Field(primary_key=True)
    Nom_produit: Optional[str]=Field(default= None, max_length = 64, nullable=True)
    Second_noms_commerciaux: Optional[str]=Field(default= None, max_length = 512, nullable=True)
    titulaire: Optional[str]=Field(default= None, max_length = 124, nullable=True)
    Type_commercial: Optional[str]=Field(default= None, max_length = 64, nullable=True)
    Gamme_usage: Optional[str]=Field(default= None, max_length = 128, nullable=True)
    Mentions_autorisees: Optional[str]=Field(default= None, max_length = 128, nullable=True)
    Restrictions_usage: Optional[str]=Field(default= None, max_length = 128, nullable=True)
    Restrictions_usage_libelle: Optional[str]=Field(default= None, max_length = 1024, nullable=True)
    Substances_actives: Optional[str]=Field(default= None, max_length = 512, nullable=True)
    Fonctions: Optional[str]=Field(default= None, max_length = 256, nullable=True)
    Formulations: Optional[str]=Field(default= None, max_length = 128, nullable=True)
    Etat_d_autorisation: Optional[str]=Field(default= None, max_length = 32, nullable=True)
    Date_de_retrait: Optional[date] = Field(default=None, nullable=True)
    Date_première_autorisation: Optional[date] = Field(default=None, nullable=True)
    Numero_AMM_reference:Optional[str]=Field(default= None, max_length = 64, nullable=True)
    Nom_produit_reference: Optional[str]=Field(default= None, max_length = 128, nullable=True)
    __table_args__ = {"schema": "Pollution_Cancer"}
    def __repr__(self):
        return f"Ammproduits(amm={self.amm}, Nom_produit={self.Nom_produit}, Substances_actives={self.Substances_actives})"


