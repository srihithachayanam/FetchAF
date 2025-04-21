# GitHub Actions Workflows

This directory contains GitHub Actions workflows that automate various aspects of the development, testing, and deployment processes.

## Available Workflows

### 1. Python Application CI (`python-app.yml`)

**Triggers:** Push to main/master branches, Pull requests to main/master

**Purpose:** This workflow validates the Python application by:

- Setting up a PostgreSQL service container for testing
- Installing dependencies
- Running linting with flake8
- Executing Python import test

### 2. Docker Image CI/CD (`docker-publish.yml`)

**Triggers:** Push to main/master branches, Tagged releases (v\*), Pull requests to main/master

**Purpose:** This workflow builds and publishes Docker images:

- Builds the Docker image from the Dockerfile
- Publishes the image to GitHub Container Registry (ghcr.io) when pushed to main/master
- Tags images with branch name, PR number, version tags, and SHA

### 3. Dependency Review (`dependency-review.yml`)

**Triggers:** Pull requests to main/master

**Purpose:** This workflow checks dependencies for security issues:

- Reviews dependencies for vulnerabilities when dependencies change
- Runs Bandit security scanner to detect common security issues
- Checks for known vulnerabilities in Python dependencies with Safety

### 4. Deployment (`deploy.yml`)

**Triggers:** Manual dispatch, Push to main/master (excluding changes to markdown and workflow files)

**Purpose:** This workflow deploys the application to a server:

- Sets up SSH connection to the deployment server using SSH keys
- Creates `.env` file with secrets from GitHub
- Copies code to the server via rsync
- Rebuilds and restarts Docker containers on the server

## Required Secrets

The following secrets need to be configured in your GitHub repository settings:

- `COHERE_API_KEY`: API key for Cohere
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database hostname
- `DB_PORT`: Database port
- `DB_NAME`: Database name
- `SSH_PRIVATE_KEY`: SSH private key for deployment
- `SERVER_HOST`: Hostname of the deployment server
- `SERVER_USER`: Username for the deployment server
- `SERVER_PATH`: Path on the server where the application should be deployed

## Manual Workflow Dispatch

The deployment workflow can be triggered manually through the GitHub Actions UI:

1. Go to the "Actions" tab in your repository
2. Select the "Deploy" workflow
3. Click "Run workflow"
4. Select the branch to deploy
5. Click "Run workflow" to start the deployment

## Local Workflow Testing

To test workflows locally before pushing, you can use [act](https://github.com/nektos/act):

```bash
# Install act (macOS)
brew install act

# Run a specific workflow
act -W .github/workflows/python-app.yml

# Run a workflow with specific event
act push -W .github/workflows/deploy.yml
```

## Workflow Maintenance

When adding new dependencies or changing the application structure, remember to update the workflows accordingly:

- Add new environment variables to both the workflows and repository secrets
- Update test commands if testing strategy changes
- Modify Docker build steps if the Dockerfile or build process changes
