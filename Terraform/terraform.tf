terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.24.0"
    }

    docker = {
      source  = "kreuzwerker/docker"
    }
    
  }
  backend "s3" {
    region = "us-east-1"
    bucket = "cloud-computing-terraform-state-files"
    key    = "stateFiles/terraform.tfstate"
  }
}
