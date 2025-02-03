# Base image
FROM ubuntu:22.04

# Set environment variables for non-interactive installs
ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/usr/local/bin:$PATH"
ENV CFLAGS="-I/usr/local/include"
ENV LDFLAGS="-L/usr/local/lib -lintl"

# Install necessary tools and MinGW-w64 for cross-compilation
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential \
    mingw-w64 \
    wget \
    curl \
    git \
    gettext \
    libgettextpo-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Nuitka
RUN pip install --upgrade pip && pip install nuitka

# Set the working directory in the container
WORKDIR /app

# Copy your Python application into the container
COPY . /app

# Install Python dependencies for the application (if any)
RUN pip install -r requirements.txt || true

# Command to compile the Python script to a Windows executable
# Replace "jenkins.py" with the name of your script
CMD ["python3", "-m", "nuitka", "--mingw64", "--lto=yes", "--clang", "jenkins.py"]
