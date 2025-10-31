# 🎓 API de Gerenciamento Escolar - Flask MVC

Uma API RESTful completa para gerenciamento escolar desenvolvida com Flask, seguindo o padrão arquitetural MVC (Model-View-Controller). O sistema permite o gerenciamento de professores, turmas e alunos com documentação interativa via Swagger.

## 📋 Funcionalidades

- ✅ **CRUD Completo de Professores** - Criação, listagem, atualização e exclusão
- ✅ **CRUD Completo de Turmas** - Gerenciamento de turmas escolares
- ✅ **CRUD Completo de Alunos** - Gestão de alunos com notas e cálculo automático de média
- ✅ **Documentação Swagger** - Interface interativa para testar a API
- ✅ **Banco de Dados SQLite** - Persistência de dados local
- ✅ **Arquitetura MVC** - Código organizado e escalável
- ✅ **Relacionamentos** - Alunos vinculados a turmas, turmas a professores

## 🚀 Tecnologias Utilizadas

- **Flask 3.1.2** - Framework web Python
- **SQLAlchemy 2.0.43** - ORM para manipulação do banco de dados
- **Flask-SQLAlchemy 3.1.1** - Integração Flask + SQLAlchemy
- **Flasgger 0.9.7.1** - Documentação Swagger automática
- **SQLite** - Banco de dados embutido

## 📁 Estrutura do Projeto

```
AP1-Mvc-Flask/
├── 📂 config/
│   └── config.py                 # Configurações da aplicação
├── 📂 docs/
│   ├── Instruções.pdf            # Instruções do projeto acadêmico
│   └── swagger.yaml              # Documentação da API
├── 📂 src/
│   ├── 📂 api/
│   │   ├── 📂 aluno/
│   │   │   └── api_alunos.py     # Rotas dos alunos
│   │   ├── 📂 professores/
│   │   │   └── api_professores.py # Rotas dos professores
│   │   └── 📂 turma/
│   │       └── api_turma.py       # Rotas das turmas
│   ├── 📂 controllers/
│   │   ├── ctrls_aluno.py         # Controller dos alunos
│   │   ├── ctrls_professores.py   # Controller dos professores
│   │   └── ctrls_turma.py         # Controller das turmas
│   └── 📂 models/
│       ├── __init__.py            # Inicialização dos modelos
│       ├── models_aluno.py        # Modelo do aluno
│       ├── models_professor.py    # Modelo do professor
│       └── models_turma.py        # Modelo da turma
├── .dockerignore                  # Arquivos ignorados pelo Docker
├── Dockerfile                     # Configuração do container Docker
├── main.py                        # Arquivo principal da aplicação
├── requirements.txt               # Dependências do projeto
└── README.md                      # Documentação do projeto
```

## ⚡ Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 1. Clone o repositório
```bash
git clone https://github.com/Ryanditko/AP1-Mvc-Flask.git
cd AP1-Mvc-Flask
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Execute a aplicação
```bash
python main.py
```

A aplicação estará disponível em: `http://127.0.0.1:5000`

## 📖 Documentação da API

Após iniciar a aplicação, acesse a documentação interativa:
- **Swagger UI**: `http://127.0.0.1:5000/apidocs`

## 🔗 Endpoints Principais

### 👨‍🏫 Professores
- `GET /professores` - Lista todos os professores
- `POST /professores` - Cria um novo professor
- `PUT /professores/{id}` - Atualiza um professor
- `DELETE /professores/{id}` - Remove um professor

### 🏫 Turmas  
- `GET /turmas` - Lista todas as turmas
- `POST /turmas` - Cria uma nova turma
- `PUT /turmas/{id}` - Atualiza uma turma
- `DELETE /turmas/{id}` - Remove uma turma

### 👩‍🎓 Alunos
- `GET /alunos` - Lista todos os alunos
- `POST /alunos` - Cria um novo aluno
- `PUT /alunos/{id}` - Atualiza um aluno
- `DELETE /alunos/{id}` - Remove um aluno

## 📊 Exemplos de Uso

### Criando um Professor
```json
POST /professores
{
  "nome": "João Silva",
  "idade": 40,
  "materia": "Matemática",
  "observacoes": "Professor titular"
}
```

### Criando uma Turma
```json
POST /turmas
{
  "nome": "Turma 101",
  "professor_id": 1,
  "ativo": true
}
```

### Criando um Aluno
```json
POST /alunos
{
  "nome": "Maria Santos",
  "idade": 18,
  "turma_id": 1,
  "data_nascimento": "2006-10-07",
  "nota_primeiro_semestre": 8.5,
  "nota_segundo_semestre": 9.0
}
```

## 🗃️ Modelos de Dados

### Professor
- `id` - Identificador único
- `nome` - Nome completo
- `idade` - Idade
- `materia` - Matéria lecionada
- `observacoes` - Observações adicionais

### Turma
- `id` - Identificador único
- `nome` - Nome da turma
- `professor_id` - ID do professor responsável
- `ativo` - Status da turma

### Aluno
- `id` - Identificador único
- `nome` - Nome completo
- `idade` - Idade
- `turma_id` - ID da turma
- `data_nascimento` - Data de nascimento
- `nota_primeiro_semestre` - Nota do 1º semestre
- `nota_segundo_semestre` - Nota do 2º semestre
- `média_final` - Calculada automaticamente

## 🧪 Testando a API

### Exemplo com curl:
```bash
# Listar professores
curl -X GET http://127.0.0.1:5000/professores

# Criar um aluno
curl -X POST http://127.0.0.1:5000/alunos \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Pedro Oliveira",
    "idade": 17,
    "turma_id": 1,
    "data_nascimento": "2007-05-15",
    "nota_primeiro_semestre": 7.5,
    "nota_segundo_semestre": 8.0
  }'

# Buscar um aluno específico
curl -X GET http://127.0.0.1:5000/alunos/1
```

### Script de teste Python:
```python
import requests

# Teste básico
response = requests.get("http://127.0.0.1:5000/alunos")
print(f"Status: {response.status_code}")
print(f"Alunos: {response.json()}")
```

## 🛠️ Desenvolvimento

### Estrutura MVC
- **Model** (`src/models/`): Definição das entidades e relacionamentos
- **Controller** (`src/controllers/`): Lógica de negócio e manipulação de dados
- **Routes** (`src/api/`): Definição das rotas e endpoints

### Padrões Utilizados
- ✅ **Repository Pattern** - Separação da lógica de acesso a dados
- ✅ **Dependency Injection** - Injeção de dependências
- ✅ **RESTful API** - Padrões REST para endpoints
- ✅ **Error Handling** - Tratamento adequado de erros
- ✅ **Status Codes** - Códigos HTTP apropriados

## 📝 Configuração

O arquivo `config/config.py` contém as configurações principais:
- Banco de dados SQLite local
- Chave secreta para segurança
- Configurações do SQLAlchemy

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é desenvolvido para fins educacionais.

## 👥 Autor

Desenvolvido como projeto acadêmico - Sistema de Gerenciamento Escolar com Flask - por **Felipe Viana**, **Iago Rozales** e **Ryan Rodrigues**.

---

⭐ **Dê uma star se este projeto foi útil para você!**