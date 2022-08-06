variable "region" {
  default = "us-east-1"
}

variable "vpc_id" {
  default = "vpc-04b730416f7b93064"
}

variable "VAULT_TOKEN" {}

variable "VAULT_URL" {
  default = "http://54.86.229.209:8200/v1/credentials/tools/aws"
}
