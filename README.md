# Home-Budget-Service
Backend service of the Home Budget App

## Python + FastAPI
Project is done with FastAPI framework that is based on python.

## How to start this project

### 1. First create .venv environment

Use your editor suggestions to create venv folder inside the root of the project.
In case of PyCharm follow instructions: [PyCharm venv setup](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html) 

In case you use VSCode please follow instructions: [VSCode venv setup](https://code.visualstudio.com/docs/python/environments)

### 2. Install requirements

Requirements are listed in ``requirements/requirements.txt``. To install them run 

`pip install -r requirements/requirements.txt`

### 3. Environment Configuration

To set up the environment configuration for **development**, follow these steps:

1. Locate the `.env.example` file in the `app/` folder.

2. Copy and rename the file as:
   - `.env` for **development**:

3. The default configuration is already set up for local development

4. (Optional) Adjust values in the `.env` file if needed

### 4. Database 

Project requires PostgreSQL for data storage.

**Option A: Use existing PostgreSQL installation**
If you already have PostgreSQL installed and running on your system, you can use it directly.

**Option B: Use Docker (recommended)**
If you don't have PostgreSQL installed, or prefer an isolated environment, use Docker:

#### Docker Setup
To set up the database, execute the following command:

`docker-compose -f deploy/local/db-docker-compose.yml up -d`

This starts:
  * PostgreSQL database (port 5444)