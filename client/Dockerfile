# --- Stage 1: Build the React App ---
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Build the React app for production
RUN npm run build
# NOTE: If your project uses Vite, this might create a 'dist' folder instead.
# If so, change the COPY command below to: COPY --from=build /app/dist ...

# --- Stage 2: Serve with Nginx ---
FROM nginx:alpine

# Copy the build output from the previous stage to Nginx's html folder
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80 (Standard web port)
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]