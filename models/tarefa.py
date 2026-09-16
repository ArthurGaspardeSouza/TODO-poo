"""
Módulo que define a classe Tarefa.

Representa uma tarefa individual da lista TODO, encapsulando seus
atributos e regras de negócio (ex.: validação de prioridade).
"""

from datetime import datetime


class Tarefa:
    """Representa uma única tarefa do sistema TODO."""

    PRIORIDADES_VALIDAS = ("baixa", "média", "alta")

    def __init__(self, id_tarefa, titulo, descricao="", prioridade="média",
                 concluida=False, data_criacao=None, data_conclusao=None):
        self._id = id_tarefa
        self._titulo = titulo
        self._descricao = descricao
        self.prioridade = prioridade  # usa o setter (validação)
        self._concluida = concluida
        self._data_criacao = data_criacao or datetime.now().strftime("%d/%m/%Y %H:%M")
        self._data_conclusao = data_conclusao

    # ---------- Propriedades (encapsulamento) ----------

    @property
    def id(self):
        return self._id

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, novo_titulo):
        if not novo_titulo or not novo_titulo.strip():
            raise ValueError("O título da tarefa não pode ser vazio.")
        self._titulo = novo_titulo.strip()

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, nova_descricao):
        self._descricao = nova_descricao.strip() if nova_descricao else ""

    @property
    def prioridade(self):
        return self._prioridade

    @prioridade.setter
    def prioridade(self, valor):
        valor = (valor or "média").strip().lower()
        if valor not in self.PRIORIDADES_VALIDAS:
            valor = "média"
        self._prioridade = valor

    @property
    def concluida(self):
        return self._concluida

    @property
    def data_criacao(self):
        return self._data_criacao

    @property
    def data_conclusao(self):
        return self._data_conclusao

    # ---------- Comportamentos (métodos) ----------

    def marcar_concluida(self):
        """Marca a tarefa como concluída e registra a data de conclusão."""
        self._concluida = True
        self._data_conclusao = datetime.now().strftime("%d/%m/%Y %H:%M")

    def desmarcar_concluida(self):
        """Reverte a tarefa para o estado pendente."""
        self._concluida = False
        self._data_conclusao = None

    def to_dict(self):
        """Converte a tarefa em um dicionário serializável (para JSON)."""
        return {
            "id": self._id,
            "titulo": self._titulo,
            "descricao": self._descricao,
            "prioridade": self._prioridade,
            "concluida": self._concluida,
            "data_criacao": self._data_criacao,
            "data_conclusao": self._data_conclusao,
        }

    @staticmethod
    def from_dict(dados):
        """Cria uma instância de Tarefa a partir de um dicionário."""
        return Tarefa(
            id_tarefa=dados["id"],
            titulo=dados["titulo"],
            descricao=dados.get("descricao", ""),
            prioridade=dados.get("prioridade", "média"),
            concluida=dados.get("concluida", False),
            data_criacao=dados.get("data_criacao"),
            data_conclusao=dados.get("data_conclusao"),
        )

    def __str__(self):
        status = "✔ Concluída" if self._concluida else "◻ Pendente"
        texto = f"[{self._id}] {self._titulo} | Prioridade: {self._prioridade} | {status}"
        if self._descricao:
            texto += f"\n     Descrição: {self._descricao}"
        texto += f"\n     Criada em: {self._data_criacao}"
        if self._concluida and self._data_conclusao:
            texto += f" | Concluída em: {self._data_conclusao}"
        return texto

    def __repr__(self):
        return f"Tarefa(id={self._id}, titulo={self._titulo!r}, concluida={self._concluida})"
