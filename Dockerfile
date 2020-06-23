FROM python:3.8-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
COPY ["main.py", "README.txt", "notifications.py", "control.py", "requirements.txt", "logging_setup.py", "./"]
RUN pip install -r requirements.txt
CMD ["python", "main.py"]