const cards = [
  {
    key: 'total',
    title: 'Total de Funcionários',
    getValue: (summary) => summary.total_employees,
    className: 'summary-card summary-card-total',
  },
  {
    key: 'high',
    title: 'Alto Risco',
    getValue: (summary) => summary.high_risk,
    getDetail: (summary) =>
      `${Number(summary.high_risk_percentage || 0).toFixed(1)}% do total`,
    className: 'summary-card summary-card-high',
  },
  {
    key: 'medium',
    title: 'Médio Risco',
    getValue: (summary) => summary.medium_risk,
    className: 'summary-card summary-card-medium',
  },
  {
    key: 'low',
    title: 'Baixo Risco',
    getValue: (summary) => summary.low_risk,
    className: 'summary-card summary-card-low',
  },
];

function SummaryCards({ summary }) {
  return (
    <section className="summary-grid" aria-label="Resumo de risco">
      {cards.map((card) => (
        <article className={card.className} key={card.key}>
          <span>{card.title}</span>
          <strong>{card.getValue(summary) ?? 0}</strong>
          {card.getDetail && <small>{card.getDetail(summary)}</small>}
        </article>
      ))}
    </section>
  );
}

export default SummaryCards;
