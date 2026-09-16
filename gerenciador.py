"""
Módulo que define a classe GerenciadorTarefas.

Responsável por manter a coleção de tarefas, aplicar as regras de
negócio (adicionar, listar, concluir, remover, ordenar) e persistir
os dados em um arquivo JSON entre execuções do programa.
"""

import json
import os

from models import Tarefa


class GerenciadorTarefas:
    """Gerencia o ciclo de vida das tarefas e a persistência em arquivo."""

    def __init__(self, arquivo="tarefas.json"):
        self._arquivo = arquivo
        self._tarefas = []
        self._proximo_id = 1
        self.carregar_tarefas()

    # ---------- Persistência ----------

    def carregar_tarefas(self):
        """Carrega as tarefas do arquivo JSON, se ele existir."""
        if not os.path.exists(self._arquivo):
            self._tarefas = []
            return

        try:
            with open(self._arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except (json.JSONDecodeError, OSError):
            self._tarefas = []
            return

        self._tarefas = [Tarefa.from_dict(item) for item in dados]
        if self._tarefas:
            self._proximo_id = max(t.id for t in self._tarefas) + 1

    def salvar_tarefas(self):
        """Persiste a lista atual de tarefas no arquivo JSON."""
        with open(self._arquivo, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self._tarefas], f,
                      ensure_ascii=False, indent=4)

    # ---------- Operações principais ----------

    def adicionar_tarefa(self, titulo, descricao="", prioridade="média"):
        """Cria e adiciona uma nova tarefa à lista, salvando em seguida."""
        nova_tarefa = Tarefa(
            id_tarefa=self._proximo_id,
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade,
        )
        self._tarefas.append(nova_tarefa)
        self._proximo_id += 1
        self.salvar_tarefas()
        return nova_tarefa

    def listar_tarefas(self, status="todas"):
        """
        Retorna as tarefas filtradas por status.
        status pode ser: 'todas', 'pendentes' ou 'concluidas'.
        """
        if status == "pendentes":
            return [t for t in self._tarefas if not t.concluida]
        if status == "concluidas":
            return [t for t in self._tarefas if t.concluida]
        return list(self._tarefas)

    def buscar_por_id(self, id_tarefa):
        """Retorna a tarefa com o id informado, ou None se não existir."""
        for tarefa in self._tarefas:
            if tarefa.id == id_tarefa:
                return tarefa
        return None

    def buscar_por_titulo(self, termo):
        """Retorna tarefas cujo título contenha o termo pesquisado."""
        termo = termo.lower().strip()
        return [t for t in self._tarefas if termo in t.titulo.lower()]

    def marcar_concluida(self, id_tarefa):
        """Marca a tarefa correspondente como concluída."""
        tarefa = self.buscar_por_id(id_tarefa)
        if tarefa is None:
            return False
        tarefa.marcar_concluida()
        self.salvar_tarefas()
        return True

    def remover_tarefa(self, id_tarefa):
        """Remove a tarefa da lista, se ela existir."""
        tarefa = self.buscar_por_id(id_tarefa)
        if tarefa is None:
            return False
        self._tarefas.remove(tarefa)
        self.salvar_tarefas()
        return True

    # ---------- Funcionalidades extras ----------

    def ordenar_por_prioridade(self):
        """Retorna as tarefas ordenadas de alta a baixa prioridade."""
        ordem = {"alta": 0, "média": 1, "baixa": 2}
        return sorted(self._tarefas, key=lambda t: ordem.get(t.prioridade, 1))

    def estatisticas(self):
        """Retorna um resumo numérico das tarefas cadastradas."""
        total = len(self._tarefas)
        concluidas = len([t for t in self._tarefas if t.concluida])
        pendentes = total - concluidas
        return {
            "total": total,
            "concluidas": concluidas,
            "pendentes": pendentes,
        }
