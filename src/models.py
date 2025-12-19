from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class PowerStats:
    intelligence: int
    strength: int
    speed: int
    durability: int
    power: int
    combat: int

@dataclass
class Appearance:
    gender: str
    race: Optional[str]
    height: List[str]
    weight: List[str]
    eyeColor: str
    hairColor: str

@dataclass
class Biography:
    fullName: str
    alterEgos: str
    aliases: List[str]
    placeOfBirth: str
    firstAppearance: str
    publisher: Optional[str]
    alignment: str

@dataclass
class Hero:
    id: int
    name: str
    slug: str
    powerstats: PowerStats
    appearance: Appearance
    biography: Biography
    images: Dict[str, str]

    def validate_hero(self) -> bool:
        """
        Aplica las reglas de negocio estrictas:
        1. Debe ser de 'Marvel Comics'.
        2. CUALQUIER stat individual <= 15 descarta al héroe.
        3. No puede tener 3 o más stats en 0.
        4. No puede tener 3 o más stats en 100.
        """
        # 1. Filtro de Publisher (Estricto con strip)
        pub = self.biography.publisher
        if not pub or pub.strip() != "Marvel Comics":
            return False

        # Extraemos los valores numéricos para validación
        stats = [
            self.powerstats.intelligence,
            self.powerstats.strength,
            self.powerstats.speed,
            self.powerstats.durability,
            self.powerstats.power,
            self.powerstats.combat
        ]

        # 2. Filtro de Valor Mínimo Individual (Estricto)
        # Si ALGUNA estadística es menor o igual a 15, fuera.
        if min(stats) <= 15:
            return False

        # 3. Filtro de Ceros
        # Si tiene 3 o más stats en 0, fuera.
        if stats.count(0) >= 3:
            return False
            
        # 4. Filtro de "Dioses Falsos"
        # Si tiene 3 o más stats en 100, fuera.
        if stats.count(100) >= 3:
            return False

        return True