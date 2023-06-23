FROM python

WORKDIR /bn

COPY requirements.txt .

RUN python -m venv venv

RUN /bin/bash -c "source venv/bin/activate"

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY templates/ templates/ 

EXPOSE 5000

CMD ["python3", "app.py"]
# CMD ["/bin/bash", "-c", "source venv/bin/activate && python app.py"]

# Note: mac is running out of memody and 'back to the winter' we are out of light. Still hace some problem with an image, it runs but can`t execute html