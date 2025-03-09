FROM apache/airflow:2.10.5-python3.12

# Set root user temporarily to install packages in correct location
USER root

# Set an installation directory accessible to the Airflow user
ENV AIRFLOW_HOME=/opt/airflow
ENV PIP_TARGET=$AIRFLOW_HOME/.local

# Copy the dependencies file
COPY requirements.txt /requirements.txt

# Install dependencies in the correct directory
RUN pip3 install --no-cache-dir -r /requirements.txt --target $PIP_TARGET

# Check if the package was installed
RUN pip3 show apache-airflow-providers-postgres

# Set PYTHONPATH after installing dependencies
ENV PYTHONPATH=$PIP_TARGET:$PYTHONPATH

# Returns to the default Airflow user
USER airflow
