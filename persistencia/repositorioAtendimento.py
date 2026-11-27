import pickle
from pathlib import Path


class RepositorioAtendimento:
    def __init__(self, caminho="dados/atendimentos.pkl"):
        self.__caminho = Path(caminho)
        self.__caminho.parent.mkdir(parents=True, exist_ok=True)

    def salvar(self, atendimentos):
        with open(self.__caminho, "wb") as arquivo:
            pickle.dump(atendimentos, arquivo)

    def carregar(self):
        if not self.__caminho.exists():
            return []

        try:
            with open(self.__caminho, "rb") as arquivo:
                atendimentos = pickle.load(arquivo)
            return atendimentos if isinstance(atendimentos, list) else []
        except (OSError, EOFError, pickle.PickleError):
            return []
