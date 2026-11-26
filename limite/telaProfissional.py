import FreeSimpleGUI as sg


class TelaProfissional:
    def tela_opcoes(self):
        layout = [
            [sg.Text("Profissionais", font=("Segoe UI", 16, "bold"), justification="center", expand_x=True)],
            [sg.Button("Listar profissionais", size=(24, 2), key="-LISTAR-")],
            [sg.Button("Cadastrar profissional", size=(24, 2), key="-CADASTRAR-")],
            [sg.Button("Editar profissional", size=(24, 2), key="-EDITAR-")],
            [sg.Button("Remover profissional", size=(24, 2), key="-REMOVER-")],
            [sg.Button("Voltar", size=(24, 2), key="-VOLTAR-")],
        ]

        janela = sg.Window("Profissionais", layout, element_justification="center", finalize=True)
        evento, _ = janela.read()
        janela.close()

        opcoes = {
            "-LISTAR-": 1,
            "-CADASTRAR-": 2,
            "-EDITAR-": 3,
            "-REMOVER-": 4,
            "-VOLTAR-": 0,
            sg.WIN_CLOSED: 0,
        }
        return opcoes.get(evento)


    def lista_profissionais(self, profissionais, permitir_selecao=False):
        linhas = [
            f"{indice} - {profissional.nome} - CPF: {profissional.cpf} - "
            f"Especialidade: {profissional.especialidade} - "
            f"Registro: {profissional.registro_profissional}"
            for indice, profissional in enumerate(profissionais, start=1)
        ]
        layout = [
            [sg.Text("Profissionais cadastrados", font=("Segoe UI", 14, "bold"))],
            [
                sg.Listbox(
                    linhas,
                    size=(72, 12),
                    expand_x=True,
                    expand_y=True,
                    key="-PROFISSIONAIS-",
                    enable_events=permitir_selecao,
                )
            ],
            [
                sg.Button("Fechar", key="-FECHAR-"),
                sg.Button("Selecionar", key="-SELECIONAR-", visible=False),
            ],
        ]

        janela = sg.Window("Lista de profissionais", layout, modal=True)
        while True:
            evento, valores = janela.read()
            if evento in (sg.WIN_CLOSED, "-FECHAR-"):
                janela.close()
                return None

            if permitir_selecao and evento == "-PROFISSIONAIS-":
                janela["-SELECIONAR-"].update(
                    visible=bool(valores["-PROFISSIONAIS-"])
                )
            elif (
                permitir_selecao
                and evento == "-SELECIONAR-"
                and valores["-PROFISSIONAIS-"]
            ):
                profissional = profissionais[
                    linhas.index(valores["-PROFISSIONAIS-"][0])
                ]
                janela.close()
                return profissional

   
    def pega_dados_profissional(self):
        layout = [
            [sg.Text("Nome")],
            [sg.Input(key="-NOME-")],
            [sg.Text("Celular")],
            [sg.Input(key="-CELULAR-")],
            [sg.Text("CPF")],
            [sg.Input(key="-CPF-")],
            [sg.Text("Especialidade")],
            [sg.Input(key="-ESPECIALIDADE-")],
            [sg.Text("Registro profissional")],
            [sg.Input(key="-REGISTRO-")],
            [sg.Text("", key="-ERRO-", text_color="red")],
            [sg.Button("Salvar", key="-SALVAR-"), sg.Button("Cancelar", key="-CANCELAR-")],
        ]

        janela = sg.Window("Cadastrar/editar profissional", layout, modal=True)
        while True:
            evento, valores = janela.read()
            if evento in (sg.WIN_CLOSED, "-CANCELAR-"):
                janela.close()
                return None
            if evento != "-SALVAR-":
                continue

            nome = valores["-NOME-"].strip()
            celular_texto = valores["-CELULAR-"].strip()
            cpf_texto = valores["-CPF-"].strip()
            especialidade = valores["-ESPECIALIDADE-"].strip()
            registro_texto = valores["-REGISTRO-"].strip()

            if not nome:
                janela["-ERRO-"].update("O nome não pode estar vazio.")
                continue
            if not especialidade:
                janela["-ERRO-"].update("A especialidade não pode estar vazia.")
                continue

            try:
                celular = int(celular_texto)
                cpf = int(cpf_texto)
                registro_profissional = int(registro_texto)
            except ValueError:
                janela["-ERRO-"].update("Celular, CPF e registro devem conter apenas números.")
                continue

            janela.close()
            return {
                "nome": nome,
                "celular": celular,
                "cpf": cpf,
                "especialidade": especialidade,
                "registro_profissional": registro_profissional,
            }


    def seleciona_profissional(self, profissional):
        layout = [
            [sg.Text(f"Confirme o CPF de {profissional.nome} para removê-lo")],
            [sg.Input(key="-CPF-")],
            [sg.Text("", key="-ERRO-", text_color="red")],
            [sg.Button("Remover", key="-REMOVER-"), sg.Button("Cancelar", key="-CANCELAR-")],
        ]

        janela = sg.Window("Remover profissional", layout, modal=True)
        while True:
            evento, valores = janela.read()
            if evento in (sg.WIN_CLOSED, "-CANCELAR-"):
                janela.close()
                return None
            if evento != "-REMOVER-":
                continue

            try:
                cpf = int(valores["-CPF-"].strip())
            except (TypeError, ValueError):
                janela["-ERRO-"].update("CPF inválido. Digite apenas números.")
                continue

            janela.close()
            return cpf


    def mostra_mensagem(self, mensagem):
        sg.popup_ok(str(mensagem), title="Profissional")
