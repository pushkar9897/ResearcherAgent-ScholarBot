# # ---------------------------
# # Use official slim Python base (multi-arch: works for amd64 + arm64)
# # ---------------------------
# # syntax=docker/dockerfile:1

# FROM python:3-alpine


# # ---------------------------
# # Environment variables
# # ---------------------------
# ENV DEBIAN_FRONTEND=noninteractive \
#     PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1

# # ---------------------------
# # Set working directory
# # ---------------------------
# WORKDIR /app

# # ---------------------------
# # Install system dependencies
# # ---------------------------
# # RUN apt-get update && \
# #     apt-get upgrade -y && \
# #     apt-get install -y --no-install-recommends \
# #     build-essential \
# #     ca-certificates \
# #     curl \
# #     wget \
# #     unzip \
# #     libgl1 \
# #     libglib2.0-0 \
# #     && apt-get clean && rm -rf /var/lib/apt/lists/*

# RUN apk update && \
#     apk upgrade && \
#     apk add --no-cache \
#     build-base \
#     ca-certificates \
#     curl \
#     wget \
#     unzip \
#     libgl1 \
#     libglib \


# # ---------------------------
# # Install Python dependencies
# # ---------------------------
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # ---------------------------
# # Copy app files
# # ---------------------------
# COPY . .

# # ---------------------------
# # Create non-root user
# # ---------------------------
# RUN useradd -m appuser
# USER appuser

# # ---------------------------
# # Expose Streamlit default port
# # ---------------------------
# EXPOSE 8501

# # ---------------------------
# # Run Streamlit
# # ---------------------------
# CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]










# Use official Python Alpine image (supports multi-arch: amd64 + arm64)
# syntax=docker/dockerfile:1

FROM python:3-alpine

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
# RUN sudo apt-get update && \
#     sudo apt-get upgrade -y && \
#     sudo apt-get install -y --no-install-recommends \
#     build-essential \
#     ca-certificates \
#     curl \
#     wget \
#     unzip \
#     libgl1 \
#     libglib2.0-0 \
#     && sudo apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
        build-base \
        ca-certificates \
        curl \
        wget \
        unzip \
        mesa-gl \
        glib \
        py3-opengl
# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Create non-root user and set permissions
RUN addgroup -S appgroup && adduser -S -G appgroup appuser && \
    chown -R appuser:appgroup /app

USER appuser

# Expose Streamlit default port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]

