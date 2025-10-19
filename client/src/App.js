import { useState } from 'react';

function App() {
  const [result, setResult] = useState(null);

  const checkServer = async () => {
    try {
      const res = await fetch('/api/test');
      const json = await res.json();
      setResult(json);
    } catch (e) {
      setResult({ error: 'Failed to reach server', detail: String(e) });
    }
  };

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h1>ברוך הבא לאפליקציה שלי 🚀</h1>
      <button onClick={checkServer}>בדיקת תקשורת לשרת</button>
      <pre>{result ? JSON.stringify(result, null, 2) : '—'}</pre>
    </div>
  );
}

export default App;

