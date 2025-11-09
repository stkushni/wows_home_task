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

