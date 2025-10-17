FROM node:20-alpine as build
WORKDIR /app
COPY frontend/package.json frontend/tsconfig.json frontend/vite.config.ts /app/
COPY frontend/index.html /app/index.html
COPY frontend/src /app/src
RUN npm ci || npm i
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]


