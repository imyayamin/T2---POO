import FreeSimpleGUI as sg


class TelaRelatorio:
    def tela_opcoes(self):
        layout = [
            [sg.Text("Relatórios", font=("Segoe UI", 16, "bold"), justification="center", expand_x=True)],
            [sg.Button("Clínicas com mais atendimentos", size=(32, 2), key="-CLINICAS-")],
            [sg.Button("Atendimentos mais caros e mais baratos", size=(32, 2), key="-ATENDIMENTOS-")],
            [sg.Button("Procedimentos mais realizados", size=(32, 2), key="-POPULARES-")],
            [sg.Button("Procedimentos mais caros e mais baratos", size=(32, 2), key="-VALORES-")],
            [sg.Button("Voltar", size=(32, 2), key="-VOLTAR-")],
        ]

        janela = sg.Window("Relatórios", layout, element_justification="center")
        evento, _ = janela.read()
        janela.close()

        opcoes = {
            "-CLINICAS-": 1,
            "-ATENDIMENTOS-": 2,
            "-POPULARES-": 3,
            "-VALORES-": 4,
            "-VOLTAR-": 0,
            sg.WIN_CLOSED: 0,
        }
        return opcoes.get(evento)

    def mostra_clinicas_com_mais_atendimentos(self, resultado):
        linhas = ["Clínicas com maior número de atendimentos:"]
        linhas.extend(
            f"- {clinica.nome}: {quantidade} atendimento(s)"
            for clinica, quantidade in resultado
        )
        self.__mostra_relatorio("Clínicas com mais atendimentos", linhas)

    def mostra_atendimentos_extremos(self, mais_caros, mais_baratos):
        linhas = ["Atendimento(s) mais caro(s):"]
        linhas.extend(
            self.__detalhes_atendimento(atendimento, valor)
            for atendimento, valor in mais_caros
        )
        linhas.append("")
        linhas.append("Atendimento(s) mais barato(s):")
        linhas.extend(
            self.__detalhes_atendimento(atendimento, valor)
            for atendimento, valor in mais_baratos
        )
        self.__mostra_relatorio("Atendimentos mais caros e mais baratos", linhas)

    def __detalhes_atendimento(self, atendimento, valor):
        return (
            f"- {atendimento.data.isoformat()} às "
            f"{atendimento.horario_inicio.strftime('%H:%M')} | "
            f"Paciente: {atendimento.paciente.nome} | "
            f"Clínica: {atendimento.clinica.nome} | "
            f"Total: R$ {valor:.2f}"
        )

    def mostra_procedimentos_populares(self, populares):
        linhas = ["Procedimento(s) mais realizado(s):"]
        for ocorrencias in populares:
            procedimento = ocorrencias[0][0]
            linhas.append(
                f"- {procedimento.descricao}: "
                f"{len(ocorrencias)} realização(ões)"
            )
        self.__mostra_relatorio("Procedimentos mais realizados", linhas)

    def mostra_procedimentos_extremos(self, mais_caros, mais_baratos):
        linhas = ["Procedimento(s) mais caro(s):"]
        linhas.extend(
            self.__detalhes_procedimento(procedimento, atendimento)
            for procedimento, atendimento in mais_caros
        )
        linhas.append("")
        linhas.append("Procedimento(s) mais barato(s):")
        linhas.extend(
            self.__detalhes_procedimento(procedimento, atendimento)
            for procedimento, atendimento in mais_baratos
        )
        self.__mostra_relatorio("Procedimentos mais caros e mais baratos", linhas)

    def __detalhes_procedimento(self, procedimento, atendimento):
        return (
            f"- {procedimento.descricao}: R$ {procedimento.custo:.2f} | "
            f"Paciente: {atendimento.paciente.nome} | "
            f"Data: {atendimento.data.isoformat()}"
        )

    def mostra_mensagem(self, mensagem):
        sg.popup_ok(str(mensagem), title="Relatórios")

    def __mostra_relatorio(self, titulo, linhas):
        layout = [
            [sg.Multiline("\n".join(linhas), size=(80, 18), disabled=True, expand_x=True, expand_y=True)],
            [sg.Button("Fechar", key="-FECHAR-")],
        ]
        janela = sg.Window(titulo, layout, modal=True, resizable=True)
        janela.read()
        janela.close()
