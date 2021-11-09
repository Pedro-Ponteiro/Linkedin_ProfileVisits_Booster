FROM python:3.8


RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get install -y google-chrome-stable \
    && apt-get install -y nano \
    && apt-get -y update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY . /app/
RUN pip install -r --no-cache-dir requirements.txt

CMD ["bash"]
