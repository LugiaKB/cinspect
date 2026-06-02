# Modelos de dados base do CInspect.
# Define as estruturas centrais usadas em todo o sistema: listas de exercícios,
# questões, turmas, submissões de código, trechos similares detectados e
# resultados de verificação de plágio.
# Utiliza apenas a biblioteca padrão do Python (dataclasses, uuid, datetime).

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class AssignmentList:
    """Representa uma lista de exercícios de uma disciplina em um semestre."""

    # Nome ou título da lista (ex: "Lista 1", "Lista de Recursão")
    name: str

    # Semestre ao qual a lista pertence (ex: "2024.1", "2025.2")
    semester: str

    # Identificador único gerado automaticamente
    id: str = field(default_factory=lambda: str(uuid4()))

    # Timestamp de criação da lista no sistema
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Question:
    """Representa uma questão individual pertencente a uma lista de exercícios."""

    # ID da lista de exercícios à qual esta questão pertence
    assignment_list_id: str

    # Número da questão dentro da lista (ex: 1, 2, 3...)
    number: int

    # Título ou enunciado resumido da questão
    title: str

    # Identificador único gerado automaticamente
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class StudentClass:
    """Representa uma turma de alunos, identificada pelo semestre e pelo curso."""

    # Semestre da turma (ex: "2024.1", "2025.2")
    semester: str

    # Nome do curso ao qual a turma pertence (ex: "Ciência da Computação")
    course: str

    # Identificador único gerado automaticamente
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class Submission:
    """Representa uma submissão de código feita por um aluno para uma questão específica."""

    # Identificador do autor (ex: matrícula do aluno)
    author: str

    # Conteúdo do código submetido
    content: str

    # Nome do arquivo original enviado pelo aluno
    filename: str

    # ID da questão à qual esta submissão responde
    question_id: str

    # ID da turma do aluno que realizou a submissão
    class_id: str

    # Identificador único gerado automaticamente
    id: str = field(default_factory=lambda: str(uuid4()))

    # Timestamp da submissão gerado automaticamente no momento da criação
    submitted_at: datetime = field(default_factory=datetime.now)


@dataclass
class SimilarFragment:
    """Representa um trecho de código suspeito de ter sido copiado entre duas submissões."""

    # ID da submissão de origem (onde o trecho foi encontrado originalmente)
    source_submission_id: str

    # ID da submissão alvo (onde o trecho suspeito foi detectado)
    target_submission_id: str

    # Trecho exato extraído da submissão de origem
    source_fragment: str

    # Trecho correspondente encontrado na submissão alvo
    target_fragment: str

    # Score de similaridade entre os dois trechos (0.0 = diferente, 1.0 = idêntico)
    similarity_score: float

    # Linha inicial do trecho na submissão alvo
    start_line: int


@dataclass
class PlagiarismResult:
    """Representa o resultado completo de uma verificação de plágio para uma submissão."""

    # ID da submissão que foi verificada
    submission_id: str

    # Score geral de plágio calculado para a submissão (0.0 a 1.0)
    overall_score: float

    # Quantidade de submissões do mesmo corpus (mesma questão e turma) consultadas
    checked_against: int

    # Lista de trechos suspeitos encontrados durante a análise
    similar_fragments: list[SimilarFragment] = field(default_factory=list)

    # Timestamp da verificação gerado automaticamente no momento da criação
    checked_at: datetime = field(default_factory=datetime.now)
