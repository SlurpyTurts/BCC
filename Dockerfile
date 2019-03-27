FROM python:2.7
COPY test.py test.py
COPY bcc-site/* ./
RUN pip install Flask
#CMD ["python", "test.py"]
CMD ["sh", "./run.sh"]
