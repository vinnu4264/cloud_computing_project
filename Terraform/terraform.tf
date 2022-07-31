terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.24.0"
    }
  }
}

provider "aws" {
  # access_key = local.aws_config.access_key
  region = "us-east-1"#local.aws_config.region
  # secret_key = local.aws_config.secret_key
  
}