FROM python:3.11-slim

# Install necessary libraries
RUN pip install pandas scikit-learn numpy

# Copy the predictive maintenance script
COPY predictive_maintenance.py /app/predictive_maintenance.py

# Set the working directory
WORKDIR /app

# Run the predictive maintenance script
CMD ["python", "predictive_maintenance.py"]
