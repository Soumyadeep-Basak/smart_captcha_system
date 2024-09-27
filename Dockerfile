# Dockerfile for Next.js app

# Use an official Node.js image as the base image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the container
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application to the container
COPY . .

# Build the Next.js app
RUN npm run build

# Expose port 3000 for the Next.js app
EXPOSE 3000

# Start the Next.js app
CMD ["npm", "run", "start"]
