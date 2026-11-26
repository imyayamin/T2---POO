import FreeSimpleGUI as sg


class TelaClinica:
    def tela_opcoes(self):
        layout = [
            [sg.Text("Clínicas", font=("Segoe UI", 16, "bold"), justification="center", expand_x=True)],
            [sg.Button("Listar clínicas", size=(24, 2), key="-LISTAR-")],
            [sg.Button("Cadastrar clínica", size=(24, 2), key="-CADASTRAR-")],
            [sg.Button("Remover clínica", size=(24, 2), key="-REMOVER-")],
            [sg.Button("Voltar", size=(24, 2), key="-VOLTAR-")],
        ]

        janela = sg.Window("Clínicas", layout, element_justification="center", finalize=True)
        evento, _ = janela.read()
        janela.close()

        opcoes = {
            "-LISTAR-": 1,
            "-CADASTRAR-": 2,
            "-REMOVER-": 3,
            "-VOLTAR-": 0,
            sg.WIN_CLOSED: 0,
        }
        return opcoes.get(evento)

    def lista_clinicas(self, clinicas, permitir_selecao=False):
        linhas = [
            f"{indice} - {clinica.nome} | Cidade: {clinica.cidade} | "
            f"Horário: {clinica.horario_funcionamento_inicial}h às "
            f"{clinica.horario_funcionamento_final}h"
            for indice, clinica in enumerate(clinicas, start=1)
        ]

        layout = [
            [sg.Text("Clínicas cadastradas", font=("Segoe UI", 14, "bold"))],
            [
                sg.Listbox(
                    linhas,
                    size=(72, 12),
                    expand_x=True,
                    expand_y=True,
                    key="-CLINICAS-",
                    enable_events=permitir_selecao,
                )
            ],
            [
                sg.Button("Fechar", key="-FECHAR-"),
                sg.Button("Selecionar", key="-SELECIONAR-", visible=False),
            ],
        ]

        janela = sg.Window("Lista de clínicas", layout, modal=True)
        while True:
            evento, valores = janela.read()

            if evento in (sg.WIN_CLOSED, "-FECHAR-"):
                janela.close()
                return None

            if permitir_selecao and evento == "-CLINICAS-":
                janela["-SELECIONAR-"].update(
                    visible=bool(valores["-CLINICAS-"])
                )
            elif (
                permitir_selecao
                and evento == "-SELECIONAR-"
                and valores["-CLINICAS-"]
            ):
                clinica = clinicas[linhas.index(valores["-CLINICAS-"][0])]
                janela.close()
                return clinica

    def pega_dados_clinica(self):
        layout = [
            [sg.Text("Nome")],
            [sg.Input(key="-NOME-")],
            [sg.Text("Cidade")],
            [sg.Input(key="-CIDADE-")],
            [sg.Text("Descrição")],
            [sg.Input(key="-DESCRICAO-")],
            [sg.Text("Horário inicial (ex.: 8)")],
            [sg.Input(key="-HORARIO-INICIAL-")],
            [sg.Text("Horário final (ex.: 18)")],
            [sg.Input(key="-HORARIO-FINAL-")],
            [sg.Text("", key="-ERRO-", text_color="red")],
            [sg.Button("Cadastrar", key="-CADASTRAR-"), sg.Button("Cancelar", key="-CANCELAR-")],
        ]

        janela = sg.Window("Cadastrar clínica", layout, modal=True)
        while True:
            evento, valores = janela.read()
            if evento in (sg.WIN_CLOSED, "-CANCELAR-"):
                janela.close()
                return None
            if evento != "-CADASTRAR-":
                continue

            nome = valores["-NOME-"].strip()
            cidade = valores["-CIDADE-"].strip()
            descricao = valores["-DESCRICAO-"].strip()
            horario_inicial_texto = valores["-HORARIO-INICIAL-"].strip()
            horario_final_texto = valores["-HORARIO-FINAL-"].strip()

            if not nome or not cidade or not descricao:
                janela["-ERRO-"].update("Nome, cidade e descrição são obrigatórios.")
                continue

            try:
                horario_inicial = int(horario_inicial_texto)
                horario_final = int(horario_final_texto)
            except ValueError:
                janela["-ERRO-"].update("Os horários devem ser números inteiros.")
                continue

            janela.close()
            return {
                "nome": nome,
                "cidade": cidade,
                "descricao": descricao,
                "horario_inicial": horario_inicial,
                "horario_final": horario_final,
            }

    def mostra_mensagem(self, mensagem):
        sg.popup_ok(str(mensagem), title="Clínica")
