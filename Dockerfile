FROM python:3.9 as dev
WORKDIR /usr/src/app
COPY . ./
RUN pip install pipenv
RUN pipenv install --dev
EXPOSE 5000
ENTRYPOINT ["pipenv"]
CMD ["run", "flask", "run", "--host=0.0.0.0", "--port=5000"]