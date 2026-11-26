import pickle
from pathlib import Path


class RepositorioRelatorio:
    def __init__(self, caminho="dados/relatorios.pkl"):
        self.__caminho = Path(caminho)
        self.__caminho.parent.mkdir(parents=True, exist_ok=True)

    def salvar(self, relatorios):
        with open(self.__caminho, "wb") as arquivo:
            pickle.dump(relatorios, arquivo)

    def carregar(self):
        if not self.__caminho.exists():
            return []

        try:
            with open(self.__caminho, "rb") as arquivo:
                relatorios = pickle.load(arquivo)
            return relatorios if isinstance(relatorios, list) else []
        except (OSError, EOFError, pickle.PickleError):
            return []
