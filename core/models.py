# Modelos de dados base do CInspect.
# Define as estruturas centrais do domínio: turmas, alunos, listas de exercícios,
# questões, submissões de código, trechos similares detectados e resultados de
# verificação de plágio.
#
# Convenção de IDs:
#   - Entidades sincronizadas com o Dikastis usam ULIDs externos (str obrigatório).
#   - Entidades criadas pelo CInspect usam UUIDs gerados automaticamente.
#
# Utiliza apenas a biblioteca padrão do Python (dataclasses, uuid, datetime).

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class StudentClass:
    """Representa uma turma de alunos identificada pelo semestre e pelo curso."""

    # ULID vindo do Dikastis — identificador externo da turma
    id: str

    # Semestre da turma (ex: "2025.1", "2025.2")
    semester: str

    # Nome do curso ao qual a turma pertence (ex: "Ciência da Computação")
    course: str


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


@dataclass
class AssignmentList:
    """Representa uma lista de exercícios aplicada em um semestre.

    O semestre é a chave de ligação com StudentClass: todas as turmas de um mesmo
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


@dataclass
class Question:
    """Representa uma questão individual pertencente a uma lista de exercícios."""

    # ULID vindo do Dikastis — identificador externo da questão
    id: str

    # FK para AssignmentList — lista à qual esta questão pertence
    assignment_list_id: str

    # Enunciado completo da questão
    statement: str

    # Especificação do input esperado pelo programa
    input_spec: str

    # Especificação do output esperado pelo programa
    output_spec: str


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
