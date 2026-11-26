import pickle
from pathlib import Path


class RepositorioClinica:
    def __init__(self, caminho="dados/clinicas.pkl"):
        self.__caminho = Path(caminho)
        self.__caminho.parent.mkdir(parents=True, exist_ok=True)

    def salvar(self, clinicas):
        with open(self.__caminho, "wb") as arquivo:
            pickle.dump(clinicas, arquivo)

    def carregar(self):
        if not self.__caminho.exists():
            return []

        try:
            with open(self.__caminho, "rb") as arquivo:
                clinicas = pickle.load(arquivo)
            return clinicas if isinstance(clinicas, list) else []
        except (OSError, EOFError, pickle.PickleError):
            return []
