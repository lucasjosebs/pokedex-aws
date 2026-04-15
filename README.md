# Pokédex AWS 🎮

Projeto de uma Pokédex completa integrada com serviços AWS, banco de dados MySQL e desenvolvimento web com Python Flask.

## Sobre o Projeto

Aplicação web que permite buscar pokémons por nome, tipo ou número da Pokédex, exibindo seus dados e imagens em cards interativos. Os dados são armazenados em um banco de dados MySQL na nuvem e as imagens em um bucket S3.

## Arquitetura AWS

Usuário → EC2 (Flask) → RDS MySQL (dados)
→ S3 (imagens)

### Serviços utilizados

- **EC2** — Servidor web rodando a aplicação Flask
- **RDS** — Banco de dados MySQL com os dados dos pokémons
- **S3** — Armazenamento das imagens dos pokémons
- **Security Groups** — Controle de acesso entre os serviços

## Tecnologias

- **Python 3** + **Flask** — Backend e API REST
- **PyMySQL** — Conexão com o banco de dados
- **Boto3** — SDK AWS para Python
- **HTML + CSS + JavaScript** — Frontend
- **MySQL** — Banco de dados relacional
- **PokeAPI** — Fonte dos dados dos pokémons

## Funcionalidades

- Listagem de todos os pokémons cadastrados
- Busca por nome, tipo ou número da Pokédex
- Cards com imagem, número, nome e tipos coloridos
- API REST com retorno em JSON
- Servidor rodando permanentemente com systemd

## Estrutura do Projeto

pokedex/
├── app.py # Servidor Flask + rotas da API
├── popular_banco.py # Script para popular o banco via PokeAPI
├── upload_imagens_s3.py # Script para upload das imagens no S3
├── templates/
│ └── index.html # Frontend da Pokédex
├── .gitignore
└── README.md

## Como Executar

### Pré-requisitos

- Conta AWS com EC2, RDS e S3 configurados
- Python 3 instalado
- Ambiente virtual Python

### Configuração do ambiente

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/pokedex-aws.git
cd pokedex-aws

# Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install flask pymysql boto3 requests
```

### Configuração do banco de dados

No MySQL, execute:

```sql
CREATE DATABASE pokedex;

USE pokedex;

CREATE TABLE pokemon (
    id          INT PRIMARY KEY AUTO_INCREMENT,
    numero      INT UNIQUE NOT NULL,
    nome        VARCHAR(100) NOT NULL,
    tipo1       VARCHAR(50) NOT NULL,
    tipo2       VARCHAR(50),
    url_imagem  TEXT NOT NULL,
    descricao   TEXT
);
```

### Variáveis de configuração

No arquivo `app.py`, configure as variáveis com seus dados:

```python
DB_HOST = 'seu-endpoint.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'sua-senha'
DB_NAME = 'pokedex'
```

### Popular o banco

```bash
# Popular com dados da PokeAPI (ajuste o TOTAL no arquivo)
python3 popular_banco.py

# Fazer upload das imagens para o S3
python3 upload_imagens_s3.py
```

### Rodar o servidor

```bash
python3 app.py
```

Acesse em `http://localhost:5000`

## API Endpoints

| Método | Rota                      | Descrição                      |
| ------ | ------------------------- | ------------------------------ |
| GET    | `/`                       | Interface web da Pokédex       |
| GET    | `/pokemon`                | Lista todos os pokémons        |
| GET    | `/pokemon/buscar?q=termo` | Busca por nome, tipo ou número |

## Aprendizados

Este projeto foi desenvolvido como prática de integração entre:

- Infraestrutura em nuvem AWS
- Banco de dados relacional MySQL
- Desenvolvimento backend com Python Flask
- Desenvolvimento frontend com HTML, CSS e JavaScript

## Demonstração

https://github.com/user-attachments/assets/b346cdef-81f0-4beb-9294-81f5d72f32f6



## Autor

Lucas Jose
