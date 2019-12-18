FROM sudame/pdfanalyzer:latest
COPY ./ /app
WORKDIR /app
CMD [ "pipenv", "run", "python",  "parse_xhtml.py"]