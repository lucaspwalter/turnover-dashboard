# Dashboard de Turnover

## O que é

Empresas perdem dinheiro quando bons funcionários pedem demissão sem que a liderança perceba os sinais com antecedência. Turnover gera custo com contratação, treinamento, perda de produtividade e impacto direto no clima do time.

Este dashboard ajuda gestores a identificar funcionários com maior risco de saída antes que o pedido de demissão aconteça. A ferramenta cruza dados de salário, tempo de casa, promoções, aumentos, faltas e advertências para gerar um score de risco claro e acionável.

## Demonstração

- Link do dashboard: https://turnover-dashboard-pi.vercel.app
- Link da API: https://turnover-dashboard-production-2a7a.up.railway.app/docs

## Como funciona a engine de score

Cada funcionário recebe um score de 0 a 100 baseado em 6 fatores:

- Tempo sem promoção maior que 2 anos: 20 pontos
- Salário abaixo da média do cargo: 20 pontos
- Faltas acima de 3 nos últimos 12 meses: 15 pontos
- Tempo de casa menor que 1 ano: 15 pontos
- Advertências nos últimos 12 meses: 15 pontos
- Sem aumento nos últimos 12 meses: 15 pontos

Score abaixo de 40 = Baixo Risco. Entre 40 e 70 = Médio Risco. Acima de 70 = Alto Risco.

## Tecnologias

- Back-end: Python, FastAPI, SQLAlchemy, PostgreSQL
- Front-end: React, Recharts
- Deploy: Railway (back-end), Vercel (front-end)

## Como rodar localmente

1. Clone o repositório:

```bash
git clone https://github.com/lucaspwalter/turnover-dashboard.git
cd turnover-dashboard
```

2. Crie e ative o ambiente virtual no diretório `backend`:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Rode a API:

```bash
python3 main.py
```

5. Acesse a documentação da API:

```text
http://localhost:8000/docs
```

6. Rode o frontend em outro terminal:

```bash
cd frontend
npm install
npm start
```

## Estrutura do projeto

```text
turnover-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/          # Rotas FastAPI: funcionários, scores e dashboard
│   │   ├── db/           # Configuração do banco de dados
│   │   ├── models/       # Modelos SQLAlchemy
│   │   ├── schemas/      # Schemas Pydantic
│   │   └── services/     # Regras de negócio, incluindo engine de score
│   ├── main.py           # Entrada da API FastAPI
│   ├── seed.py           # Popula o banco com dados fictícios
│   └── requirements.txt  # Dependências do back-end
├── frontend/
│   ├── src/
│   │   ├── components/   # Cards, gráfico por departamento e tabela de ranking
│   │   ├── api.js        # Cliente Axios da API
│   │   └── App.jsx       # Página principal do dashboard
│   └── package.json      # Dependências e scripts do front-end
└── README.md
```
