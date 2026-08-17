# Painel de rotatividade

Um painel de risco de rotatividade de funcionários com pontuação explicável e insights em nível de departamento.

## Visão geral

As empresas perdem dinheiro quando bons funcionários se demitem antes que a liderança perceba sinais de alerta. A rotatividade cria custos por meio de contratação, treinamento, perda de produtividade e impacto direto no moral da equipe.

Este painel ajuda os gerentes a identificar os funcionários com maior risco de saída antes de pedirem demissão. Combina salário, estabilidade, promoções, aumentos, ausências e advertências para gerar uma pontuação de risco clara e acionável.

## Demonstração

- Dashboard: https://turnover-dashboard-pi.vercel.app
- API: https://turnover-dashboard-production-2a7a.up.railway.app/docs

## Características

Cada funcionário recebe uma pontuação de 0 a 100 com base em seis fatores:

- Mais de dois anos sem promoção: 20 pontos
- Salário abaixo da média da função: 20 pontos
- Mais de três faltas nos últimos 12 meses: 15 pontos
- Menos de um ano na empresa: 15 pontos
- Advertências nos últimos 12 meses: 15 pontos
- Sem aumento nos últimos 12 meses: 15 pontos

Pontuação abaixo de 40 = Baixo Risco. De 40 a 70 = Risco Médio. Acima de 70 = Alto Risco.

## Pilha de tecnologia

- Back-end: Python, FastAPI, SQLAlchemy, PostgreSQL
- Front-end: React, Recharts
- Implantação: Ferrovia (backend), Vercel (frontend)

## Começando

### Opção rápida com Docker

```bash
git clone https://github.com/lucaspwalter/turnover-dashboard.git
cd turnover-dashboard
docker compose up
```

Open `http://localhost:3000`. API: `http://localhost:8000/docs`.

### Instalação manual

1. Clone o repositório:

```bash
git clone https://github.com/lucaspwalter/turnover-dashboard.git
cd turnover-dashboard
```

2. Crie e ative o ambiente virtual dentro do `backend`:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

3. Instale dependências:

```bash
pip install -r requirements.txt
```

4. Execute a API:

```bash
python3 main.py
```

5. Abra a documentação da API:

```text
http://localhost:8000/docs
```

6. Execute o frontend em outro terminal:

```bash
cd frontend
npm install
npm start
```

## Estrutura do Projeto

```text
turnover-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routes: employees, scores, and dashboard
│   │   ├── db/           # Database configuration
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business rules, including the scoring engine
│   ├── main.py           # FastAPI entry point
│   ├── seed.py           # Populates the database with sample data
│   └── requirements.txt  # Backend dependencies
├── frontend/
│   ├── src/
│   │   ├── components/   # Cards, department chart, and ranking table
│   │   ├── api.js        # Axios API client
│   │   └── App.jsx       # Main dashboard page
│   └── package.json      # Frontend dependencies and scripts
└── README.md
```

## Licença

Licenciado sob a licença MIT. Veja `LICENÇA`.
