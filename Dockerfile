FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY plot.py .
CMD ["plot.py"]
ENTRYPOINT ["python3"]