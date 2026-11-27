from datetime import date, time

import FreeSimpleGUI as sg


class TelaAtendimento:
    def __init__(
        self,
        controladorAtendimento,
        controladorClinica,
        controladorPaciente,
        controladorProfissional,
    ):
        self.__controladorAtendimento = controladorAtendimento
        self.__controladorClinica = controladorClinica
        self.__controladorPaciente = controladorPaciente
        self.__controladorProfissional = controladorProfissional

    def tela_opcoes(self):
        layout = [
            [sg.Text("Atendimentos", font=("Segoe UI", 16, "bold"), justification="center", expand_x=True)],
            [sg.Button("Cadastrar atendimento", size=(28, 2), key="-CADASTRAR-")],
            [sg.Button("Listar atendimentos", size=(28, 2), key="-LISTAR-")],
            [sg.Button("Editar atendimento", size=(28, 2), key="-EDITAR-")],
            [sg.Button("Remover atendimento", size=(28, 2), key="-REMOVER-")],
            [sg.Button("Voltar", size=(28, 2), key="-VOLTAR-")],
        ]

        janela = sg.Window("Atendimentos", layout, element_justification="center")
        evento, _ = janela.read()
        janela.close()

        opcoes = {
            "-CADASTRAR-": 1,
            "-LISTAR-": 2,
            "-EDITAR-": 3,
            "-REMOVER-": 4,
            "-VOLTAR-": 0,
            sg.WIN_CLOSED: 0,
        }
        return opcoes.get(evento)

    def mostra_mensagem(self, mensagem):
        sg.popup_ok(str(mensagem), title="Atendimento")

    def escolher_clinica(self):
        return self.__seleciona_item(
            self.__controladorClinica.clinicas,
            "Clínicas cadastradas",
            "Nenhuma clínica cadastrada.",
            self.__formata_clinica,
        )

    def escolher_paciente(self):
        return self.__seleciona_item(
            self.__controladorPaciente.pacientes,
            "Pacientes cadastrados",
            "Nenhum paciente cadastrado.",
            self.__formata_paciente,
        )

    def escolher_profissional(self):
        return self.__seleciona_item(
            self.__controladorProfissional.profissionais,
            "Profissionais cadastrados",
            "Nenhum profissional cadastrado.",
            self.__formata_profissional,
        )

    def escolher_tipo_atendimento(self):
        tipos = ["Consulta", "Exame", "Retorno", "Outro"]
        layout = [
            [sg.Text("Tipo de atendimento")],
            [sg.Combo(tipos, default_value=tipos[0], readonly=True, key="-TIPO-")],
            [sg.Button("Confirmar", key="-CONFIRMAR-"), sg.Button("Cancelar", key="-CANCELAR-")],
        ]
        janela = sg.Window("Tipo de atendimento", layout, modal=True)
        evento, valores = janela.read()
        janela.close()

        if evento != "-CONFIRMAR-":
            return None
        return valores["-TIPO-"]

    def pega_dados_atendimento(self):
        clinica = self.escolher_clinica()
        if clinica is None:
            return None

        paciente = self.escolher_paciente()
        if paciente is None:
            return None

        profissional = self.escolher_profissional()
        if profissional is None:
            return None

        tipo_atendimento = self.escolher_tipo_atendimento()
        if tipo_atendimento is None:
            return None

        layout = [
            [sg.Text(f"Clínica: {clinica.nome} | Paciente: {paciente.nome}")],
            [sg.Text(f"Profissional: {profissional.nome} | Tipo: {tipo_atendimento}")],
            [sg.Text("Data (AAAA-MM-DD)")],
            [sg.Input(key="-DATA-")],
            [sg.Text("Horário de início (HH:MM)")],
            [sg.Input(key="-INICIO-")],
            [sg.Text("Horário de término (HH:MM)")],
            [sg.Input(key="-FIM-")],
            [sg.Text("", key="-ERRO-", text_color="red")],
            [sg.Button("Salvar", key="-SALVAR-"), sg.Button("Cancelar", key="-CANCELAR-")],
        ]
        janela = sg.Window("Dados do atendimento", layout, modal=True)

        while True:
            evento, valores = janela.read()
            if evento in (sg.WIN_CLOSED, "-CANCELAR-"):
                janela.close()
                return None
            if evento != "-SALVAR-":
                continue

            try:
                data_atendimento = date.fromisoformat(valores["-DATA-"].strip())
                horario_inicio = time.fromisoformat(valores["-INICIO-"].strip())
                horario_fim = time.fromisoformat(valores["-FIM-"].strip())
            except ValueError:
                janela["-ERRO-"].update(
                    "Data ou horário inválido. Use AAAA-MM-DD e HH:MM."
                )
                continue

            if horario_fim <= horario_inicio:
                janela["-ERRO-"].update(
                    "O horário final deve ser maior que o horário inicial."
                )
                continue

            if not self.__controladorAtendimento.horario_dentro_da_clinica(
                clinica, horario_inicio, horario_fim
            ):
                janela["-ERRO-"].update(
                    "O atendimento deve ocorrer dentro do horário da clínica "
                    f"({clinica.horario_funcionamento_inicial}h às "
                    f"{clinica.horario_funcionamento_final}h)."
                )
                continue

            janela.close()
            return {
                "clinica": clinica,
                "paciente": paciente,
                "profissional": profissional,
                "data": data_atendimento,
                "horario_inicio": horario_inicio,
                "horario_fim": horario_fim,
                "tipo_atendimento": tipo_atendimento,
            }

    def lista_atendimentos(self, atendimentos):
        if not atendimentos:
            self.mostra_mensagem("Nenhum atendimento cadastrado.")
            return

        self.__mostra_lista(
            atendimentos,
            "Atendimentos cadastrados",
            self.__formata_atendimento,
        )

    def seleciona_atendimento(self, atendimentos):
        if not atendimentos:
            self.mostra_mensagem("Nenhum atendimento cadastrado.")
            return None

        return self.__seleciona_item(
            atendimentos,
            "Selecione um atendimento",
            "Nenhum atendimento cadastrado.",
            self.__formata_atendimento,
        )

    def __seleciona_item(self, itens, titulo, mensagem_vazia, formatador):
        if not itens:
            self.mostra_mensagem(mensagem_vazia)
            return None

        return self.__mostra_lista(
            itens,
            titulo,
            formatador,
            permitir_selecao=True,
        )

    def __mostra_lista(self, itens, titulo, formatador, permitir_selecao=False):
        linhas = [formatador(item) for item in itens]
        chave_lista = "-ITENS-"
        layout = [
            [sg.Text(titulo, font=("Segoe UI", 14, "bold"))],
            [
                sg.Listbox(
                    linhas,
                    size=(82, 12),
                    expand_x=True,
                    expand_y=True,
                    key=chave_lista,
                    enable_events=permitir_selecao,
                )
            ],
            [
                sg.Button("Fechar", key="-FECHAR-"),
                sg.Button("Selecionar", key="-SELECIONAR-", visible=False),
            ],
        ]
        janela = sg.Window(titulo, layout, modal=True, resizable=True)

        while True:
            evento, valores = janela.read()
            if evento in (sg.WIN_CLOSED, "-FECHAR-"):
                janela.close()
                return None

            if permitir_selecao and evento == chave_lista:
                janela["-SELECIONAR-"].update(
                    visible=bool(valores[chave_lista])
                )
            elif (
                permitir_selecao
                and evento == "-SELECIONAR-"
                and valores[chave_lista]
            ):
                item = itens[linhas.index(valores[chave_lista][0])]
                janela.close()
                return item

    def __formata_clinica(self, clinica):
        return (
            f"{clinica.nome} | Cidade: {clinica.cidade} | "
            f"Horário: {clinica.horario_funcionamento_inicial}h às "
            f"{clinica.horario_funcionamento_final}h"
        )

    def __formata_paciente(self, paciente):
        return f"{paciente.nome} | CPF: {paciente.cpf}"

    def __formata_profissional(self, profissional):
        return (
            f"{profissional.nome} | CPF: {profissional.cpf} | "
            f"Especialidade: {profissional.especialidade}"
        )

    def __formata_atendimento(self, atendimento):
        return (
            f"{atendimento.data.isoformat()} | "
            f"{atendimento.horario_inicio.strftime('%H:%M')} às "
            f"{atendimento.horario_fim.strftime('%H:%M')} | "
            f"Paciente: {atendimento.paciente.nome} | "
            f"Profissional: {atendimento.profissional.nome} | "
            f"Clínica: {atendimento.clinica.nome} | "
            f"Tipo: {atendimento.tipoAtendimento} | "
            f"Valor: R$ {atendimento.valor:.2f}"
        )
