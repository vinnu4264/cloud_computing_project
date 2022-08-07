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

# provider "google" {
#   # Configuration options
# }

provider "vault" {
  token = "hvs.Hfkxg6re5QTY8mK7dzibccGB"
  address = "http://54.86.229.209:8200/"
}