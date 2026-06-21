from dataclasses import dataclass

@dataclass
class Classification:
    GeneID: str
    Localization: str
    essenziale: str

    def __str__(self):
        return f"{self.GeneID}"

    def __hash__(self):
        return hash(self.GeneID)
