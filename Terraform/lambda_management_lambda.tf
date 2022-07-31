resource "aws_iam_role" "lambdaiam" {
  name = "lambdaiam"
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
  function_name = "cc_management_lambda"
  role          = aws_iam_role.lambdaiam.arn
  handler       = "index.lambda_handler"
  timeout = "300"
  filename = "${path.module}/python/cc_manage.zip"
  source_code_hash = filebase64sha256("${path.module}/python/cc_manage.zip")

  runtime = "python3.7"
}

data "archive_file" "zip_the_python_code" {
type        = "zip"
source_dir  = "${path.module}/cc_manage/"
output_path = "${path.module}/python/cc_manage.zip"
}
