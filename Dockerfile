FROM sudame/pdfanalyzer:latest
COPY ./ /app
WORKDIR /app
RUN pipenv install
CMD [ "pipenv", "run", "python",  "parse_xhtml.py"]