# --- Stage 1: Build the React App ---
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

# --- Stage 2: Serve with Nginx ---
FROM nginx:alpine

# Copy the build output
COPY --from=build /app/build /usr/share/nginx/html

# --- CRITICAL FIX: Custom Nginx Config for React Router ---
# This "try_files" line tells Nginx: "If file doesn't exist, load index.html"
# This fixes the 404 error on /login and /profile
RUN echo 'server { \
    listen 80; \
    root /usr/share/nginx/html; \
    index index.html index.htm; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]