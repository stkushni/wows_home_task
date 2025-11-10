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

The repository ships with a Docker image (based on `python:3.8-slim`) that
prepares the database, installs all dependencies (including the Allure CLI +
JRE) and leaves you inside the container after the initial test run so you can
inspect reports or rerun tests.

### Install Docker (if needed)

Follow the official instructions for your OS if Docker Engine/Desktop is not yet
available locally:

| Platform | Documentation |
| --- | --- |
| Linux | [docs.docker.com/engine/install](https://docs.docker.com/engine/install/) |
| macOS | [docs.docker.com/desktop/install/mac-install](https://docs.docker.com/desktop/install/mac-install/) |
| Windows | [docs.docker.com/desktop/install/windows-install](https://docs.docker.com/desktop/install/windows-install/) |

> ℹ️ After installing Docker Desktop (macOS/Windows) remember to start the
> application once so that the Docker daemon is running before you continue.

### Step-by-step workflow

1. **Build the image** (run from the project root):
   ```bash
   docker build -t wows-tests .
   ```
2. **Start an interactive container** that exposes the Allure server port and
   keeps running after the first test execution:
   ```bash
   docker run -it --name wows-tests-run -p 5050:5050 wows-tests
   ```
   On first boot the entrypoint will automatically:
   - recreate and populate `/app/db/world_of_warships.db`;
   - execute `pytest -v --alluredir=/app/allure-results`;
   - store the pytest exit status in `/tmp/pytest_exit_code` and drop you into a
     shell instead of terminating the container so you can inspect results.

   > 💡 Want the container to exit immediately after the command finishes? Add
   > `-e KEEP_CONTAINER_ALIVE=0` to the `docker run` command.
3. **Serve the Allure report** (optional) directly from the running container:
   ```bash
   allure serve /app/allure-results --host 0.0.0.0 --port 5050
   ```
   Visit http://localhost:5050 in your browser to view the report (the `-p
   5050:5050` flag from the previous step forwards the port).
4. **Rerun tests or inspect artifacts** at any time while the container is
   running. Execute additional `pytest` commands, open the saved exit code via
   `cat /tmp/pytest_exit_code`, or explore generated files under `/app`.
5. **Reconnect later** if you detached from the session while the container is
   still running:
   ```bash
   docker exec -it wows-tests-run bash
   ```
   When finished, exit the shell (`exit`) and stop the container:
   ```bash
   docker stop wows-tests-run
   ```
   To clean everything up and start over, remove the stopped container:
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

