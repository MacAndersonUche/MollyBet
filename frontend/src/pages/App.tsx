import React from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';

export const App: React.FC = () => {
  const { pathname } = useLocation();
  return (
    <div
      style={{
        fontFamily: 'Inter, system-ui, Avenir, Helvetica, Arial, sans-serif',
      }}
    >
      <header
        style={{
          padding: '12px 16px',
          borderBottom: '1px solid #eee',
          display: 'flex',
          gap: 12,
        }}
      >
        <strong>Betting Admin</strong>
        <nav style={{ display: 'flex', gap: 10 }}>
          <Link to="/">Bets</Link>
          <Link to="/customers">Customers</Link>
          <Link to="/events">Events</Link>
          <Link to="/audit">Audit</Link>
        </nav>
        <span style={{ marginLeft: 'auto', color: '#888' }}>{pathname}</span>
      </header>
      <main style={{ padding: 16 }}>
        <Outlet />
      </main>
    </div>
  );
};
