FROM python:3.9
ENV APP_HOME /code
WORKDIR $APP_HOME
COPY ./wk_math/requirements.txt requirements.txt
# Install requirements in to root user directory (/root/.local)
# (prevent that requirements are installed at each building, taking advantage of container layers already built)
RUN pip install --user -r requirements.txt
ENV PATH=/root/.local/bin:$PATH
COPY ./wk_math/app $APP_HOME/app