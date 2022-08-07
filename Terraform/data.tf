data "aws_caller_identity" "current" {}

data "aws_ecr_authorization_token" "token" {}

data "archive_file" "zip_the_python_code" {
  type        = "zip"
  source_file = "${path.module}/code/lambda_function.py"
  output_path = "management_lambda.zip"
}

data "aws_vpc" "this" {
  id = var.vpc_id
}

# data "aws_subnet_ids" "this" {
#   vpc_id = data.aws_vpc.this.id
# }

# data "vault_generic_secret" "secret_data" {
#   path = "aws/creds/Admin"
# }

data "vault_generic_secret" "secret_data" {
  path = "credentials/tools/aws"
}

data "vault_generic_secret" "gcp_creds" {
  path = "credentials/tools/gcp"
}




