# We're using the latest version of Prefect with Python 3.12
FROM prefecthq/prefect:2-python3.12

# Add our Pipfile to the image and install dependencies
COPY Pipfile* .

RUN pip install pipenv && \
    pipenv install

# Add our flow code to the image
COPY flows /opt/prefect/flows

# Run our flow script when the container starts
CMD ["python", "ml_pipeline.py"]