FROM python:3

WORKDIR /bn

COPY requirements.txt .

# RUN python -m venv venv

# RUN /bin/bash -c "source venv/bin/activate"

RUN pip install -r requirements.txt

COPY . .

# COPY templates/ templates/ 

EXPOSE 5000
# ENV FLASK_APP=app.py

# ENTRYPOINT [ "flask" ]
# CMD ["run", '--host', "0.0.0.0"]

CMD ["python", "app.py"]
# CMD ["/bin/bash", "-c", "source venv/bin/activate", "python && app.py"]

# Note: mac is running out of memory and 'back to the winter' we are out of light. Still have some problem with an image, it runs but can`t execute html