"""
Sistema de Gerenciamento de Tarefas (TODO) - CLI
Trabalho Avaliativo de Programação Orientada a Objetos.

Autor: Arthur Gaspar de Souza

Este arquivo contém apenas a interface de linha de comando (CLI).
Toda a lógica de negócio fica em GerenciadorTarefas, e o modelo de
dados fica em Tarefa, seguindo o princípio de responsabilidade única.
"""

from gerenciador import GerenciadorTarefas


def exibir_menu():
    print("\n" + "=" * 40)
    print("   SISTEMA DE TAREFAS (TODO) - MENU")
    print("=" * 40)
    print("1. Adicionar nova tarefa")
    print("2. Listar todas as tarefas")
    print("3. Listar tarefas pendentes")
    print("4. Listar tarefas concluídas")
    print("5. Marcar tarefa como concluída")
    print("6. Remover tarefa")
    print("7. Buscar tarefa por título")
    print("8. Listar tarefas por prioridade")
    print("9. Ver estatísticas")
    print("0. Sair")
    print("=" * 40)


def ler_opcao_inteira(mensagem):
    """Lê um número inteiro do usuário, tratando entradas inválidas."""
    while True:
        valor = input(mensagem).strip()
        if valor.isdigit():
            return int(valor)
        print("⚠️  Digite apenas números, por favor.")


def imprimir_tarefas(tarefas):
    if not tarefas:
        print("\nNenhuma tarefa encontrada.")
        return
    print()
    for tarefa in tarefas:
        print("-" * 40)
        print(tarefa)
    print("-" * 40)


def adicionar_tarefa(gerenciador):
    print("\n--- Nova Tarefa ---")
    titulo = input("Título: ").strip()
    while not titulo:
        print("⚠️  O título não pode ser vazio.")
        titulo = input("Título: ").strip()

    descricao = input("Descrição (opcional): ").strip()

    print("Prioridade (baixa / média / alta) [padrão: média]: ", end="")
    prioridade = input().strip().lower() or "média"

    tarefa = gerenciador.adicionar_tarefa(titulo, descricao, prioridade)
    print(f"\n✅ Tarefa '{tarefa.titulo}' adicionada com sucesso (ID {tarefa.id}).")


def marcar_concluida(gerenciador):
    imprimir_tarefas(gerenciador.listar_tarefas("pendentes"))
    if not gerenciador.listar_tarefas("pendentes"):
        return
    id_tarefa = ler_opcao_inteira("\nDigite o ID da tarefa a concluir: ")
    if gerenciador.marcar_concluida(id_tarefa):
        print("✅ Tarefa marcada como concluída!")
    else:
        print("⚠️  Tarefa não encontrada.")


def remover_tarefa(gerenciador):
    imprimir_tarefas(gerenciador.listar_tarefas("todas"))
    if not gerenciador.listar_tarefas("todas"):
        return
    id_tarefa = ler_opcao_inteira("\nDigite o ID da tarefa a remover: ")
    confirmacao = input("Tem certeza? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Operação cancelada.")
        return
    if gerenciador.remover_tarefa(id_tarefa):
        print("🗑️  Tarefa removida com sucesso.")
    else:
        print("⚠️  Tarefa não encontrada.")


def buscar_tarefa(gerenciador):
    termo = input("\nDigite parte do título a buscar: ").strip()
    resultados = gerenciador.buscar_por_titulo(termo)
    imprimir_tarefas(resultados)


def exibir_estatisticas(gerenciador):
    stats = gerenciador.estatisticas()
    print("\n--- Estatísticas ---")
    print(f"Total de tarefas : {stats['total']}")
    print(f"Concluídas       : {stats['concluidas']}")
    print(f"Pendentes        : {stats['pendentes']}")


def main():
    gerenciador = GerenciadorTarefas("tarefas.json")

    print("Bem-vindo ao Sistema de Gerenciamento de Tarefas!")

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            adicionar_tarefa(gerenciador)
        elif opcao == "2":
            imprimir_tarefas(gerenciador.listar_tarefas("todas"))
        elif opcao == "3":
            imprimir_tarefas(gerenciador.listar_tarefas("pendentes"))
        elif opcao == "4":
            imprimir_tarefas(gerenciador.listar_tarefas("concluidas"))
        elif opcao == "5":
            marcar_concluida(gerenciador)
        elif opcao == "6":
            remover_tarefa(gerenciador)
        elif opcao == "7":
            buscar_tarefa(gerenciador)
        elif opcao == "8":
            imprimir_tarefas(gerenciador.ordenar_por_prioridade())
        elif opcao == "9":
            exibir_estatisticas(gerenciador)
        elif opcao == "0":
            print("\nAté logo! 👋")
            break
        else:
            print("⚠️  Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
