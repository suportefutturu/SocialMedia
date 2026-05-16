# Tuitlog — Seu Diário Visual Diário

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Version: MVP](https://img.shields.io/badge/Version-MVP-green.svg)](https://github.com/tuitlog/tuitlog)

> Um espaço tranquilo para respirar, contemplar imagens e ler palavras. Resgatando a essência do antigo Fotolog com roupagem visual moderna, limpa e elegante.

---

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Configuração Local](#instalação-e-configuração-local)
- [Estrutura de Diretórios](#estrutura-de-diretórios)
- [Deploy em Produção](#deploy-em-produção)
- [Comandos Úteis](#comandos-úteis)
- [Personalização](#personalização)
- [Licença](#licença)

---

## Sobre o Projeto

**Tuitlog** é uma aplicação web que resgata a essência dos antigos fotologs — diários visuais populares nos anos 2000 — com uma estética contemporânea minimalista. O nome funde "Tuit" (variação carinhosa de "teu") com "log" (registro), significando literalmente "o teu registro pessoal".

### Contexto Histórico

Inspirado no icônico **Fotolog**, plataforma que revolucionou o compartilhamento de fotos diárias antes da era das redes sociais algorítmicas, o Tuitlog traz de volta:

- **Cronologia rígida**: Sem algoritmos de relevância. Tudo é exibido do mais recente ao mais antigo.
- **Uma foto por dia**: Para contas gratuitas, incentivando curadoria e hábito diário.
- **Personalização como identidade**: Cores e fontes que expressam individualidade.
- **Cultura de comunidade**: Amizades, mensagens e grupos temáticos.

### Diferenciais

| Característica | Descrição |
|----------------|-----------|
| 📅 Cronologia Pura | Nenhum feed algorítmico. Apenas ordem temporal. |
| 🎨 Design Minimalista | Espaço negativo, tipografia refinada, animações sutis. |
| 🌈 Personalização | Cada usuário customiza cores e fontes do próprio perfil. |
| 🤝 Tuitamigos | Sistema de amizades com lista pública navegável. |
| 📖 Tuitbook | Livro de visitas clássico, modernizado. |
| 🏘️ Tuitcomunidades | Grupos temáticos com feeds coletivos. |

### Stack Tecnológica

| Camada | Tecnologia |
|--------|------------|
| Backend | Python 3.9+ / Flask 3.0 |
| Banco de Dados | SQLite (dev) / PostgreSQL (prod) |
| Autenticação | Flask-Login |
| Frontend | HTML5 semântico / CSS moderno puro / JavaScript minimalista |
| Build | Nenhum framework — CSS e JS puros |

---

## Funcionalidades

### Núcleo do MVP

#### 1. Perfil de Usuário e Mural Cronológico (Tuitlog)
- **Foto do dia em destaque**: Imagem mais recente em área generosa no topo
- **Arquivo cronológico**: Grid responsivo de miniaturas em ordem reversa
- **Personalização visual**: Cores e fontes aplicadas dinamicamente
- **Sidebar informativa**: Avatar, bio, contador de visitas, Tuitamigos, Tuitcomunidades

#### 2. Sistema de Upload com Restrição Inteligente
- Interface drag-and-drop minimalista
- Bloqueio para contas gratuitas após primeira postagem do dia
- Mensagem amigável reforçando cultura de curadoria diária
- Feedback visual de upload com confirmação sutil

#### 3. Página de Detalhes da Foto (Tuit)
- Imagem grande com cantos arredondados e sombra suave
- Legenda e data em tipografia convidativa
- Contador de visualizações discreto
- Comentários cronológicos com limite de 20 por postagem
- Exclusão de comentários apenas pelo dono da foto

#### 4. Cultura de Comunidade e Descoberta
- **Página Inicial / Explorar**: Grid de Tuits recentes + ranking de perfis mais visitados
- **Tuitcomunidades**: Grupos temáticos criados por usuários com feeds coletivos

#### 5. Tuitbook (Livro de Visitas)
- Layout de cartões de mensagens
- Ordenação cronológica
- Design que evoca guestbooks clássicos com estética moderna

#### 6. Interação Social
- **Tuitamigos**: Botões de adicionar/remover amizade proeminentes
- **Compartilhamento**: Menu dropdown com Twitter/X, Facebook, WhatsApp, Telegram, Pinterest

### Vocabulário Próprio

| Termo | Significado |
|-------|-------------|
| **Tuitlog** | O perfil/diário visual de um usuário |
| **Tuit** | Uma postagem individual (foto + legenda) |
| **Tuitamigos** | Lista de amigos/conexões |
| **Tuitbook** | Livro de visitas do perfil |
| **Tuitcomunidade** | Grupo temático de usuários |

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.9 ou superior** — [Download](https://www.python.org/downloads/)
- **pip atualizado** — Geralmente incluído com Python
- **Git** — [Download](https://git-scm.com/)
- **Navegador moderno** — Chrome, Firefox, Safari ou Edge

Verifique as versões:

```bash
python --version    # Deve ser 3.9+
pip --version       # Versão recente
git --version       # Qualquer versão recente
```

---

## Instalação e Configuração Local

Siga estes passos para rodar o Tuitlog em seu ambiente de desenvolvimento:

### Passo 1: Clonar o Repositório

```bash
cd /workspace
git clone https://github.com/seu-usuario/tuitlog.git
cd tuitlog
```

### Passo 2: Criar Ambiente Virtual

```bash
python -m venv venv
```

### Passo 3: Ativar Ambiente Virtual

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Passo 4: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 5: Configurar Variáveis de Ambiente

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Edite `.env` conforme necessário:

```env
SECRET_KEY=sua-chave-secreta-muito-segura-aqui
DATABASE_URL=sqlite:///tuitlog.db
UPLOAD_FOLDER=./static/uploads/photos
AVATAR_FOLDER=./static/uploads/avatars
MAX_CONTENT_LENGTH=16777216
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif
```

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `SECRET_KEY` | Chave para sessões e tokens CSRF | Obrigatório em produção |
| `DATABASE_URL` | URL de conexão do banco | `sqlite:///tuitlog.db` |
| `UPLOAD_FOLDER` | Pasta para fotos enviadas | `./static/uploads/photos` |
| `AVATAR_FOLDER` | Pasta para avatares | `./static/uploads/avatars` |
| `MAX_CONTENT_LENGTH` | Tamanho máximo de upload (bytes) | `16777216` (16MB) |
| `ALLOWED_EXTENSIONS` | Extensões permitidas | `png,jpg,jpeg,gif` |

### Passo 6: Inicializar Banco de Dados

O banco será criado automaticamente ao iniciar a aplicação. Para criar o usuário admin padrão:

```bash
python app.py
```

Na primeira execução, o script cria:
- Todas as tabelas do banco
- Um usuário admin (`admin` / `admin123`)

### Passo 7: Criar Pastas de Upload

As pastas já são criadas automaticamente, mas verifique:

```bash
mkdir -p static/uploads/photos static/uploads/avatars
```

### Passo 8: Executar Servidor de Desenvolvimento

```bash
python app.py
```

Ou usando Flask CLI:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=1313
```

### Passo 9: Acessar a Aplicação

Abra seu navegador em:

```
http://localhost:1313
```

### Testando a Aplicação

1. **Criar primeiro usuário**: Acesse `/register` e crie uma conta
2. **Fazer login**: Use `/login` com suas credenciais
3. **Postar foto**: Clique em "Novo Tuit" e faça upload
4. **Personalizar perfil**: Vá em "Editar Perfil" e mude cores/fontes
5. **Explorar**: Visite `/explorar` para ver postagens de todos

---

## Estrutura de Diretórios

```
tuitlog/
├── app.py                      # Aplicação principal Flask (rotas, modelos, lógica)
├── requirements.txt            # Dependências Python
├── .env.example                # Modelo de variáveis de ambiente
├── .gitignore                  # Arquivos ignorados pelo Git
├── README.md                   # Esta documentação
├── Dockerfile                  # Configuração Docker para produção
├── docker-compose.yml          # Orquestração de containers
│
├── instance/                   # Banco de dados SQLite (gerado automaticamente)
│   └── tuitlog.db
│
├── static/                     # Arquivos estáticos
│   ├── css/
│   │   └── style.css           # CSS principal (1100+ linhas)
│   ├── js/
│   │   └── main.js             # JavaScript minimalista
│   └── uploads/
│       ├── photos/             # Fotos dos Tuits
│       │   └── .gitkeep
│       └── avatars/            # Avatares dos usuários
│           └── .gitkeep
│
└── templates/                  # Templates HTML (Jinja2)
    ├── base.html               # Template base com header/footer
    ├── index.html              # Página inicial
    ├── profile.html            # Perfil de usuário
    ├── view_post.html          # Detalhes de um Tuit
    ├── create_post.html        # Formulário de novo Tuit
    ├── login.html              # Login
    ├── register.html           # Registro
    ├── edit_profile.html       # Edição de perfil
    ├── tuitbook.html           # Livro de visitas
    ├── explore.html            # Explorar posts
    ├── communities.html        # Lista de comunidades
    ├── view_community.html     # Detalhes da comunidade
    └── create_community.html   # Criar comunidade
```

### Descrição dos Arquivos Principais

| Arquivo | Responsabilidade |
|---------|------------------|
| `app.py` | Toda a lógica backend: modelos SQLAlchemy, rotas, autenticação, upload |
| `style.css` | Sistema visual completo: variáveis CSS, componentes, responsividade |
| `main.js` | Interações discretas: dropdowns, drag-drop, auto-hide de mensagens |
| `base.html` | Layout mestre com navegação e footer |

---

## Deploy em Produção

### Cenário A: Deploy em VPS Linux (DigitalOcean / Linode / AWS EC2)

#### Preparação do Servidor (Ubuntu 22.04)

```bash
# Atualizar pacotes
sudo apt update && sudo apt upgrade -y

# Instalar dependências do sistema
sudo apt install -y python3-pip python3-venv nginx git supervisor
```

#### Clone e Configuração

```bash
# Clonar repositório
cd /var/www
sudo git clone https://github.com/seu-usuario/tuitlog.git
cd tuitlog

# Criar ambiente virtual
sudo python3 -m venv venv
sudo source venv/bin/activate

# Instalar dependências
sudo pip install -r requirements.txt
sudo pip install gunicorn
```

#### Configurar Gunicorn

Crie `/etc/systemd/system/tuitlog.service`:

```ini
[Unit]
Description=Tuitlog Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/tuitlog
Environment="PATH=/var/www/tuitlog/venv/bin"
ExecStart=/var/www/tuitlog/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar e iniciar serviço
sudo systemctl enable tuitlog
sudo systemctl start tuitlog
sudo systemctl status tuitlog
```

#### Configurar Nginx

Crie `/etc/nginx/sites-available/tuitlog`:

```nginx
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;

    location /static {
        alias /var/www/tuitlog/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /uploads {
        alias /var/www/tuitlog/static/uploads;
        expires 7d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Habilitar site
sudo ln -s /etc/nginx/sites-available/tuitlog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Firewall e SSL

```bash
# Configurar firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable

# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obter certificado SSL
sudo certbot --nginx -d seudominio.com -d www.seudominio.com
```

#### Variáveis de Ambiente em Produção

Edite `/var/www/tuitlog/.env`:

```env
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
DATABASE_URL=sqlite:///instance/tuitlog.db
```

---

### Cenário B: Deploy em Plataforma PaaS (Render / Railway / Fly.io)

#### Render.com

1. **Preparar Repositório**: Certifique-se de ter `requirements.txt` na raiz

2. **Criar `render.yaml`**:

```yaml
services:
  - type: web
    name: tuitlog
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: tuitlog-db
          property: connectionString

databases:
  - name: tuitlog-db
    databaseName: tuitlog
    user: tuitlog
```

3. **Configurar no Render**:
   - Conecte seu repositório GitHub
   - O `render.yaml` será detectado automaticamente
   - Configure variáveis de ambiente adicionais no dashboard

4. **Migrar para PostgreSQL**: No primeiro deploy, o Render provisionará o banco

#### Railway.app

1. **Deploy via GitHub**:
   - Conecte sua conta Railway ao GitHub
   - Selecione o repositório do Tuitlog

2. **Configurar Variáveis**:
   ```
   SECRET_KEY=<gerar-aleatorio>
   DATABASE_URL=<provisionar-postgres-no-railway>
   ```

3. **Build e Start automáticos**: Railway detecta `requirements.txt`

#### Fly.io

1. **Instalar Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   fly auth login
   ```

2. **Inicializar App**:
   ```bash
   fly launch --name tuitlog
   ```

3. **Configurar `fly.toml`**:
   ```toml
   [build]
   
   [app]
     primary_region = "gru"
   
   [http_service]
     internal_port = 8000
     force_https = true
   
   [[vm]]
     cpu_kind = "shared"
     cpus = 1
     memory_mb = 256
   
   [mounts]
     source = "uploads_data"
     destination = "/app/static/uploads"
   ```

4. **Deploy**:
   ```bash
   fly deploy
   fly secrets set SECRET_KEY=$(openssl rand -hex 32)
   ```

---

### Cenário C: Deploy com Docker

#### Dockerfile

```dockerfile
# Multi-stage build para imagem otimizada
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV FLASK_APP=app
ENV PYTHONUNBUFFERED=1

# Criar volumes para persistência
VOLUME ["/app/static/uploads", "/app/instance"]

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "1313:8000"
    environment:
      - SECRET_KEY=${SECRET_KEY:-dev-key-change-in-production}
      - DATABASE_URL=sqlite:///instance/tuitlog.db
    volumes:
      - uploads_data:/app/static/uploads
      - db_data:/app/instance
    restart: unless-stopped

volumes:
  uploads_data:
  db_data:
```

#### Build e Execução

```bash
# Build da imagem
docker-compose build

# Executar
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Parar
docker-compose down
```

#### Deploy em Provedores Container

**AWS ECS**:
```bash
aws ecs create-cluster --cluster-name tuitlog
aws ecs create-service --cluster tuitlog --service-name tuitlog-web \
  --task-definition tuitlog-task --desired-count 1
```

**Google Cloud Run**:
```bash
gcloud run deploy tuitlog \
  --image gcr.io/seu-projeto/tuitlog:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

**Azure Container Instances**:
```bash
az container create \
  --resource-group tuitlog-rg \
  --name tuitlog \
  --image seuacr.azurecr.io/tuitlog:latest \
  --dns-name-label tuitlog \
  --ports 8000
```

---

## Comandos Úteis

| Comando | Descrição |
|---------|-----------|
| `python app.py` | Iniciar servidor de desenvolvimento |
| `flask run --host=0.0.0.0 --port=1313` | Alternativa com Flask CLI |
| `pip install -r requirements.txt` | Instalar/atualizar dependências |
| `python -m venv venv` | Criar ambiente virtual |
| `source venv/bin/activate` | Ativar ambiente (Linux/Mac) |
| `docker-compose up -d` | Rodar com Docker |
| `docker-compose down` | Parar containers Docker |
| `sqlite3 instance/tuitlog.db` | Acessar banco SQLite diretamente |

### Shell do Flask (para administração)

```bash
flask shell
```

Dentro do shell:

```python
from app import db, User

# Criar usuário admin manualmente
admin = User(username='admin', email='admin@tuitlog.com', display_name='Admin')
admin.set_password('senha-forte')
db.session.add(admin)
db.session.commit()

# Listar usuários
User.query.all()

# Resetar banco (cuidado!)
db.drop_all()
db.create_all()
```

---

## Personalização

### Alterar Cores Padrão

Edite `static/css/style.css`:

```css
:root {
    --color-accent: #2d5a5a;        /* Cor primária */
    --color-accent-light: #3d7a7a;  /* Hover */
    --color-accent-dark: #1d3a3a;   /* Active */
    
    --color-bg-primary: #fafafa;    /* Fundo principal */
    --color-text-primary: #1a1a1a;  /* Texto principal */
}
```

### Adicionar Novas Fontes

1. Adicione no `<head>` do `templates/base.html`:

```html
<link href="https://fonts.googleapis.com/css2?family=Nova+Square&display=swap" rel="stylesheet">
```

2. Atualize as opções em `templates/edit_profile.html`:

```html
<option value="'Nova Square', cursive">Nova Square (Display)</option>
```

3. Adicione à variável no modelo `User`:

```python
font_family = db.Column(db.String(50), default="'Inter', sans-serif")
```

### Modificar o Slogan

Edite `templates/base.html`:

```html
<div class="logo-tagline">Seu slogan personalizado aqui</div>
```

E no footer:

```html
<div class="footer-tagline">Seu slogan personalizado aqui</div>
```

---

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

```
MIT License

Copyright (c) 2024 Tuitlog

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

**Feito com calma e cuidado.** 🌿
