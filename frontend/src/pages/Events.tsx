import React from 'react';
import { api } from '../lib/api';

type Event = {
  id: number;
  date: string;
  competition_id: number;
  team_a_id: number;
  team_b_id: number;
  status: 'prematch' | 'live' | 'finished';
};

export const Events: React.FC = () => {
  const [rows, setRows] = React.useState<Event[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    api<Event[]>('/events')
      .then(setRows)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading…</div>;
  if (error) return <div style={{ color: 'crimson' }}>{error}</div>;

  return (
    <div>
      <h3>Events</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            {['ID', 'Date', 'Competition', 'Team A', 'Team B', 'Status'].map(
              (h) => (
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
              )
            )}
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id}>
              <td style={{ padding: 6 }}>{r.id}</td>
              <td style={{ padding: 6 }}>
                {new Date(r.date).toLocaleString()}
              </td>
              <td style={{ padding: 6 }}>{r.competition_id}</td>
              <td style={{ padding: 6 }}>{r.team_a_id}</td>
              <td style={{ padding: 6 }}>{r.team_b_id}</td>
              <td style={{ padding: 6 }}>{r.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
