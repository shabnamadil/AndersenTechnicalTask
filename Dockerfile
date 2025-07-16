# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /code

# Install build tools and Python dev headers required for uWSGI
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libpcre3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements_prod.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements_prod.txt

# Create a non-root user
RUN addgroup --system django && adduser --system --ingroup django django

# Copy app source
COPY ./app /code

# Copy config files
COPY uwsgi.ini /conf/uwsgi.ini

# Copy entrypoint script
COPY starter.sh /starter.sh
RUN chmod +x /starter.sh

# Set permissions
RUN chown -R django:django /code

# Switch to non-root user
USER django

# Expose Django port
EXPOSE 8000

# Start the app using entrypoint
ENTRYPOINT ["/starter.sh"]

# Run uWSGI with the appropriate configuration
CMD ["uwsgi", "--ini", "/conf/uwsgi.ini"]