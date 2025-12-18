FROM python:3.10
EXPOSE 5000:5000
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

# build: docker build -t rest-apis-flask-python .
# run: docker run -d -p 5000:5000 rest-apis-flask-python
# docker run -dp 5000:5000 -w //app -v "%cd%://app" flask-smorest-api
