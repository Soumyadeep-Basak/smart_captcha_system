# Dockerfile for Next.js app

# Step 1: Build stage
FROM node:18 AS builder
WORKDIR /app

COPY ./app/package.json ./app/package-lock.json ./
RUN npm install

COPY ./app ./
RUN npm run build

# Step 2: Production stage
FROM node:18-alpine AS production
WORKDIR /app

COPY --from=builder /app ./
EXPOSE 3000

CMD ["npm", "run", "start"]
