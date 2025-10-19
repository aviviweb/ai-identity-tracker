import { Router } from 'express';
import { pool } from '../db/connection.js';

const router = Router();

router.get('/test', async (_req, res) => {
  try {
    const now = await pool.query('SELECT NOW() AS now');
    return res.json({ message: 'שרת פעיל והחיבור למסד הצליח!', now: now.rows[0].now });
  } catch (err) {
    return res.status(500).json({ error: 'DB connection failed', detail: String(err) });
  }
});

export default router;

