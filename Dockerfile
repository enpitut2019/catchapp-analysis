FROM sudame/pdfanalyzer
COPY ./ /app
WORKDIR /app
CMD [ "pipenv", "run", "python",  "parse_xhtml.py"]