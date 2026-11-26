import pickle
from pathlib import Path


class RepositorioProfissional:
    def __init__(self, caminho="dados/profissionais.pkl"):
        self.__caminho = Path(caminho)
        self.__caminho.parent.mkdir(parents=True, exist_ok=True)

    def salvar(self, profissionais):
        with open(self.__caminho, "wb") as arquivo:
            pickle.dump(profissionais, arquivo)

    def carregar(self):
        if not self.__caminho.exists():
            return []

        try:
            with open(self.__caminho, "rb") as arquivo:
                profissionais = pickle.load(arquivo)
            return profissionais if isinstance(profissionais, list) else []
        except (OSError, EOFError, pickle.PickleError):
            return []
