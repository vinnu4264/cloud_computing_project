# Cloud Computing Project

## Folders description
|Folder|Description|
|-|-|
|.github/workflows|Holds github workflow pipeline as code|
|application|Dockerfile with  python code that gets converted to image and stored in AWS-ECR that is used by ECS|
|Terraform| InfrastructureAsCode to provision Lambda, ecr, roles, security groups in AWS |
|Terraform/code| Python code for lambda |
| Scripts | Holds custom scripts written to manage VCS and IAC deployments from local environment |

