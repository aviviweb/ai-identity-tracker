import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import { pool } from './db/connection.js';
import apiRoutes from './routes/api.js';

const app = express();
const PORT = process.env.PORT || 8080;
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(cors());
app.use(express.json());
app.use('/api', apiRoutes);

// בדיקת חיבור למסד בעת עלייה
(async () => {
  try {
    await pool.query('SELECT 1');
    console.log('✅ Database connected');
  } catch (e) {
    console.error('❌ Database connection error:', e);
  }
})();

// הפצה סטטית בפרודקשן (Railway)
if (process.env.NODE_ENV === 'production') {
  const clientBuild = path.resolve(__dirname, './client-build');
  app.use(express.static(clientBuild));
  app.get('*', (_req, res) => {
    res.sendFile(path.join(clientBuild, 'index.html'));
  });
}

app.listen(PORT, () => console.log(`🚀 Server listening on port ${PORT}`));

