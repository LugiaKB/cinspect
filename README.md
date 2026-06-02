# CInspect

**CInspect** é uma ferramenta de análise acadêmica de código desenvolvida para o Centro de Informática da UFPE (CIn/UFPE). Seu objetivo é auxiliar monitores e professores na avaliação automatizada de submissões de código dos alunos, cobrindo desde detecção de plágio até feedback estruturado de qualidade.

---

## Módulos Planejados

| Módulo | Descrição |
|---|---|
| **Detecção de Plágio** | Compara submissões entre si e com repositórios externos para identificar similaridades suspeitas. |
| **Verificação de Restrições por Lista** | Valida se o código usa ou evita determinadas estruturas (ex.: proibir `while`, exigir recursão). |
| **Análise de Estrutura e Estilo** | Verifica conformidade com guias de estilo, complexidade ciclomática e organização do código. |
| **Feedback Automatizado** | Gera relatórios em linguagem natural com sugestões de melhoria para cada submissão. |

---

## Estrutura de Pastas

```
cinspect/
├── core/                  # Lógica de negócio e algoritmos de análise
│   ├── similarity/        # Detecção de plágio e similaridade
│   ├── services/          # Camada de serviços (orquestração)
│   └── tests/             # Testes automatizados do núcleo
├── api/                   # API HTTP com FastAPI
│   └── routers/           # Roteadores organizados por domínio
├── web/                   # Interface web (frontend)
├── Pipfile                # Dependências gerenciadas pelo Pipenv
├── Dockerfile             # Imagem Docker da aplicação
├── docker-compose.yml     # Orquestração dos serviços
└── README.md              # Este arquivo
```

---

## Setup e Execução

### Com Pipenv (desenvolvimento local)

```bash
# Instalar dependências (incluindo dev)
pipenv install --dev

# Ativar o ambiente virtual
pipenv shell

# Iniciar o servidor de desenvolvimento
uvicorn api.main:app --reload
```

### Com Docker

```bash
# Construir a imagem e subir os serviços
docker compose up --build

# A API ficará disponível em http://localhost:8000
# Documentação interativa: http://localhost:8000/docs
```

---

## Requisitos

- Python 3.12+
- Pipenv (para execução local)
- Docker e Docker Compose (para execução em contêiner)

---

## Contribuição

Este projeto segue as convenções:
- **Código**: escrito em inglês
- **Comentários e mensagens de interface**: em português
- **Commits**: seguem o padrão [Conventional Commits](https://www.conventionalcommits.org/)
