FROM python:3.10-slim
ARG REQUIREMENTS_FILE=requirements.txt
WORKDIR /app
COPY dependencies/${REQUIREMENTS_FILE} requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "items_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
