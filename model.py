from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


class ChapadurHardboard(BaseModel):
    apto_s_film: int
    second: int
    third: int
    plastificado: int
    no_apto: int
    total: int
    informado: int
    diferencia: int
    no_apto_percentage: float
    motivo_descartes: str


class PalletsArlog(BaseModel):
    oi: int
    branca: int
    reparacion: int
    no_apto: int
    total: int
    informado: int
    diferencia: int
    no_apto_percentage: float
    motivo_descartes: str


class MarcosDeMadera(BaseModel):
    apto: int
    no_apto_mnpncr: int
    no_apto: int
    total: int
    informado: int
    diferencia: int
    no_apto_percentage: float
    motivo_descartes: str


class Report(BaseModel):
    num_informe: int
    cliente: str
    num_remit: str
    reception_date: datetime
    chapadur_hardboard: ChapadurHardboard
    pallets_arlog: PalletsArlog
    marcos_de_madera: MarcosDeMadera
    fecha_fin_proceso_chapadur: datetime
    fecha_fin_proceso_pallet_marco: datetime
    observaciones: Optional[List[str]]
