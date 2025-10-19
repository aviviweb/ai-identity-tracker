// Copies CRA build from ../client/build to ./client-build
const fs = require('fs');
const path = require('path');

// Support CRA (build) and Vite (dist)
const candidateDirs = [
  path.resolve(__dirname, '../client/build'),
  path.resolve(__dirname, '../client/dist'),
];
const src = candidateDirs.find((p) => fs.existsSync(p));
const dest = path.resolve(__dirname, './client-build');

function copyDirSync(sourceDir, targetDir) {
  if (!fs.existsSync(targetDir)) fs.mkdirSync(targetDir, { recursive: true });
  for (const entry of fs.readdirSync(sourceDir, { withFileTypes: true })) {
    const srcPath = path.join(sourceDir, entry.name);
    const destPath = path.join(targetDir, entry.name);
    if (entry.isDirectory()) {
      copyDirSync(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

if (!src) {
  console.error(`Client build not found. Looked for: ${candidateDirs.join(', ')}`);
  process.exit(0);
}

copyDirSync(src, dest);
console.log(`✔ Copied client build from ${src} to ${dest}`);

