import { useEffect, useState } from 'react';

import './App.css';
import api from './api';
import DepartmentChart from './components/DepartmentChart';
import RankingTable from './components/RankingTable';
import SummaryCards from './components/SummaryCards';

const initialSummary = {
  total_employees: 0,
  high_risk: 0,
  medium_risk: 0,
  low_risk: 0,
  high_risk_percentage: 0,
  average_score: 0,
};

function App() {
  const [summary, setSummary] = useState(initialSummary);
  const [departments, setDepartments] = useState([]);
  const [ranking, setRanking] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function loadDashboard() {
      try {
        setLoading(true);
        setError('');

        const [summaryResponse, departmentResponse, rankingResponse] =
          await Promise.all([
            api.get('/dashboard/summary'),
            api.get('/dashboard/by-department'),
            api.get('/scores/ranking'),
          ]);

        setSummary(summaryResponse.data);
        setDepartments(departmentResponse.data);
        setRanking(rankingResponse.data);
      } catch (err) {
        setError('Não foi possível carregar os dados do dashboard.');
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, []);

  if (loading) {
    return (
      <main className="app-shell">
        <div className="loading-state">Carregando dashboard...</div>
      </main>
    );
  }

  return (
    <main className="app-shell">
      <header className="page-header">
        <div>
          <h1>Dashboard de Turnover</h1>
          <p>
            Score médio geral: <strong>{Number(summary.average_score || 0).toFixed(1)}</strong>
          </p>
        </div>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <SummaryCards summary={summary} />
      <DepartmentChart data={departments} />
      <RankingTable ranking={ranking} />
    </main>
  );
}

export default App;
