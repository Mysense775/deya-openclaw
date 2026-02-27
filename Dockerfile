# Deya OpenClaw Instance
# Полный инстанс с веб-интерфейсом

FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js (for OpenClaw)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Create user
RUN useradd -m -s /bin/bash openclaw

# Set working directory
WORKDIR /home/openclaw

# Stage 2: Install OpenClaw
FROM base as openclaw-install

# Download and install OpenClaw
RUN curl -fsSL https://github.com/openclaw/openclaw/releases/latest/download/openclaw-linux-amd64 -o /usr/local/bin/openclaw \
    && chmod +x /usr/local/bin/openclaw

# Stage 3: Install skills
FROM openclaw-install as skills-install

COPY skills/ /tmp/skills/

# Extract and install skills
RUN mkdir -p /home/openclaw/.openclaw/workspace/skills && \
    cd /tmp/skills && \
    for skill in *.skill; do \
        if [ -f "$skill" ]; then \
            name=$(basename "$skill" .skill); \
            mkdir -p "/home/openclaw/.openclaw/workspace/skills/$name"; \
            tar -xzf "$skill" -C "/home/openclaw/.openclaw/workspace/skills/$name" --strip-components=1; \
        fi \
    done

# Install Python dependencies for skills
RUN cd /home/openclaw/.openclaw/workspace/skills/deya-dashboard && \
    pip install --no-cache-dir -r requirements.txt

# Stage 4: Final image
FROM skills-install as final

# Create workspace structure
RUN mkdir -p /home/openclaw/.openclaw/workspace/memory && \
    mkdir -p /home/openclaw/.openclaw/logs && \
    mkdir -p /home/openclaw/.openclaw/assets

# Copy identity files
COPY config/IDENTITY.md /home/openclaw/.openclaw/workspace/
COPY config/SOUL.md /home/openclaw/.openclaw/workspace/
COPY config/USER.md /home/openclaw/.openclaw/workspace/
COPY config/AGENTS.md /home/openclaw/.openclaw/workspace/

# Copy startup script
COPY scripts/start.sh /usr/local/bin/start-deya
RUN chmod +x /usr/local/bin/start-deya

# Set ownership
RUN chown -R openclaw:openclaw /home/openclaw

# Switch to user
USER openclaw

# Set environment
ENV HOME=/home/openclaw
ENV OPENCLAW_CONFIG=/home/openclaw/.openclaw/config.yaml
ENV PYTHONPATH=/home/openclaw/.openclaw/workspace/skills/deya-dashboard

# Expose ports
EXPOSE 8000 8001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8001 || exit 1

# Start command
CMD ["start-deya"]
