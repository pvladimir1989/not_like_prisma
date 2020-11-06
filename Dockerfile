FROM python:3.8

WORKDIR /not_like_prisma

COPY . /not_like_prisma

RUN pip install -r requirements.txt && apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

ENV PYTHONPATH "${PYTHONPATH}:/not_like_prisma"

# CMD ["python", "not_like_prisma/bot.py"]

CMD export FLASK_APP=not_like_prisma && export FLASK_ENV=development && flask run -h 0.0.0.0
