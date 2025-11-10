# wows_home_task

## Overview

**wows_home_task** is a test automation project designed to verify two main database error scenarios:  
1. Invalid component entries  
2. Incorrect component parameter values  

To improve test result readability and reporting, **Allure** integration has been added.
For better readability, all database operations have been moved into dedicated service classes.
---

## Installation and Setup

### 1. Create a Virtual Environment
Create a Python 3.8 virtual environment and activate it:

```bash
python3.8 -m venv venv
source venv/bin/activate   # On Linux/macOS
venv\Scripts\activate      # On Windows
```

### 2. Install Dependencies
Install all required Python packages:

```bash
pip install -r requirements.txt
```

### 3. Prepare the Database
Create the database by running:

```bash
python create_db.py
```

### 4. Populate the Database
Insert initial test data:

```bash
python populate_db.py
```

---

## Running Tests

### Run Tests Without Allure Report
You can execute tests directly with:

```bash
pytest -v
```

### Run Tests With Allure Report Generation
To generate Allure results, use:

```bash
pytest --alluredir=allure-results
```

---

## Docker: One-Command Test Environment

The repository ships with a Docker image that prepares the database, installs all
dependencies (including the Allure CLI + JRE) and leaves you inside the
container after the initial test run so you can inspect reports or rerun tests.

### 1. Build the Image

```bash
docker build -t wows-tests .
```

### 2. Run the Container Interactively

```bash
docker run -it --name wows-tests-run -p 5050:5050 wows-tests
```

What happens automatically on first start:

1. The SQLite database is recreated and populated inside the container
   (`/app/db/world_of_warships.db`).
2. `pytest -v --alluredir=/app/allure-results` is executed.
3. When tests finish, the exit code is written to `/tmp/pytest_exit_code`, and an
   interactive shell opens instead of terminating the container. This lets you:
   - rerun tests (`pytest`, `pytest -k ...`, etc.);
   - view the stored exit code: `cat /tmp/pytest_exit_code`;
   - generate and serve the Allure report.

> 💡 If you need the container to stop immediately after the command, launch it
> with `-e KEEP_CONTAINER_ALIVE=0`.

### 3. View the Allure Report (Optional)

Inside the interactive shell execute:

```bash
allure serve /app/allure-results --host 0.0.0.0 --port 5050
```

The command exposes the report on http://localhost:5050 thanks to the `-p 5050:5050`
port mapping from step 2.

### 4. Rerun Tests Later

Reattach to the container (if it is still running) with:

```bash
docker exec -it wows-tests-run bash
```

Then run `pytest` commands as needed. When you are done, exit the shell with
`exit` and stop the container:

```bash
docker stop wows-tests-run
```

To start from scratch, remove the stopped container:

```bash
docker rm wows-tests-run
```

---

## Viewing the Allure Report

### 1. Install Allure and JRE
To view the generated report, you need to have **Java Runtime Environment (JRE)** and **Allure** installed locally.

- [Install JRE](https://www.oracle.com/java/technologies/javase-jre8-downloads.html)  
- [Install Allure](https://docs.qameta.io/allure/#_installing_a_commandline)

### 2. Serve the Allure Report
Once installed, from the project root run:

```bash
allure serve allure-results
```

Allure will generate and open the report in your default web browser.

---

## Notes

- Ensure that your database is running and accessible before executing tests.  
- Adjust database connection parameters in the configuration file if required.  
- The project is compatible with **Python 3.8** and newer.

---

**Author:** *Sergei Kushnir*

