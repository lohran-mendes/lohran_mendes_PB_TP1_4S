import os
import subprocess
from datetime import datetime
from enum import Enum


class Status(Enum):
    A_FAZER = "a fazer"
    FAZENDO = "fazendo"
    CONCLUIDA = "concluída"


class Urgencia(Enum):
    PEQUENA = "pequena"
    NORMAL = "normal"
    ALTA = "alta"


class Tarefa:
    def __init__(
        self,
        descricao,
        urgencia: Urgencia = Urgencia.NORMAL,
        prazo_final="não informado",
    ):
        """Inicializa uma nova tarefa.

        Args:
            descricao: Texto descritivo da tarefa.
            urgencia: Nível de urgência da tarefa. Padrão: Urgencia.NORMAL.
            prazo_final: Data limite para conclusão ou 'não informado'. Padrão: 'não informado'.
        """
        self.descricao = descricao
        self.data_criacao = datetime.now()
        self.status: Status = Status.A_FAZER
        self.urgencia: Urgencia = urgencia
        self.prazo_final: datetime = prazo_final


lista_de_tarefas: list[Tarefa] = []


def _ler_urgencia() -> Urgencia | None:
    """Solicita ao usuário o nível de urgência da tarefa.

    Returns:
        O enum Urgencia correspondente à escolha do usuário,
        ou None em caso de entrada inválida.
    """
    try:
        escolha = int(
            input("Qual a urgência da tarefa? (1-pequena, 2-normal, 3-alta): ")
        )
    except ValueError:
        print("O valor inserido não é um número válido!")
        return None

    mapa_urgencia = {1: Urgencia.PEQUENA, 2: Urgencia.NORMAL, 3: Urgencia.ALTA}
    urgencia = mapa_urgencia.get(escolha)
    if urgencia is None:
        print("O valor inserido não é um número válido!")
    return urgencia


def _ler_prazo_final() -> datetime | str | None:
    """Solicita ao usuário se deseja definir um prazo final e, se sim, qual a data.

    Returns:
        Um objeto datetime com o prazo informado, a string 'não informado' caso
        o usuário opte por não definir prazo, ou None em caso de entrada inválida.
    """
    try:
        escolha = int(input("Deseja adicionar um prazo para a tarefa? (1-sim/2-nao): "))
    except ValueError:
        print("O valor inserido não é um número válido!")
        return None

    if escolha != 1:
        return "não informado"

    entrada = input("Digite a data como prazo final (DD/MM/AAAA HH:MM): ")
    try:
        return datetime.strptime(entrada, "%d/%m/%Y %H:%M")
    except ValueError:
        print("Data inválida! Use o formato DD/MM/AAAA HH:MM")
        return None


def adicionar_tarefa():
    """Coleta os dados necessários via input e adiciona uma nova tarefa à lista."""
    descricao = input("Digite a descrição da tarefa: ")
    if not descricao:
        print("A descrição não pode ser vazia!")
        return

    urgencia = _ler_urgencia()
    if urgencia is None:
        return

    prazo_final = _ler_prazo_final()
    if prazo_final is None:
        return

    tarefa = Tarefa(descricao, urgencia, prazo_final)
    lista_de_tarefas.append(tarefa)
    print("Tarefa adicionada com sucesso!")


def listar_tarefas():
    """Exibe todas as tarefas cadastradas com seus respectivos dados."""
    if not lista_de_tarefas:
        print("A lista de tarefas está vazia!")
        return
    print("\nListando as Tarefas: ")
    for tarefa in lista_de_tarefas:
        index = lista_de_tarefas.index(tarefa) + 1
        print(
            f"{index}. {tarefa.descricao} - status: {tarefa.status.value} - urgencia: {tarefa.urgencia.value} - prazo final: {tarefa.prazo_final} - data de criação: {tarefa.data_criacao}"
        )


def marcar_tarefa_como_concluida():
    """Lista as tarefas e marca a tarefa selecionada pelo usuário como concluída."""
    listar_tarefas()
    index = (
        int(input("\nInsira o identificador da tarefa a ser marcada como concluída: "))
        - 1
    )
    if 0 <= index < len(lista_de_tarefas):
        lista_de_tarefas[index].status = Status.CONCLUIDA
        print("Tarefa marcada como concluída com sucesso!")
        return
    else:
        print("A tarefa com o identificador enviado não existe")


def remover_tarefa():
    """Lista as tarefas e remove a tarefa selecionada pelo usuário da lista."""
    listar_tarefas()
    try:
        index = int(input("\nSelecione o identificador da tarefa a ser removida: ")) - 1
    except ValueError:
        print("opção inválida, tente novamente com um número!")
        return

    if index < len(lista_de_tarefas):
        lista_de_tarefas.pop(index)
        print("A tarefa foi removida com sucesso!")
    else:
        print(
            "Não existe nenhuma tarefa com esse identificador dentro da lista de tarefas"
        )


def exibir_menu():
    """Limpa o terminal e exibe as opções do menu principal."""
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
    print("\n- GERENCIADOR DE TAREFAS -")
    print("1. Listar tarefas")
    print("2. Criar tarefa")
    print("3. Marcar tarefa como concluída")
    print("4. Remover tarefa")
    print("5. Sair")


def gerenciador_de_tarefas():
    """Inicia e controla o loop principal do gerenciador de tarefas."""
    while True:
        exibir_menu()
        try:
            opcao_escolhida = int(input("\nEscolha uma opção: "))

            if opcao_escolhida == 1:
                listar_tarefas()
            elif opcao_escolhida == 2:
                adicionar_tarefa()
            elif opcao_escolhida == 3:
                marcar_tarefa_como_concluida()
            elif opcao_escolhida == 4:
                remover_tarefa()
            elif opcao_escolhida == 5:
                print("Saindo...\n")
                return
        except ValueError:
            print("opção inválida, tente novamente!")

        input("\nPressione enter para continuar... ")


gerenciador_de_tarefas()
