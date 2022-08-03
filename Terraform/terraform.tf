terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.24.0"
    }
  }
  backend "s3" {
    bucket = "cloud-computing-terraform-state-files"
    key    = "stateFiles/terraform.tfstate"
  }
}
