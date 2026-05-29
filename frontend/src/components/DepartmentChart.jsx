import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

function DepartmentChart({ data }) {
  return (
    <section className="panel">
      <div className="panel-header">
        <h2>Risco por Departamento</h2>
      </div>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 12, right: 20, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="department" tickLine={false} axisLine={false} />
            <YAxis allowDecimals={false} tickLine={false} axisLine={false} />
            <Tooltip />
            <Legend />
            <Bar dataKey="high_risk" name="Alto" fill="#dc2626" radius={[4, 4, 0, 0]} />
            <Bar dataKey="medium_risk" name="Médio" fill="#d97706" radius={[4, 4, 0, 0]} />
            <Bar dataKey="low_risk" name="Baixo" fill="#16a34a" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}

export default DepartmentChart;
