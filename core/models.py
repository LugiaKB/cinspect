# Modelos de dados base do CInspect.
# Define as estruturas centrais do domínio: turmas, alunos, listas de exercícios,
# questões, submissões de código, trechos suspeitos e resultados de verificação
# de plágio.
#
# Convenção de IDs:
#   - Entidades sincronizadas com o Dikastis recebem ULIDs externos como str
#     obrigatório (sem valor padrão).
#   - Entidades criadas internamente pelo CInspect têm IDs gerados com uuid4.
#
# Utiliza apenas a biblioteca padrão do Python (dataclasses, uuid, datetime).

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


# ---------------------------------------------------------------------------
# Funções auxiliares de validação (uso interno do módulo)
# ---------------------------------------------------------------------------

def _validate_required_string(value: str, field_name: str) -> None:
    """Verifica que uma string obrigatória não está vazia após remover espaços."""
    if not value or not value.strip():
        raise ValueError(f"O campo '{field_name}' não pode ser vazio.")


def _validate_score_range(value: float, field_name: str) -> None:
    """Verifica que um score de similaridade ou plágio está no intervalo [0.0, 1.0]."""
    if not (0.0 <= value <= 1.0):
        raise ValueError(
            f"O campo '{field_name}' deve estar entre 0.0 e 1.0, "
            f"mas recebeu {value}."
        )


def _validate_positive_integer(value: int, field_name: str) -> None:
    """Verifica que um número inteiro é estritamente positivo (maior que zero)."""
    if value <= 0:
        raise ValueError(
            f"O campo '{field_name}' deve ser maior que zero, "
            f"mas recebeu {value}."
        )


def _validate_non_negative_integer(value: int, field_name: str) -> None:
    """Verifica que um número inteiro não é negativo (maior ou igual a zero)."""
    if value < 0:
        raise ValueError(
            f"O campo '{field_name}' não pode ser negativo, "
            f"mas recebeu {value}."
        )


# ---------------------------------------------------------------------------
# Modelos de domínio
# ---------------------------------------------------------------------------

@dataclass
class StudentClass:
    """Representa uma turma de alunos identificada pelo semestre e pelo curso."""

    # ULID vindo do Dikastis — identificador externo da turma
    id: str

    # Semestre da turma (ex: "2025.1", "2025.2")
    semester: str

    # Nome do curso ao qual a turma pertence (ex: "Ciência da Computação")
    course: str

    def __post_init__(self) -> None:
        _validate_required_string(self.id, "id")
        _validate_required_string(self.semester, "semester")
        _validate_required_string(self.course, "course")


@dataclass
class Student:
    """Representa um aluno vinculado a uma turma."""

    # ULID vindo do Dikastis — identificador externo do aluno
    id: str

    # Nome completo do aluno
    full_name: str

    # Username do aluno no Dikastis
    dikastis_username: str

    # FK para StudentClass — turma à qual o aluno pertence
    class_id: str

    def __post_init__(self) -> None:
        _validate_required_string(self.id, "id")
        _validate_required_string(self.full_name, "full_name")
        _validate_required_string(self.dikastis_username, "dikastis_username")
        _validate_required_string(self.class_id, "class_id")


@dataclass
class AssignmentList:
    """Representa uma lista de exercícios aplicada em um semestre.

    As listas pertencem ao semestre, não à turma: todas as turmas de um mesmo
    semestre compartilham as mesmas listas de exercícios.
    """

    # ULID vindo do Dikastis — identificador externo da lista
    id: str

    # Número da lista dentro do semestre (1 a 6):
    #   1 = Condicionais
    #   2 = Loops
    #   3 = Listas
    #   4 = Funções
    #   5 = Recursão
    #   6 = Dicionários e Tuplas
    number: int

    # Semestre em que a lista foi aplicada (ex: "2025.1")
    semester: str

    def __post_init__(self) -> None:
        _validate_required_string(self.id, "id")
        _validate_required_string(self.semester, "semester")
        if not (1 <= self.number <= 6):
            raise ValueError(
                f"O campo 'number' deve estar entre 1 e 6, "
                f"mas recebeu {self.number}."
            )


