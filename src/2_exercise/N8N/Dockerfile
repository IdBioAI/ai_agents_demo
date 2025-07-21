FROM n8nio/n8n:next
USER root
# Install system dependencies for MySQL
RUN apk add --no-cache mysql-client
# Install NPM packages globally
RUN npm install -g \
    yahoo-finance2 \
    axios \
    mysql2 \
    node-fetch \
    moment \
    uuid
USER node