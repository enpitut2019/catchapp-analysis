FROM sudame/pdfanalyzer:latest
COPY Pipfile parse_xhtml.py Pipfile.lock /app/
WORKDIR /app
ENV PIPENV_VENV_IN_PROJECT=1 LD_LIBRARY_PATH=/usr/local/lib
RUN pipenv install
CMD [ "pipenv", "run", "python",  "parse_xhtml.py"]