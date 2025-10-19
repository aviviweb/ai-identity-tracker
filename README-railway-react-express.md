# פרויקט React + Express + PostgreSQL (Neon) מוכן לפריסה ב‑Railway

מסמך זה מדריך אותך צעד‑אחר‑צעד להקמה מקומית ופריסה חינמית ל‑Railway.

## דרישות מקדימות
- Node.js 18+
- חשבון Neon.tech (מסד PostgreSQL חינמי)
- חשבון Railway.app

## 1) יצירת מסד ב‑Neon וקבלת DATABASE_URL
1. הירשם ל‑Neon.
2. צור Project + Branch + Database.
3. העתק את ה‑Connection string (Postgres). דוגמה:
   `postgresql://user:pass@ep-xyz.eu-central-1.aws.neon.tech/dbname?sslmode=require`
4. שמור את ה‑URL לשימוש בקובץ `.env` בשורש הפרויקט.

## 2) קובץ `.env` בשורש
צור קובץ `.env` בשורש עם:
```env
DATABASE_URL=postgresql://user:pass@ep-xyz.eu-central-1.aws.neon.tech/dbname?sslmode=require
PORT=8080
PGSSL=1
```

## 3) התקנת צד שרת והרצה מקומית
```bash
cd server
npm install
npm run dev
```
בדוק:
- http://localhost:8080/api/test צריך להחזיר JSON עם הודעת הצלחה וזמן נוכחי.

## 4) יצירת לקוח React (CRA) והרצה
```bash
npx create-react-app client
cd client
npm start
```
לאחר יצירה, ודא שב‑`client/package.json` קיים:
```json
{
  "proxy": "http://localhost:8080"
}
```
ועדכן את `client/src/App.js` להצגת הודעה בעברית וכפתור הבודק `/api/test`.

דוגמה ל־`client/src/App.js`:
```js
import { useState } from 'react';

function App() {
  const [result, setResult] = useState(null);
  const checkServer = async () => {
    const res = await fetch('/api/test');
    const json = await res.json();
    setResult(json);
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
```

## 5) בניית הלקוח ושילוב בפרודקשן
בנה את ה‑client והעתק את ה‑build אל `server/client-build`:
```bash
cd client && npm run build && cd ..
cd server && npm run postbuild
```
בפרודקשן (Railway), השרת יגיש סטטי מתוך `server/client-build`.

## 6) פריסה ל‑Railway
1. התחבר ל‑Railway ולחץ New Project → Deploy from GitHub (בחר את הריפו).
2. הגדר Variables:
   - `DATABASE_URL` (מה‑Neon)
   - `NODE_ENV=production`
3. הגדר פקודות:
   - Build command:
     ```bash
     npm --prefix server install && npm --prefix client ci && npm --prefix client run build && npm --prefix server ci && npm --prefix server run postbuild
     ```
   - Start command:
     ```bash
     npm --prefix server start
     ```
4. פרוס ולחץ על ה‑URL שקיבלת. `/api/test` אמור לעבוד, וה‑UI יוגש מהשורש.

## תקלות נפוצות
- SSL ב‑Neon: השאר `sslmode=require` ב‑DATABASE_URL או `PGSSL=1`.
- PORT: Railway מקצה PORT; Express מאזין על `process.env.PORT || 8080`.
- CORS: בפרודקשן מגישים סטטי מאותו דומיין ולכן אין בעיית CORS.

בהצלחה! 🚀
