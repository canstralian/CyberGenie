# Use Ubuntu as a base image
FROM ubuntu:20.04

# Set non-interactive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    subfinder \
    amass \
    httpx \
    nuclei \
    nikto \
    git \
    curl \
    bash \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Go (for Go-based tools like subfinder)
RUN curl -sSL https://golang.org/dl/go1.16.7.linux-amd64.tar.gz -o /tmp/go.tar.gz && \
    tar -C /usr/local -xzf /tmp/go.tar.gz && \
    rm /tmp/go.tar.gz

# Set Go binary path
ENV PATH=$PATH:/usr/local/go/bin

# Set working directory
WORKDIR /workspace

# Clone CyberGenie repo
RUN git clone https://github.com/canstralian/CyberGenie.git

# Make sure all scripts are executable
RUN chmod +x CyberGenie/scripts/bounty/*.sh

# Set the entry point to the init script
ENTRYPOINT ["bash", "CyberGenie/init.sh"]