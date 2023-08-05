## Python CI Workflow Documentation

This documentation provides an overview of the Python CI workflow implemented using GitHub Actions.

### Workflow Overview

The Python CI workflow is triggered by two events: pushes to the `main` branch and pull requests targeting the `main` branch. It consists of a single job named `build`, which runs on an `ubuntu-latest` environment.

### Steps

The following steps are executed as part of the workflow:

1. **Checkout code**

   - Name: Checkout code
   - Uses: `actions/checkout@v2`
   - Description: This step checks out the repository code onto the runner.

2. **Setup Python**

   - Name: Setup Python
   - Uses: `actions/setup-python@v2`
   - Description: This step sets up the Python environment for subsequent steps. The Python version used is `3.8`.

3. **Install dependencies**

   - Name: Install dependencies
   - Run: `pip install -r requirements.txt`
   - Description: This step installs the project dependencies by running `pip install` with the requirements specified in the `requirements.txt` file.

4. **Run tests**
   - Name: Run tests
   - Run: `pytest tests`
   - Description: This step executes the test suite by running the `pytest` command with the `tests` directory.
