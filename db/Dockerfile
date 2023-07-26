# Use the official PostgreSQL image as the base image
FROM postgres:latest

# Set environment variables for PostgreSQL configuration (optional but recommended)
ENV POSTGRES_USER=admin
ENV POSTGRES_PASSWORD=admin
ENV POSTGRES_DB=test

# Expose the PostgreSQL port
EXPOSE 5432

# Use the official pgAdmin image as the base image
FROM dpage/pgadmin4:latest

# Set environment variables for pgAdmin configuration (optional but recommended)
ENV PGADMIN_DEFAULT_EMAIL=admin@admin.com
ENV PGADMIN_DEFAULT_PASSWORD=root

# Expose the pgAdmin port
EXPOSE 80

# Add a configuration file for pgAdmin to connect to the PostgreSQL container
ADD servers.json /pgadmin4/servers.json
