import { useEffect, useState } from 'react';
import api from '../../services/api';

export default function Dashboard() {
  const [monitors, setMonitors] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/monitors')
      .then(res => setMonitors(res.data))
      .catch(() => setMonitors([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      {loading ? <p>Loading...</p> : (
        <ul>
          {monitors.map(m => (
            <li key={m.id}>{m.name} - {m.url} - {m.is_active ? 'Active' : 'Paused'}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
