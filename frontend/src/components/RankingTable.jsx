const riskLabels = {
  HIGH: 'Alto',
  MEDIUM: 'Médio',
  LOW: 'Baixo',
};

const riskClassNames = {
  HIGH: 'risk-badge risk-high',
  MEDIUM: 'risk-badge risk-medium',
  LOW: 'risk-badge risk-low',
};

function RankingTable({ ranking }) {
  const topRanking = [...ranking]
    .sort((a, b) => Number(b.score || 0) - Number(a.score || 0))
    .slice(0, 10);

  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Top 10 Funcionários por Score</h2>
      </div>
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Nome</th>
              <th>Departamento</th>
              <th>Cargo</th>
              <th>Score</th>
              <th>Risco</th>
            </tr>
          </thead>
          <tbody>
            {topRanking.map((employee) => (
              <tr key={employee.employee_id}>
                <td>{employee.name}</td>
                <td>{employee.department}</td>
                <td>{employee.role}</td>
                <td>{Number(employee.score || 0).toFixed(0)}</td>
                <td>
                  <span className={riskClassNames[employee.risk_level] || 'risk-badge'}>
                    {riskLabels[employee.risk_level] || employee.risk_level}
                  </span>
                </td>
              </tr>
            ))}
            {topRanking.length === 0 && (
              <tr>
                <td colSpan="5" className="empty-state">
                  Nenhum score encontrado.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default RankingTable;
