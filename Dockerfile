FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/projet_chef_d_oeuvre

COPY requirements.txt /app/projet_chef_d_oeuvre/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000" ]

CMD ["gunicorn", "--chdir", "projet_chef_d_oeuvre", "projet_chef_d_oeuvre.wsgi:application", "--bind", "0.0.0.0:8000"]


# docker build -t projet_chef_d_oeuvre .
# docker run --rm -p 8000:8000 -v $(pwd):/app projet_chef_d_oeuvre
