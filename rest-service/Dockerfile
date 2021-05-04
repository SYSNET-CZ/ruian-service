FROM python:3
MAINTAINER Radim Jager "rjaeger@sysnet.cz"
COPY .. /opt/geoservice
WORKDIR /opt/geoservice
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENV POSTGIS_HOST=postgis
ENV POSTGIS_PORT=5432
ENV RUIAN_DATABASE=ruian
ENV POVODI_DATABASE=povodi
ENV MAPY_DATABASE=mapy
ENV POSTGIS_USER=docker
ENV POSTGIS_PASSWORD=docker
ENV RESOURCE_PREFIX=geoapi
ENV FLASK_ENV=development
# ENV FLASK_ENV=production
ENV FLASK_APP=app.py
EXPOSE 5000
# ENTRYPOINT ["python"]
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000"]
