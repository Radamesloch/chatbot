FROM python:3.10.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt_tab

COPY . /app/

EXPOSE 5000

CMD ["python", "router.py"]