from entidade.clinica import Clinica
from limite.telaClinica import TelaClinica
from exceptions.exceptions import (ListaVaziaException, ClinicaRepetidaException, HorarioInvalidoException)

class ControladorClinica:

    def __init__(self, controladorGeral):
        self.__clinicas = []
        self.__tela_clinica = TelaClinica()
        self.__controladorGeral = controladorGeral

    @property
    def clinicas(self):
        return self.__clinicas

    def pega_clinica_por_nome(self, nome: str):
        for clinica in self.__clinicas:
            if clinica.nome == nome:
                return clinica
        return None

    def incluir_clinica(self):
        try:
            dados_clinica = self.__tela_clinica.pega_dados_clinica()
        except ValueError as e:
            self.__tela_clinica.mostra_mensagem(str(e))
            return

        if dados_clinica is None:
            return

        try:
            horario_inicial = dados_clinica["horario_inicial"]
            horario_final = dados_clinica["horario_final"]
            nome = dados_clinica["nome"]

            if horario_inicial >= horario_final:
                raise HorarioInvalidoException()

            if self.pega_clinica_por_nome(nome) is not None:
                raise ClinicaRepetidaException(nome)

            nova_clinica = Clinica(
                nome,
                dados_clinica["cidade"],
                dados_clinica["descricao"],
                horario_inicial,
                horario_final
            )
            self.__clinicas.append(nova_clinica)
            self.__tela_clinica.mostra_mensagem("Clínica cadastrada com sucesso!")

        except (HorarioInvalidoException, ClinicaRepetidaException) as e:
            self.__tela_clinica.mostra_mensagem(str(e))

    def listar_clinicas(self, permitir_selecao=False):
        if not self.__clinicas:
            raise ListaVaziaException("clínicas")
        clinica_selecionada = self.__tela_clinica.lista_clinicas(
            self.__clinicas,
            permitir_selecao=permitir_selecao,
        )
        if permitir_selecao:
            return clinica_selecionada
        return self.__clinicas

    def remover_clinica(self):
        try:
            clinica = self.listar_clinicas(permitir_selecao=True)
        except ListaVaziaException as e:
            self.__tela_clinica.mostra_mensagem(str(e))
            return

        if clinica is None:
            return

        self.__clinicas.remove(clinica)
        self.__tela_clinica.mostra_mensagem("Clínica removida com sucesso!")

    def retornar(self):
        self.__controladorGeral.abre_tela()

    def abre_tela(self):
        lista_opcoes = {
            1: self.listar_clinicas,
            2: self.incluir_clinica,
            3: self.remover_clinica,
            0: self.retornar,
        }
        while True:
            opcao = self.__tela_clinica.tela_opcoes()
            funcao = lista_opcoes.get(opcao)
            if funcao is None:
                self.__tela_clinica.mostra_mensagem("Opção inválida.")
                continue
            
            try:
                funcao()
            except ListaVaziaException as e:
                self.__tela_clinica.mostra_mensagem(str(e))
    