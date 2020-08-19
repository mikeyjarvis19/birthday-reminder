FROM python:3.8-alpine
RUN apk add --no-cache gcc musl-dev linux-headers
COPY ["README.md", "requirements.txt", "*.py", "./birthday-reminder/"]
WORKDIR "./birthday-reminder"
RUN pip install -r requirements.txt
CMD ["python", "main.py"]