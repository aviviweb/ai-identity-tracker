import dotenv from 'dotenv';
import path from 'path';
import { fileURLToPath } from 'url';
import pkg from 'pg';

const { Pool } = pkg;
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// טוען .env משורש הפרויקט
dotenv.config({ path: path.resolve(__dirname, '../../.env') });

const useSsl = Boolean(process.env.DATABASE_URL?.includes('neon.tech') || process.env.PGSSL);
export const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: useSsl ? { rejectUnauthorized: false } : false,
});

