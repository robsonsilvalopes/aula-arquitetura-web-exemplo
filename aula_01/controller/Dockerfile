### PALANTIR Project (PM-MT/SESP, Fapemat and UFMT)
###
### Docker file to CONTROLLER module.
###
### __auth__="Maxweel Carmo"
### __date__="dd/04/2021"
### ver: 0.1

#FROM python:3.8-slim
FROM python:3.9
ENV APP_HOME /code
WORKDIR $APP_HOME
COPY requirements.txt requirements.txt
# Install requirements in to root user directory (/root/.local)
# (prevent that requirements are installed at each building, taking advantage of container layers already built)
RUN pip install --user -r requirements.txt
ENV PATH=/root/.local/bin:$PATH
COPY . ./
#RUN pip install -r requirements.txt

# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app.main:app
# CMD flask run
# ENTRYPOINT ["sh", "-c", "sleep 2073600"]