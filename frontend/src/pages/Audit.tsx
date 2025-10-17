import React from 'react';
import { api } from '../lib/api';

type Audit = {
  id: number;
  table_name: string;
  operation: 'INSERT' | 'UPDATE' | 'DELETE';
  username: string;
  changed_at: string;
  row_id: number | null;
};

export const Audit: React.FC = () => {
  const [rows, setRows] = React.useState<Audit[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    api<Audit[]>('/audit')
      .then(setRows)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading…</div>;
  if (error) return <div style={{ color: 'crimson' }}>{error}</div>;

  return (
    <div>
      <h3>Audit Log</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            {['ID', 'Table', 'Operation', 'User', 'At', 'Row'].map((h) => (
              <th
                key={h}
                style={{
                  textAlign: 'left',
                  borderBottom: '1px solid #ddd',
                  padding: 6,
                }}
              >
                {h}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id}>
              <td style={{ padding: 6 }}>{r.id}</td>
              <td style={{ padding: 6 }}>{r.table_name}</td>
              <td style={{ padding: 6 }}>{r.operation}</td>
              <td style={{ padding: 6 }}>{r.username}</td>
              <td style={{ padding: 6 }}>
                {new Date(r.changed_at).toLocaleString()}
              </td>
              <td style={{ padding: 6 }}>{r.row_id ?? '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
