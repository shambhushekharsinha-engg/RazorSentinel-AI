FROM python:3.10-slim

# Install libgomp1 which is required by LightGBM on Linux
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install with no-cache to save memory during build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Generate data and train the model during the build process
RUN python src/data_generator.py && \
    python src/train_verifier.py && \
    python src/evaluate.py

# Expose port 8000
EXPOSE 8000

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"]
