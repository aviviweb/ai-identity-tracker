# --- build client ---
FROM node:18 AS client
WORKDIR /app/client
COPY client/package.json client/package-lock.json* ./
RUN npm install
COPY client/ .
RUN npm run build

# --- server ---
FROM node:18-alpine
WORKDIR /app/server
ENV NODE_ENV=production
ENV PORT=8080
COPY server/package.json server/package-lock.json* ./
RUN npm install --only=production
COPY server/ .
COPY --from=client /app/client/build ./client-build
EXPOSE 8080
CMD ["node","server.js"]
