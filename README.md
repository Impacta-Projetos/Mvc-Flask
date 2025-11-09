# 🎓 Sistema de Gerenciamento Escolar - Arquitetura de Microsserviços

Uma solução completa de microsserviços para gerenciamento escolar desenvolvida com Flask, seguindo o padrão arquitetural MVC (Model-View-Controller). O sistema é composto por três microsserviços independentes que se comunicam via HTTP REST API, permitindo escalabilidade e manutenção independente de cada serviço.

## 📋 Índice

- [Descrição da API](#-descrição-da-api)
- [Arquitetura de Microsserviços](#-arquitetura-de-microsserviços)
- [Integração entre Serviços](#-integração-entre-serviços)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Instruções de Execução com Docker](#-instruções-de-execução-com-docker)
- [Documentação da API](#-documentação-da-api)
- [Endpoints dos Microsserviços](#-endpoints-dos-microsserviços)

---

## 📖 Descrição da API

O sistema é dividido em **três microsserviços independentes**, cada um com sua própria base de dados e responsabilidades específicas:

### 1️⃣ **Microsserviço de Gerenciamento** (Porta 5000)
Responsável pelo gerenciamento das entidades principais do sistema escolar:
- **Professores**: CRUD completo para cadastro e gerenciamento de professores
- **Turmas**: CRUD completo para gestão de turmas escolares
- **Alunos**: CRUD completo para gestão de alunos

**Base de dados**: `gerenciamento.db` (SQLite)

### 2️⃣ **Microsserviço de Atividades** (Porta 5001)
Responsável pelo gerenciamento acadêmico:
- **Atividades**: CRUD de atividades escolares vinculadas a turmas e professores
- **Notas**: CRUD de notas dos alunos vinculadas às atividades

**Base de dados**: `atividades.db` (SQLite)

**Integrações**: Valida a existência de professores, turmas e alunos consultando o microsserviço de Gerenciamento via HTTP.

### 3️⃣ **Microsserviço de Reservas** (Porta 5002)
Responsável pelo gerenciamento de reservas:
- **Reservas**: CRUD de reservas de salas

**Base de dados**: `reservas.db` (SQLite)

---

## 🏗️ Arquitetura de Microsserviços

### Padrão Arquitetural

O projeto segue uma **arquitetura de microsserviços** com as seguintes características:

#### **1. Independência de Serviços**
- Cada microsserviço possui seu próprio código-fonte, banco de dados e dependências
- Podem ser desenvolvidos, testados e implantados independentemente
- Falhas em um serviço não afetam diretamente os outros

#### **2. Padrão MVC em Cada Microsserviço**
Todos os microsserviços seguem a arquitetura MVC:

```
Microsserviço/
├── models/           # Model: Entidades e acesso ao banco de dados
├── controllers/      # Controller: Lógica de negócio e validações
└── api/             # View: Rotas HTTP e interface REST
```

#### **3. Comunicação Síncrona HTTP**
- Os microsserviços se comunicam via **requisições HTTP REST**
- Utiliza a biblioteca `requests` do Python
- Comunicação através de DNS interno do Docker (nomes dos containers)

#### **4. Bancos de Dados Independentes**
Cada microsserviço possui sua própria base de dados SQLite:
- `gerenciamento.db`: Dados de professores, turmas e alunos
- `atividades.db`: Dados de atividades e notas
- `reservas.db`: Dados de reservas

#### **5. Containerização com Docker**
- Cada microsserviço roda em um container Docker isolado
- Orquestração via Docker Compose
- Rede privada `backend` para comunicação entre containers

### Diagrama da Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                         Cliente (Swagger UI)                     │
└────────┬─────────────────┬─────────────────┬────────────────────┘
         │                 │                 │
         │ :5000           │ :5001           │ :5002
         ▼                 ▼                 ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Gerenciamento  │ │   Atividades    │ │    Reservas     │
│  Microsserviço  │ │  Microsserviço  │ │  Microsserviço  │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ • Professores   │ │ • Atividades    │ │ • Reservas      │
│ • Turmas        │ │ • Notas         │ │                 │
│ • Alunos        │ │                 │ │                 │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ Flask + SQLite  │ │ Flask + SQLite  │ │ Flask + SQLite  │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         └───────────────────┴───────────────────┘
                    Rede Docker: backend
```

---

## 🔗 Integração entre Serviços

### Como os Microsserviços se Comunicam

#### **1. Validação de Dependências via HTTP**

O microsserviço de **Atividades** precisa validar se professores, turmas e alunos existem antes de criar atividades ou notas. Essa validação é feita através de **requisições HTTP** ao microsserviço de **Gerenciamento**.

**Exemplo: Criação de uma Atividade**

```python
# No controller de atividades (ctrls_atividades.py)

def validar_professor(professor_id):
    """Valida se o professor existe no microsserviço de Gerenciamento"""
    try:
        response = requests.get(f'http://gerenciamento:5000/professores/{professor_id}')
        if response.status_code == 200:
            return True, "Professor encontrado"
        else:
            return False, "Professor não encontrado"
    except requests.exceptions.RequestException as e:
        return False, f"Erro de conexão: {e}"

def validar_turma(turma_id):
    """Valida se a turma existe no microsserviço de Gerenciamento"""
    try:
        response = requests.get(f'http://gerenciamento:5000/turmas/{turma_id}')
        if response.status_code == 200:
            return True, "Turma encontrada"
        else:
            return False, "Turma não encontrada"
    except requests.exceptions.RequestException as e:
        return False, f"Erro de conexão: {e}"
```

#### **2. Fluxo de Criação de uma Atividade**

1. Cliente faz POST para `/atividades` no microsserviço de Atividades (porta 5001)
2. Controller de Atividades valida os dados recebidos
3. **Valida o professor**: Faz GET para `http://gerenciamento:5000/professores/{id}`
4. **Valida a turma**: Faz GET para `http://gerenciamento:5000/turmas/{id}`
5. Se ambas validações passarem, cria a atividade no banco `atividades.db`
6. Retorna resposta ao cliente

```
Cliente → POST /atividades (porta 5001)
           ↓
    Microsserviço Atividades
           ↓
    GET /professores/1 → Microsserviço Gerenciamento
           ↓
    GET /turmas/5 → Microsserviço Gerenciamento
           ↓
    Salva atividade.db
           ↓
    Retorna 201 Created
```

#### **3. Fluxo de Criação de uma Nota**

1. Cliente faz POST para `/notas` no microsserviço de Atividades
2. Controller de Notas valida os dados
3. **Valida o aluno**: Faz GET para `http://gerenciamento:5000/alunos/{id}`
4. **Valida a atividade**: Busca localmente no banco `atividades.db`
5. Cria a nota vinculada à atividade
6. Retorna resposta ao cliente

### **4. Fluxo de Criação de uma Reserva**

1. Cliente faz POST para `/reservas` no microsserviço de Gerenciamento
2. Controller de Reservas valida os dados
3. **Valida a turma**: Faz GET para `http://gerenciamento:5000/turmas/{id}`
4. Se a validação passar, cria a reserva no banco `reservas.db`
5. Retorna resposta ao cliente

#### **5. Resolução de Nomes via Docker DNS**

O Docker Compose cria uma rede privada `backend` onde os containers se comunicam usando seus nomes:

- `http://gerenciamento:5000` → Container do microsserviço de Gerenciamento
- `http://atividades:5001` → Container do microsserviço de Atividades
- `http://reservas:5002` → Container do microsserviço de Reservas

**Não é necessário usar IP**, pois o Docker resolve automaticamente o nome do container para o IP interno.

#### **6. Tratamento de Erros de Comunicação**

Os microsserviços implementam tratamento robusto de erros:

```python
try:
    response = requests.get(f'http://gerenciamento:5000/professores/{professor_id}')
    if response.status_code == 200:
        return True, "Professor encontrado"
    else:
        return False, f"Professor não encontrado. Status: {response.status_code}"
except requests.exceptions.RequestException as e:
    return False, f"Erro de conexão com Gerenciamento: {e}"
```

Se o microsserviço de Gerenciamento estiver **offline**, a criação da atividade falhará com uma mensagem clara de erro.

---

## 🚀 Tecnologias Utilizadas

### Backend
- **Flask 3.1.2** - Framework web Python minimalista e poderoso
- **SQLAlchemy 2.0.43** - ORM para manipulação do banco de dados
- **Flask-SQLAlchemy 3.1.1** - Integração Flask + SQLAlchemy
- **Flasgger 0.9.7.1** - Documentação Swagger/OpenAPI automática
- **Requests 2.31.0** - Cliente HTTP para comunicação entre microsserviços

### Banco de Dados
- **SQLite** - Banco de dados embutido, um para cada microsserviço

### Infraestrutura
- **Docker** - Containerização de aplicações
- **Docker Compose** - Orquestração de múltiplos containers
- **Python 3.9+** - Linguagem de programação

---

## 📁 Estrutura do Projeto

```
Mvc-Flask/
├── 📂 atividades/                    # Microsserviço de Atividades
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── 📂 config/
│   │   └── config.py
│   ├── 📂 docs/
│   │   └── swagger.yaml
│   └── 📂 src/
│       ├── 📂 api/
│       │   ├── 📂 atividades/
│       │   │   └── api_atividades.py      # Rotas de atividades
│       │   └── 📂 notas/
│       │       └── api_notas.py           # Rotas de notas
│       ├── 📂 controllers/
│       │   ├── ctrls_atividades.py        # Lógica de negócio (validações HTTP)
│       │   └── ctrls_notas.py
│       └── 📂 models/
│           ├── __init__.py
│           ├── models_atividades.py       # Modelo de dados
│           └── models_notas.py
│
├── 📂 gerenciamento/                 # Microsserviço de Gerenciamento
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── 📂 config/
│   │   └── config.py
│   ├── 📂 docs/
│   │   └── swagger.yaml
│   └── 📂 src/
│       ├── 📂 api/
│       │   ├── 📂 aluno/
│       │   │   └── api_alunos.py
│       │   ├── 📂 professores/
│       │   │   └── api_professores.py
│       │   └── 📂 turma/
│       │       └── api_turma.py
│       ├── 📂 controllers/
│       │   ├── ctrls_aluno.py
│       │   ├── ctrls_professores.py
│       │   └── ctrls_turma.py
│       └── 📂 models/
│           ├── __init__.py
│           ├── models_aluno.py
│           ├── models_professor.py
│           └── models_turma.py
│
├── 📂 reservas/                      # Microsserviço de Reservas
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── 📂 config/
│   │   └── config.py
│   ├── 📂 docs/
│   │   └── swagger.yaml
│   └── 📂 src/
│       ├── 📂 api/
│       │   └── api.py
│       ├── 📂 controllers/
│       │   └── controll.py
│       └── 📂 models/
│           └── models.py
│
├── docker-compose.yml                # Orquestração dos microsserviços
└── README.md                         # Este arquivo
```

---

## 🐳 Instruções de Execução com Docker

### Pré-requisitos

- **Docker**: [Instalar Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Instalar Docker Compose](https://docs.docker.com/compose/install/)

### 1. Clone o Repositório

```bash
git clone https://github.com/Impacta-Projetos/Mvc-Flask.git
cd Mvc-Flask
```

### 2. Inicie os Microsserviços com Docker Compose

Execute o comando abaixo na raiz do projeto:

```bash
docker-compose up --build
```

**O que acontece:**
- ✅ Cria 3 containers Docker (gerenciamento, atividades, reservas)
- ✅ Instala todas as dependências automaticamente
- ✅ Cria uma rede Docker privada `backend` para comunicação
- ✅ Inicializa os bancos de dados SQLite
- ✅ Expõe as portas 5000, 5001 e 5002

**Aguarde até ver as mensagens:**
```
gerenciamento  | * Running on http://0.0.0.0:5000
atividades     | * Running on http://0.0.0.0:5001
reservas       | * Running on http://0.0.0.0:5002
```

### 3. Acesse as Aplicações

- **Gerenciamento**: http://localhost:5000/apidocs
- **Atividades**: http://localhost:5001/apidocs
- **Reservas**: http://localhost:5002/apidocs

### 4. Testar a Comunicação entre Microsserviços

#### Passo 1: Criar um Professor no Gerenciamento
```bash
curl -X POST http://localhost:5000/professores \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Dr. João Silva",
    "idade": 45,
    "materia": "Matemática",
    "observacoes": "Professor titular"
  }'
```

**Resposta esperada:**
```json
{
  "mensagem": "Professor criado com sucesso."
}
```

#### Passo 2: Criar uma Turma no Gerenciamento
```bash
curl -X POST http://localhost:5000/turmas \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Turma 3A",
    "professor_id": 1,
    "ativo": true
  }'
```

#### Passo 3: Criar uma Atividade no microsserviço de Atividades

Esta requisição vai **validar automaticamente** se o professor e a turma existem fazendo requisições HTTP ao microsserviço de Gerenciamento:

```bash
curl -X POST http://localhost:5001/atividades \
  -H "Content-Type: application/json" \
  -d '{
    "descricao": "Prova de Cálculo 1",
    "data_entrega": "2025-12-15",
    "turma_id": 1,
    "professor_id": 1
  }'
```

**Se o professor ou turma não existirem, você receberá:**
```json
{
  "erro": "Professor não encontrado. Status: 404"
}
```

**Se ambos existirem:**
```json
{
  "mensagem": "Atividade criada com sucesso."
}
```

### 5. Parar os Microsserviços

```bash
docker-compose down
```

Para também remover os volumes (bancos de dados):
```bash
docker-compose down -v
```

### 6. Ver Logs dos Containers

Para debugar problemas de comunicação:

```bash
# Ver logs de todos os serviços
docker-compose logs

# Ver logs de um serviço específico
docker-compose logs atividades
docker-compose logs gerenciamento

# Ver logs em tempo real
docker-compose logs -f
```

---

## 📖 Documentação da API

Cada microsserviço possui sua documentação Swagger interativa:

### Swagger UI (Interface Interativa)
- **Gerenciamento**: http://localhost:5000/apidocs
- **Atividades**: http://localhost:5001/apidocs
- **Reservas**: http://localhost:5002/apidocs

---

## 🔗 Endpoints dos Microsserviços

### 🏫 Microsserviço de Gerenciamento (Porta 5000)

#### Professores
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/professores` | Lista todos os professores |
| GET | `/professores/{id}` | Busca um professor específico |
| POST | `/professores` | Cria um novo professor |
| PUT | `/professores/{id}` | Atualiza um professor |
| DELETE | `/professores/{id}` | Remove um professor |

**Exemplo de Criação:**
```json
POST /professores
{
  "nome": "Dr. João Silva",
  "idade": 45,
  "materia": "Matemática",
  "observacoes": "Professor titular"
}
```

#### Turmas
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/turmas` | Lista todas as turmas |
| GET | `/turmas/{id}` | Busca uma turma específica |
| POST | `/turmas` | Cria uma nova turma |
| PUT | `/turmas/{id}` | Atualiza uma turma |
| DELETE | `/turmas/{id}` | Remove uma turma |

**Exemplo de Criação:**
```json
POST /turmas
{
  "descricao": "Turma 3A",
  "professor_id": 1,
  "ativo": true
}
```

#### Alunos
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/alunos` | Lista todos os alunos |
| GET | `/alunos/{id}` | Busca um aluno específico |
| POST | `/alunos` | Cria um novo aluno |
| PUT | `/alunos/{id}` | Atualiza um aluno |
| DELETE | `/alunos/{id}` | Remove um aluno |

**Exemplo de Criação:**
```json
POST /alunos
{
  "nome": "Maria Santos",
  "idade": 16,
  "turma_id": 1,
  "data_nascimento": "2008-05-15"
}
```

### 📚 Microsserviço de Atividades (Porta 5001)

#### Atividades
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/atividades` | Lista todas as atividades |
| GET | `/atividades/{id}` | Busca uma atividade específica |
| POST | `/atividades` | Cria uma nova atividade (valida professor e turma) |
| PUT | `/atividades/{id}` | Atualiza uma atividade |
| DELETE | `/atividades/{id}` | Remove uma atividade |

**Exemplo de Criação (com validação HTTP):**
```json
POST /atividades
{
  "nome_atividade": "Prova de Cálculo",
  "descricao": "Prova de Cálculo 1",
  "peso_porcento": 30,
  "data_entrega": "2025-12-15",
  "turma_id": 1,
  "professor_id": 1
}
```

**Validações realizadas automaticamente:**
- ✅ Consulta `GET http://gerenciamento:5000/professores/1`
- ✅ Consulta `GET http://gerenciamento:5000/turmas/1`
- ✅ Só cria a atividade se ambos existirem

#### Notas
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/notas` | Lista todas as notas |
| GET | `/notas/{id}` | Busca uma nota específica |
| POST | `/notas` | Cria uma nova nota (valida aluno) |
| PUT | `/notas/{id}` | Atualiza uma nota |
| DELETE | `/notas/{id}` | Remove uma nota |

**Exemplo de Criação (com validação HTTP):**
```json
POST /notas
{
  "nota": 9.5,
  "aluno_id": 1,
  "atividade_id": 1
}
```

**Validação realizada automaticamente:**
- ✅ Consulta `GET http://gerenciamento:5000/alunos/1`

### 🏢 Microsserviço de Reservas (Porta 5002)

#### Reservas
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/reservas` | Lista todas as reservas |
| GET | `/reservas/{id}` | Busca uma reserva específica |
| POST | `/reservas` | Cria uma nova reserva |
| PUT | `/reservas/{id}` | Atualiza uma reserva |
| DELETE | `/reservas/{id}` | Remove uma reserva |

**Exemplo de Criação (com validação HTTP):**
```json
POST /reservas
{
  "num_sala": 205,
  "lab": true,
  "data": "2025-12-15",
  "turma_id": 1
}
```

**Validações realizadas automaticamente:**
- ✅ Consulta `GET http://gerenciamento:5000/turmas/1`
- ✅ Só cria a reserva se a turma existir

---

## 🧪 Testando a Integração entre Microsserviços

### Cenário 1: Teste de Validação Bem-Sucedida

```bash
# 1. Criar um professor
curl -X POST http://localhost:5000/professores \
  -H "Content-Type: application/json" \
  -d '{"nome": "Prof. Ana", "idade": 40, "materia": "História", "observacoes": ""}'

# 2. Criar uma turma
curl -X POST http://localhost:5000/turmas \
  -H "Content-Type: application/json" \
  -d '{"nome": "Turma 2B", "professor_id": 1, "ativo": true}'

# 3. Criar uma atividade (valida professor e turma via HTTP)
curl -X POST http://localhost:5001/atividades \
  -H "Content-Type: application/json" \
  -d '{"descricao": "Trabalho de História", "data_entrega": "2025-11-30", "turma_id": 1, "professor_id": 1}'

# ✅ Resposta: {"mensagem": "Atividade criada com sucesso."}
```

### Cenário 2: Teste de Validação com Falha

```bash
# Tentar criar atividade com professor inexistente
curl -X POST http://localhost:5001/atividades \
  -H "Content-Type: application/json" \
  -d '{"descricao": "Atividade Teste", "data_entrega": "2025-12-01", "turma_id": 1, "professor_id": 999}'

# ❌ Resposta: {"erro": "Professor não encontrado. Status: 404"}
```

### Cenário 3: Teste com Serviço Offline

```bash
# Parar o microsserviço de gerenciamento
docker-compose stop gerenciamento

# Tentar criar atividade
curl -X POST http://localhost:5001/atividades \
  -H "Content-Type: application/json" \
  -d '{"descricao": "Teste", "data_entrega": "2025-12-01", "turma_id": 1, "professor_id": 1}'

# ❌ Resposta: {"erro": "Erro de conexão com Gerenciamento: ..."}
```

---

## 🛠️ Desenvolvimento Local (Sem Docker)

Se preferir executar sem Docker para desenvolvimento:

### 1. Instalar dependências de cada microsserviço

```bash
# Gerenciamento
cd gerenciamento
pip install -r requirements.txt
python main.py

# Atividades (em outro terminal)
cd atividades
pip install -r requirements.txt
python main.py

# Reservas (em outro terminal)
cd reservas
pip install -r requirements.txt
python main.py
```

### 2. Ajustar URLs de comunicação

Quando executar localmente sem Docker, edite os controllers para usar `localhost` ao invés dos nomes dos containers:

```python
# Em ctrls_atividades.py
response = requests.get(f'http://localhost:5000/professores/{professor_id}')
```

---

## 🗃️ Modelos de Dados

### Gerenciamento

**Professor**
```python
{
  "id": 1,
  "nome": "Dr. João Silva",
  "idade": 45,
  "materia": "Matemática",
  "observacoes": "Professor titular"
}
```

**Turma**
```python
{
  "id": 1,
  "descricao": "Turma 3A",
  "professor_id": 1,
  "ativo": true
}
```

**Aluno**
```python
{
  "id": 1,
  "nome": "Maria Santos",
  "idade": 16,
  "turma_id": 1,
  "data_nascimento": "2008-05-15"
}
```

### Atividades

**Atividade**
```python
{
  "id": 1,
  "descricao": "Prova de Cálculo 1",
  "data_entrega": "2025-12-15",
  "turma_id": 1,        # Referência ao microsserviço de Gerenciamento
  "professor_id": 1     # Referência ao microsserviço de Gerenciamento
}
```

**Nota**
```python
{
  "id": 1,
  "nota": 9.5,
  "aluno_id": 1,       # Referência ao microsserviço de Gerenciamento
  "atividade_id": 1
}
```

### Reservas

**Reserva**
```python
{
  "id": 1,
  "num_sala": "203",
  "lab": true,
  "data_reserva": "2025-11-15",
  "turma_id": 1        # Referência ao microsserviço de Gerenciamento
}
```

---

## 🔍 Troubleshooting

### Problema: "Erro de conexão com Gerenciamento"

**Causa**: O microsserviço de Gerenciamento não está acessível.

**Solução**:
```bash
# Verificar se todos os containers estão rodando
docker-compose ps

# Ver logs do serviço
docker-compose logs gerenciamento

# Reiniciar os serviços
docker-compose restart
```

### Problema: "Professor não encontrado. Status: 404"

**Causa**: O professor_id fornecido não existe no banco de dados do microsserviço de Gerenciamento.

**Solução**:
1. Listar professores: `curl http://localhost:5000/professores`
2. Criar o professor se necessário
3. Usar um ID válido ao criar a atividade

### Problema: Containers não se comunicam

**Causa**: Containers não estão na mesma rede Docker ou foram iniciados individualmente.

**Solução**:
```bash
# Sempre usar docker-compose
docker-compose down
docker-compose up --build
```

---

## 📊 Padrões e Boas Práticas Implementadas

✅ **Arquitetura de Microsserviços**: Serviços independentes e desacoplados  
✅ **Padrão MVC**: Separação clara de responsabilidades  
✅ **RESTful API**: Endpoints seguindo convenções REST  
✅ **Validação Cross-Service**: Validações via HTTP entre microsserviços  
✅ **Tratamento de Erros**: Respostas apropriadas para cada cenário  
✅ **Documentação Swagger**: Documentação interativa automática  
✅ **Containerização**: Deploy consistente com Docker  
✅ **Bancos Independentes**: Cada microsserviço com seu próprio banco  
✅ **Códigos de Status HTTP**: Uso correto de status codes (200, 201, 404, 400, etc.)

---

## � Configuração do Docker

### docker-compose.yml
```yaml
version: '3.8'

services:
  atividades:
    build: ./atividades
    ports:
      - "5001:5001"
    volumes:
      - ./atividades:/app
    networks:
      - backend
    container_name: atividades

  gerenciamento:
    build: ./gerenciamento
    ports:
      - "5000:5000"
    volumes:
      - ./gerenciamento:/app
    networks:
      - backend
    container_name: gerenciamento

  reservas:
    build: ./reservas
    ports:
      - "5002:5002"
    volumes:
      - ./reservas:/app
    networks:
      - backend
    container_name: reservas

networks:
  backend:
    driver: bridge
```

### Dockerfile (Exemplo)
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

---

## 👥 Autores

Desenvolvido como projeto acadêmico para a disciplina de Desenvolvimento de APIs.

**Equipe:**
- Felipe Viana
- Iago Rozales
- Ryan Rodrigues

**Instituição**: Faculdade Impacta  
**Curso**: Análise e Desenvolvimento de Sistemas  
**Ano**: 2025

---

## 📚 Referências

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Docker Documentation](https://docs.docker.com/)
- [RESTful API Design](https://restfulapi.net/)
- [Microservices Architecture](https://microservices.io/)

---

⭐ **Se este projeto foi útil para você, deixe uma star no repositório!**