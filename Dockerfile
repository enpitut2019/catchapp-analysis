FROM sudame/pdfanalyzer:latest
COPY ./ /app
WORKDIR /app
ENV PIPENV_VENV_IN_PROJECT=1
RUN pipenv install
CMD [ "pipenv", "run", "python",  "parse_xhtml.py"]