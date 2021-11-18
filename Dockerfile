FROM python:3.8.0
RUN apt-get update && apt-get install git-lfs
RUN pip3 install --upgrade pip

WORKDIR /app
COPY . /app
RUN git lfs pull -I model/predictions.pkl

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["src/app.py"]