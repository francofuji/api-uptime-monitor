import { useEffect, useState } from 'react';
import api from '../../services/api';

export default function Monitors() {
  const [monitors, setMonitors] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    api.get('/monitors')
      .then(res => setMonitors(res.data))
      .catch(() => setError('Failed to load monitors'))
      .finally(() => setLoading(false));
  }, []);

  const handlePause = async (id: string) => {
    await api.post(`/monitors/${id}/pause`);
    setMonitors(monitors.map(m => m.id === id ? { ...m, is_active: false } : m));
  };
  const handleResume = async (id: string) => {
    await api.post(`/monitors/${id}/resume`);
    setMonitors(monitors.map(m => m.id === id ? { ...m, is_active: true } : m));
  };
  const handleDelete = async (id: string) => {
    await api.delete(`/monitors/${id}`);
    setMonitors(monitors.filter(m => m.id !== id));
  };

  return (
    <div>
      <h1>Monitors</h1>
      {loading ? <p>Loading...</p> : error ? <p style={{color:'red'}}>{error}</p> : (
        <ul>
          {monitors.map(m => (
            <li key={m.id}>
              {m.name} - {m.url} - {m.is_active ? 'Active' : 'Paused'}
              <button onClick={() => handlePause(m.id)} disabled={!m.is_active}>Pause</button>
              <button onClick={() => handleResume(m.id)} disabled={m.is_active}>Resume</button>
              <button onClick={() => handleDelete(m.id)}>Delete</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
