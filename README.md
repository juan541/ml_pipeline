# ML Pipeline with Prefect

This repository contains an example of utilizing Prefect for managing machine learning workflows. The project is implemented in Python 3.12. The main entry point for the workflow is `ml_pipeline.py`.
It's a good starting point for the platform.

## Table of Contents
- [Introduction](#introduction)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Submitting Snowflake Credentials](#submitting-snowflake-credentials)
- [License](#license)

## Introduction
This project demonstrates the use of Prefect for orchestrating and managing ML workflows. The main file, `ml_pipeline.py`, defines the workflow and its components. Prefect provides a powerful, open-source platform to help you manage your workflows with ease and reliability.

## Setup

### Prerequisites
- Python 3.12
- `pipenv` for package management

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/ml-workflow-prefect.git
   cd ml-workflow-prefect
   ```

2. Install the dependencies using `pipenv`:
   ```bash
   pipenv install
   ```

## Usage

To run the main workflow, execute the following command:
```bash
python ml_pipeline.py
```

Ensure that you have configured any necessary environment variables or configuration files as required by your specific workflow components.

## Submitting Snowflake Credentials

To connect to your Snowflake account for downloading data, you need to provide your Snowflake credentials. These credentials should be stored in a `.env` file in the root directory of the project. The required variables are:

- `SN_USERNAME`: Your Snowflake username
- `SN_PASSWORD`: Your Snowflake password
- `SN_ACCOUNT`: Your Snowflake account identifier
- `SN_WAREHOUSE`: Your Snowflake warehouse identifier
- `SN_DB`: Your Snowflake target database
- `SN_ROLE`: Your Snowflake role


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.