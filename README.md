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

## GCLOUD CONFIG
https://cloudcomputingproject-358720.uc.r.appspot.com \
alias gcloud=~/Downloads/google-cloud-sdk/bin/gcloud \
gcloud app logs tail -s default \
gcloud app browse \
gcloud app deploy —quiet

## VAULT Link
http://54.86.229.209:8200/v1/aws/creds/Admin
http://54.86.229.209:8200/v1/secret/credentials/tools/aws
http://54.86.229.209:8200/v1/secret/credentials/tools/gcp

## Manually scale ecs services (Very disruptive)
aws ecs update-service --cluster cc-proj-cluster --service da_container-service --desired-count 0

## Resource planning
1. Website -> GCP, Flask based application (ecs management, graphs, datasheet)
2. IAC -> infra as code. (Lambda, ecs, ecr, security groups, ….) Terraform
3. Functionality
    1. Lambda -> Instant
    2. ECS -> Container service

## Computation idea
Computation
Part1 : Fetching and gathering data. -> GCP application. (shards, history, service)\
Part2 : Performing analysis on data  -> Lambda, ECS (Risk analysis (Portions) )\
Part3 : Display results

## Idea
Data : T1, T100\
		Lambdas  
        -> T1-T51\
		-> T51-T100\
		ECS.           
        -> T1-T51\
				     -> T51-T100


