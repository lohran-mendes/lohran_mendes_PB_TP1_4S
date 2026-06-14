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
        self.descricao = descricao
        self.data_criacao = datetime.now()
        self.status: Status = Status.A_FAZER
        self.urgencia: Urgencia = urgencia
        self.prazo_final: datetime = prazo_final


lista_de_tarefas: list[Tarefa] = []


def adicionar_tarefa():
    descricao = input("Digite a descrição da tarefa: ")
    if not descricao:
        print("A descrição não pode ser vazia!")
        return

    try:
        urgencia_input = int(
            input("Qual a urgência da tarefa? (1-pequena, 2-normal, 3-alta): ")
        )
        if urgencia_input == 1:
            urgencia = Urgencia.PEQUENA
        elif urgencia_input == 2:
            urgencia = Urgencia.NORMAL
        elif urgencia_input == 3:
            urgencia = Urgencia.ALTA
        else:
            print("O valor inserido não é um número válido!")
            return
    except ValueError:
        print("O valor inserido não é um número válido!")
        return

    try:
        tem_prazo_final = int(
            input("Deseja adicionar um prazo para a tarefa? (1-sim/2-nao): ")
        )
        if tem_prazo_final == 1:
            entrada = input("Digite a data como prazo final (DD/MM/AAAA HH:MM): ")
            try:
                prazo_final = datetime.strptime(entrada, "%d/%m/%Y %H:%M")
            except ValueError:
                print("Data inválida! Use o formato DD/MM/AAAA HH:MM")
                return
            tarefa = Tarefa(descricao, urgencia, prazo_final)
            lista_de_tarefas.append(tarefa)
            print("Tarefa adicionada com sucesso!")
            return
    except ValueError:
        print("O valor inserido não é um número válido!")

    tarefa = Tarefa(descricao, urgencia)
    lista_de_tarefas.append(tarefa)
    print("Tarefa adicionada com sucesso!")


def listar_tarefas():
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
        print("Não existe nenhuma tarefa com esse identificador dentro da lista de tarefas")


def exibir_menu():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
    print("\n- GERENCIADOR DE TAREFAS -")
    print("1. Listar tarefas")
    print("2. Criar tarefa")
    print("3. Marcar tarefa como concluída")
    print("4. Remover tarefa")
    print("5. Sair")


def gerenciador_de_tarefas():
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
