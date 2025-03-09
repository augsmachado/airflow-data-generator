# Airflow Data Generator

## Overview

This project, Airflow Data Generator, demonstrates how to orchestrate data generation and processing tasks using Apache Airflow and PostgreSQL. It leverages a multi-container Docker setup for easy deployment and management. The project includes:

-   **Airflow DAGs**: Defines workflows for data generation and processing, including connections to multiple PostgreSQL databases. Currently, the dual_postgres_dag.py DAG demonstrates querying two separate Postgres databases.
-   **PostgreSQL Integration**: Uses PostgreSQL as the backend database for Airflow metadata and also includes multiple Postgres containers for demonstrating data interaction with different databases.
-   **Dockerized Environment**: Utilizes Docker Compose to manage the multi-container environment, including Airflow, PostgreSQL (for Airflow metadata), and additional PostgreSQL instances for data processing.
-   **Automated Build Process**: Includes a Makefile for streamlined building and running of the Docker environment.

The project aims to provide a practical example of how to use Airflow to orchestrate data-related tasks, interact with multiple databases, and manage the entire process within a containerized environment. It serves as a starting point for building more complex data pipelines and workflows. Future development may include more sophisticated data generation tasks, data transformation logic, and integration with other data processing tools.

## 🚀 Features

-   Airflow orchestration
-   PostgreSQL database integration
-   Metabase data visualization tool
-   Dynamic table creation and population: Create and populate tables based on JSON table definitions, allowing for flexible data generation.

## 🛠 Tech Stack

-   Python: 3.12
-   PostgreSQL: 15
-   Airflow: 2.10.5
-   Metabase: 0.53.5.4
-   Docker: 4.38.0

## 📦 Prerequisites

-   Python 3.12+
-   PostgreSQL 15
-   Airflow 2.10.5
-   Docker Hub
-   Docker Compose
-   pip

## 🔧 Installation

### 1. Clone Repository

```bash
git clone https://github.com/augsmachado/airflow-data-generator.git
cd airflow-data-generator
```

### 🚦 Running the Application

You can use the `make docker-init` command or execute

```bash
chmod +x ./scripts/setup_metabase_db.sh
docker compose up -d || exit 1
for db in postgres1 postgres2; do \
    while ! docker compose exec -T $$db pg_isready -U usr$${db:7} -d db$${db:7}; do \
    	sleep 1; \
    done \
done
docker compose run --rm postgres1 /bin/bash -c "./scripts/setup_metabase_db.sh" || exit 1
```

To verify if containers are running, you can use the `make docker-verify` command or execute

```bash
docker ps
```

### 🔍 Testing

You can use the `make python-test` command or execute

```bash
pytest
```

### 🔐 Security

-   CodeQL analysis integrated
-   Dependabot for dependency updates
-   Regular security scans

### 🤝 Contributing

Feel free to submit issues or pull requests for improvements or bug fixes. Use the framework below:

-   Fork the repository
-   Create your feature branch
-   Commit your changes
-   Push to the branch
-   Create a Pull Request

### 📄 License

This project is licensed under the Apache License 2.0.
See the LICENSE file for details.
