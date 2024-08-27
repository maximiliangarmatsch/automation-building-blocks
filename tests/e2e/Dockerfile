FROM ubuntu:22.04

# Set environment variable to stop tzdata asking questions
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ca-certificates \
    xauth \
    xvfb \
    openbox \
    psmisc \
    procps \
    vim \
    python3 \
    python3-pip \
    python3-venv \
    wget \
    unzip \
    fonts-liberation \
    libasound2 \
    libgbm1 \
    libnspr4 \
    libnss3 \
    libu2f-udev \
    xdg-utils \
    python3-tk \
    python3-dev \
    gnome-screenshot \
    libvulkan1 && \
    rm -rf /var/lib/apt/lists/*

# For Xauth Authority error
RUN touch ~/.Xauthority

RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip setuptools wheel && \
    /opt/venv/bin/pip install selenium pyautogui

# Download and install Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb || true && \
    apt-get install -f -y && \
    rm google-chrome-stable_current_amd64.deb

# Download and install ChromeDriver
RUN wget -q https://chromedriver.storage.googleapis.com/126.0.6478.126/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip || true

WORKDIR /home

COPY script/start_virtual_display.sh /home/start_virtual_display.sh
COPY script/stop_virtual_display.sh /home/stop_virtual_display.sh
COPY virtual_display_pyautogui.py /home/virtual_display_pyautogui.py

RUN chmod +x /home/start_virtual_display.sh && \
    chmod +x /home/stop_virtual_display.sh

RUN mkdir /home/screenshots

ENTRYPOINT ["/bin/bash"]