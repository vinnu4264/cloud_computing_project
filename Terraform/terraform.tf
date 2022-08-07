terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.24.0"
    }

    docker = {
      source = "kreuzwerker/docker"
    }

    # google = {
    #   source = "hashicorp/google"
    #   version = "4.31.0"
    # }

    vault = {
      source = "hashicorp/vault"
      version = "3.8.1"
    }

  }
  backend "s3" {
    region = "us-east-1"
    bucket = "cloud-computing-terraform-state-files"
    key    = "stateFiles/terraform.tfstate"
  }
}
