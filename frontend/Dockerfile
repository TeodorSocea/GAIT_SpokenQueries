# Use official Node.js image as base
FROM node:18-alpine as build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json ./

# Install dependencies
RUN npm install --force

# Copy the rest of the application
COPY . ./

# Build the React app
RUN npm run build

# Use Nginx for serving static files
FROM nginx:alpine

# Copy built React files to Nginx's default directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
