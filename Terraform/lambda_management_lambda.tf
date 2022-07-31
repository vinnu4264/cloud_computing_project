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
  handler       = "cc_manage_lambda.main.lambda_handler"
#   layers = [ aws_lambda_layer_version.common_lambda_layer.id ]
  timeout = "300"
  filename = "./bin/cc_manage_lambda.zip"
  source_code_hash = filebase64sha256("./bin/cc_manage_lambda.zip")

  runtime = "python3.7"

  environment {
    variables = {
      foo = "bar"
    }
  }
}