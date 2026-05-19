from dataclasses import dataclass, field

#Faz a ligação de informações entre as verificações

@dataclass
class DadosPDF:
    feriados: list = field(default_factory=list)
    quantidade_de_pas_especializada: int = field(default_factory=int)