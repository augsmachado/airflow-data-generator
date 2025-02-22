# Usa a imagem oficial do Airflow
FROM apache/airflow:2.10.5-python3.12

# Define usuário root temporariamente para instalar pacotes no local correto
USER root

# Define um diretório de instalação acessível ao usuário airflow
ENV AIRFLOW_HOME=/opt/airflow
ENV PIP_TARGET=$AIRFLOW_HOME/.local
ENV PYTHONPATH=$PIP_TARGET:$PYTHONPATH

# Copia o arquivo de dependências
COPY requirements.txt /requirements.txt

# Instala as dependências no diretório correto
RUN pip3 install --no-cache-dir -r /requirements.txt --target $PIP_TARGET

# Verifica se o pacote foi instalado
RUN pip3 show apache-airflow-providers-postgres

# Retorna para o usuário padrão do Airflow
USER airflow
