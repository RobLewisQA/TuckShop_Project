# Use Python 3.6 or later as a base image
FROM python:3.6
# Copy contents into image
COPY . .
# Install pip dependencies from requirements
RUN pip install -r requirements.txt

# Expose the correct port
EXPOSE 5000
# Entry point
ENTRYPOINT ["python", "app.py"]