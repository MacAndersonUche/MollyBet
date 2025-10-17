import React from 'react';
import { api } from '../lib/api';

type Money = { amount: number; currency: 'USD' | 'GBP' | 'EUR' };

type Customer = {
  id: number;
  username: string;
  real_name: string;
  currency: Money['currency'];
  status: 'active' | 'disabled';
  balance: Money;
  created_at: string;
};

export const Customers: React.FC = () => {
  const [rows, setRows] = React.useState<Customer[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    api<Customer[]>('/customers')
      .then(setRows)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading…</div>;
  if (error) return <div style={{ color: 'crimson' }}>{error}</div>;

  return (
    <div>
      <h3>Customers</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            {['ID', 'Username', 'Name', 'Currency', 'Balance', 'Status'].map(
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
              <td style={{ padding: 6 }}>{r.username}</td>
              <td style={{ padding: 6 }}>{r.real_name}</td>
              <td style={{ padding: 6 }}>{r.currency}</td>
              <td style={{ padding: 6 }}>
                {r.balance.amount.toFixed(2)} {r.balance.currency}
              </td>
              <td style={{ padding: 6 }}>{r.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
