FROM python:bullseye
COPY ../ .
RUN pip install dash
RUN pip install pandas
RUN pip install plotly
RUN pip install geopandas
RUN pip install gunicorn
RUN useradd mike
RUN ["chmod", "+x", "app.py"]
RUN ["chmod", "+x", "wsgi.py"]
EXPOSE 8050
USER mike
ENTRYPOINT gunicorn --bind 0.0.0.0:8050 wsgi