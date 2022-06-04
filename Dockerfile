# 
FROM python:3.9

# 
WORKDIR /src

# 
COPY ./requirements.txt ./

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