@dataclass
class Question:
    """Representa uma questão individual pertencente a uma lista de exercícios."""

    # ULID vindo do Dikastis — identificador externo da questão
    id: str

    # FK para AssignmentList — lista à qual esta questão pertence
    assignment_list_id: str

    # Número da questão dentro da lista (ex: 1, 2, 3...)
    number: int

    # Título curto da questão (ex: "Sequência de Fibonacci")
    title: str

    # Enunciado completo da questão
    statement: str

    # Especificação do input esperado pelo programa
    input_spec: str

    # Especificação do output esperado pelo programa
    output_spec: str

    def __post_init__(self) -> None:
        _validate_required_string(self.id, "id")
        _validate_required_string(self.assignment_list_id, "assignment_list_id")
        _validate_positive_integer(self.number, "number")
        _validate_required_string(self.title, "title")
        _validate_required_string(self.statement, "statement")
        _validate_required_string(self.input_spec, "input_spec")
        _validate_required_string(self.output_spec, "output_spec")


@dataclass
class Submission:
    """Representa uma submissão de código feita por um aluno para uma questão específica."""

    # FK para Student — aluno que realizou a submissão
    student_id: str

    # FK para Question — questão à qual esta submissão responde
    question_id: str

    # Caminho do arquivo de código no disco ou no object storage
    storage_path: str

    # Identificador único autogerado pelo CInspect
    id: str = field(default_factory=lambda: str(uuid4()))

    # Timestamp da submissão gerado automaticamente no momento da criação
    submitted_at: datetime = field(default_factory=datetime.now)

    # Indica se a submissão foi aprovada nos testes automatizados
    approved: bool = False

    def __post_init__(self) -> None:
        _validate_required_string(self.student_id, "student_id")
        _validate_required_string(self.question_id, "question_id")
        _validate_required_string(self.storage_path, "storage_path")


@dataclass
class SimilarFragment:
    """Representa um trecho de código suspeito de ter sido copiado entre duas submissões."""

    # FK para PlagiarismResult — resultado ao qual este trecho pertence
    plagiarism_result_id: str

    # FK para Submission — submissão de origem (onde o trecho foi encontrado originalmente)
    source_submission_id: str

    # FK para Submission — submissão alvo (onde o trecho suspeito foi detectado)
    target_submission_id: str

    # Trecho exato extraído da submissão de origem
    source_fragment: str

    # Trecho correspondente encontrado na submissão alvo
    target_fragment: str

    # Score de similaridade entre os dois trechos (0.0 = diferente, 1.0 = idêntico)
    similarity_score: float

    # Linha inicial do trecho na submissão alvo
    start_line: int

    # Linha final do trecho na submissão alvo
    end_line: int

    # Identificador único autogerado pelo CInspect
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        _validate_required_string(self.plagiarism_result_id, "plagiarism_result_id")
        _validate_required_string(self.source_submission_id, "source_submission_id")
        _validate_required_string(self.target_submission_id, "target_submission_id")
        _validate_required_string(self.source_fragment, "source_fragment")
        _validate_required_string(self.target_fragment, "target_fragment")
        _validate_score_range(self.similarity_score, "similarity_score")
        _validate_positive_integer(self.start_line, "start_line")
        if self.end_line < self.start_line:
            raise ValueError(
                f"O campo 'end_line' ({self.end_line}) deve ser maior ou igual "
                f"a 'start_line' ({self.start_line})."
            )


@dataclass
class PlagiarismResult:
    """Representa o resultado completo de uma verificação de plágio para uma submissão."""

    # FK para Submission — submissão que foi verificada
    submission_id: str

    # Score geral de plágio calculado para a submissão (0.0 a 1.0)
    overall_score: float

    # Quantidade de submissões do corpus consultadas durante a verificação
    checked_against: int

    # Identificador único autogerado pelo CInspect
    id: str = field(default_factory=lambda: str(uuid4()))

    # Timestamp da verificação gerado automaticamente no momento da criação
    checked_at: datetime = field(default_factory=datetime.now)

    # Lista de trechos suspeitos encontrados durante a análise
    similar_fragments: list[SimilarFragment] = field(default_factory=list)

    def __post_init__(self) -> None:
        _validate_required_string(self.submission_id, "submission_id")
        _validate_score_range(self.overall_score, "overall_score")
        _validate_non_negative_integer(self.checked_against, "checked_against")
