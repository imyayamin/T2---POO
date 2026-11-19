import pickle
from pathlib import Path


class RepositorioPaciente:
    def __init__(self, caminho="dados/pacientes.pkl"):
        self.__caminho = Path(caminho)
        self.__caminho.parent.mkdir(parents=True, exist_ok=True)

    def salvar(self, pacientes):
        with open(self.__caminho, "wb") as arquivo:
            pickle.dump(pacientes, arquivo)

    def carregar(self):
        if not self.__caminho.exists():
            return []

        try:
            with open(self.__caminho, "rb") as arquivo:
                pacientes = pickle.load(arquivo)
            return pacientes if isinstance(pacientes, list) else []
        except (OSError, EOFError, pickle.PickleError):
            return []
