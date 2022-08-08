# Cloud Computing Project

## Folders description
|Folder|Description|
|-|-|
|.github/workflows|Holds github workflow pipeline as code|
|application|Dockerfile with  python code that gets converted to image and stored in AWS-ECR that is used by ECS|
|Terraform| InfrastructureAsCode to provision Lambda, ecr, roles, security groups in AWS |
|Terraform/code| Python code for lambda |
| Scripts | Holds custom scripts written to manage VCS and IAC deployments from local environment |
|Website| Holds the website related code. Website is built using the Python Flask module|

## Deploying web application to GCloud App Engine
- Install gcloud 
    - Download and install Gcloud CLI from https://cloud.google.com/sdk/docs/install
    - `alias gcloud=~/Downloads/google-cloud-sdk/bin/gcloud` (optional)
- Go to Website folder
- initialize project with `gcloud init`
    - Follow the process of logging and setting up gcloud access
- run `gcloud app deploy`