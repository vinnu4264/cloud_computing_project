data "archive_file" "zip_the_python_code" {
  type        = "zip"
  source_file = "${path.module}/code/lambda_function.py"
  output_path = "nametest.zip"
}