# Contributing to CyberGenie

Thank you for considering contributing to CyberGenie! We welcome contributions from the community to help improve the project. This document provides guidelines for contributing to the project, including coding standards, commit message conventions, and the process for submitting pull requests.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Coding Standards](#coding-standards)
3. [Commit Message Conventions](#commit-message-conventions)
4. [Submitting Pull Requests](#submitting-pull-requests)
5. [Code of Conduct](#code-of-conduct)

## Getting Started

To get started with contributing to CyberGenie, follow these steps:

1. **Fork the repository:**
   - Go to the [CyberGenie repository](https://github.com/canstralian/CyberGenie) on GitHub.
   - Click the "Fork" button to create a copy of the repository in your GitHub account.

2. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/CyberGenie.git
   cd CyberGenie
   ```

3. **Create a new branch:**
   ```sh
   git checkout -b your-branch-name
   ```

4. **Set up the development environment:**
   - Follow the instructions in the `README.md` file to set up the development environment, install dependencies, and configure the application.

5. **Make your changes:**
   - Implement your changes, following the coding standards and guidelines provided in this document.

6. **Run tests:**
   - Ensure that all tests pass by running the test suite.
   ```sh
   pytest
   ```

## Coding Standards

To maintain a consistent codebase, please adhere to the following coding standards:

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code.
- Use meaningful variable and function names.
- Write clear and concise docstrings for all functions and classes.
- Use type annotations for function signatures and variables.
- Keep lines of code within 88 characters.
- Use a linter, such as `flake8`, to check for code style issues.
- Use `black` for code formatting. To format your code, run the following command:
  ```sh
  black .
  ```

## Commit Message Conventions

Please follow these conventions for commit messages:

- Use the present tense ("Add feature" not "Added feature").
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...").
- Limit the subject line to 50 characters.
- Capitalize the subject line.
- Do not end the subject line with a period.
- Separate the subject from the body with a blank line.
- Use the body to explain what and why vs. how.

## Submitting Pull Requests

To submit a pull request, follow these steps:

1. **Push your changes to your forked repository:**
   ```sh
   git push origin your-branch-name
   ```

2. **Create a pull request:**
   - Go to the [CyberGenie repository](https://github.com/canstralian/CyberGenie) on GitHub.
   - Click the "New pull request" button.
   - Select your branch from the "compare" dropdown.
   - Provide a clear and descriptive title for your pull request.
   - Describe the changes you have made and the purpose of the pull request.
   - Click "Create pull request" to submit your changes for review.

3. **Address feedback:**
   - Be responsive to feedback and make any necessary changes to your pull request.
   - Once your pull request is approved, it will be merged into the main branch.

4. **Review process:**
   - Ensure all pull requests are reviewed by at least one other team member before being merged. This helps to catch potential issues and maintain code quality.

## Code of Conduct

We expect all contributors to adhere to the [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand the expectations for behavior when contributing to the project.

Thank you for your contributions and for helping to improve CyberGenie!
