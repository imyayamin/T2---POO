import FreeSimpleGUI as sg

from exceptions.exceptions import EntradaInvalidaException


class TelaPaciente:
    def tela_opcoes(self):
        layout = [
            [sg.Text("Pacientes", font=("Segoe UI", 16, "bold"), justification="center", expand_x=True)],
            [sg.Button("Listar pacientes", size=(24, 2), key="-LISTAR-")],
            [sg.Button("Cadastrar paciente", size=(24, 2), key="-CADASTRAR-")],
            [sg.Button("Remover paciente", size=(24, 2), key="-REMOVER-")],
            [sg.Button("Voltar", size=(24, 2), key="-VOLTAR-")],
        ]

        janela = sg.Window("Pacientes", layout, element_justification="center", finalize=True)
        evento, _ = janela.read()
        janela.close()

        if evento == "-LISTAR-":
            return 1
        if evento == "-CADASTRAR-":
            return 2
        if evento == "-REMOVER-":
            return 3
        if evento in ("-VOLTAR-", sg.WIN_CLOSED):
            return 0
        return None

    def pega_dados_paciente(self):
        layout = [
            [sg.Text("Nome")],
            [sg.Input(key="-NOME-")],
            [sg.Text("Celular")],
            [sg.Input(key="-CELULAR-")],
            [sg.Text("CPF")],
            [sg.Input(key="-CPF-")],
            [sg.Text("Idade")],
            [sg.Input(key="-IDADE-")],
            [sg.Button("Cadastrar"), sg.Button("Cancelar")],
        ]

        janela = sg.Window("Cadastrar paciente", layout, modal=True)
        evento, valores = janela.read()
        janela.close()

        if evento != "Cadastrar":
            raise EntradaInvalidaException("cadastro cancelado")

        nome = valores["-NOME-"].strip()
        celular = valores["-CELULAR-"].strip()
        cpf = valores["-CPF-"].strip()
        idade_texto = valores["-IDADE-"].strip()

        if not nome:
            raise EntradaInvalidaException("nome")

        try:
            celular = int(celular)
            cpf = int(cpf)
            idade = int(idade_texto)
        except (TypeError, ValueError):
            raise EntradaInvalidaException("dados do paciente")

        return {"nome": nome, "celular": celular, "cpf": cpf, "idade": idade}

    def pega_dados_acompanhante(self):
        layout = [
            [sg.Text("Nome do acompanhante")],
            [sg.Input(key="-ACOMPANHANTE-")],
            [sg.Button("Confirmar", key="-CONFIRMAR-"), sg.Button("Cancelar")],
        ]

        janela = sg.Window("Acompanhante", layout, modal=True)
        evento, valores = janela.read()
        janela.close()

        if evento != "-CONFIRMAR-":
            return None

        return valores["-ACOMPANHANTE-"].strip()

    def seleciona_paciente(self, paciente):
        layout = [
            [sg.Text(f"Confirme o CPF de {paciente.nome}")],
            [sg.Input(key="-CPF-")],
            [sg.Button("Remover", key="-REMOVER-"), sg.Button("Cancelar")],
        ]

        janela = sg.Window("Remover paciente", layout, modal=True)
        evento, valores = janela.read()
        janela.close()

        if evento != "-REMOVER-":
            return None

        try:
            return int(valores["-CPF-"].strip())
        except (TypeError, ValueError):
            raise EntradaInvalidaException("CPF")

    def lista_pacientes(self, pacientes, permitir_selecao=False):
        linhas = [
            f"{indice} - {paciente.nome} - CPF: {paciente.cpf} - Idade: {paciente.idade}"
            for indice, paciente in enumerate(pacientes, start=1)
        ]

        layout = [
            [sg.Text("Pacientes cadastrados", font=("Segoe UI", 14, "bold"))],
            [
                sg.Listbox(
                    linhas,
                    size=(60, 12),
                    expand_x=True,
                    expand_y=True,
                    key="-PACIENTES-",
                    enable_events=permitir_selecao,
                )
            ],
            [
                sg.Button("Fechar", key="-FECHAR-"),
                sg.Button("Selecionar", key="-SELECIONAR-", visible=False),
            ],
        ]

        janela = sg.Window("Lista de pacientes", layout, modal=True)
        while True:
            evento, valores = janela.read()

            if evento in (sg.WIN_CLOSED, "-FECHAR-"):
                janela.close()
                return None

            if permitir_selecao and evento == "-PACIENTES-":
                janela["-SELECIONAR-"].update(
                    visible=bool(valores["-PACIENTES-"])
                )
            elif (
                permitir_selecao
                and evento == "-SELECIONAR-"
                and valores["-PACIENTES-"]
            ):
                paciente = pacientes[linhas.index(valores["-PACIENTES-"][0])]
                janela.close()
                return paciente

    def mostra_mensagem(self, mensagem):
        sg.popup_ok(mensagem, title="Paciente")
