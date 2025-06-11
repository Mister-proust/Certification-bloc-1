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
