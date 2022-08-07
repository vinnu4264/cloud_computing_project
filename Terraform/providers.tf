provider "aws" {
  region = "us-east-1" #local.aws_config.region

}

provider "docker" {
  registry_auth {
    address  = local.aws_ecr_registry
    username = data.aws_ecr_authorization_token.token.user_name
    password = data.aws_ecr_authorization_token.token.password
  }
}

provider "google" {
  # Configuration options
}