FROM python:3.12
EXPOSE 5000
WORKDIR /app
COPY ./requirement.txt requirement.txt
RUN pip install --no-cache-dir --upgrade -r requirement.txt
COPY . .
CMD [ "flask","run","--host","0.0.0.0" ]