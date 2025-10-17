import React from 'react';
import { api } from '../lib/api';

type Money = { amount: number; currency: 'USD' | 'GBP' | 'EUR' };

type Bet = {
  id: number;
  bookie: string;
  customer_id: number;
  bookie_bet_id: string;
  bet_type: string;
  event_id: number;
  sport: string;
  placement_status: 'pending' | 'placed' | 'failed';
  outcome: 'win' | 'lose' | 'void' | null;
  stake: Money;
  odds: number;
  placement_data: Record<string, unknown>;
  created_at: string;
  updated_at: string;
};

export const Bets: React.FC = () => {
  const [rows, setRows] = React.useState<Bet[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    api<Bet[]>('/bets')
      .then(setRows)
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading…</div>;
  if (error) return <div style={{ color: 'crimson' }}>{error}</div>;

  return (
    <div>
      <h3>Bets</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            {[
              'ID',
              'Bookie',
              'Customer',
              'Event',
              'Stake',
              'Odds',
              'Status',
              'Outcome',
            ].map((h) => (
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
              <td style={{ padding: 6 }}>{r.bookie}</td>
              <td style={{ padding: 6 }}>{r.customer_id}</td>
              <td style={{ padding: 6 }}>{r.event_id}</td>
              <td style={{ padding: 6 }}>
                {r.stake.amount.toFixed(2)} {r.stake.currency}
              </td>
              <td style={{ padding: 6 }}>{r.odds}</td>
              <td style={{ padding: 6 }}>{r.placement_status}</td>
              <td style={{ padding: 6 }}>{r.outcome ?? '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
