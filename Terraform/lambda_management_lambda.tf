resource "aws_iam_role" "lambdaiam" {
  name               = "lambdaiam"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "cc_management_lambda" {
  function_name    = "cc_management_lambda"
  role             = aws_iam_role.lambdaiam.arn
  handler          = "lambda_function.lambda_handler"
  timeout          = "300"
  filename         = "management_lambda.zip"
  source_code_hash = data.archive_file.zip_the_python_code.output_base64sha256
  runtime          = "python3.7"

  environment {
    variables = {
      VAULT_TOKEN = data.vault_generic_secret.secret_data.data["access_key"]
      VAULT_URL   = var.VAULT_URL
    }
  }

}

