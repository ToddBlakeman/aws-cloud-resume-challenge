resource "aws_lambda_function" "myfunc" {
  filename         = data.archive_file.zip.output_path
  source_code_hash = data.archive_file.zip.output_base64sha256
  function_name    = "myfunc"
  role             = aws_iam_role.lamba_role.arn
  handler          = "func.handler"
  runtime          = "python3.9"
}

resource "aws_iam_role" "lamba_role" {
  name = "lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })

  tags = {
    project = "aws-cloud-resume-challenge"
  }
}

resource "aws_iam_policy" "iam_policy_for_lambda_role" {
  name        = "aws_iam_policy_for_lambda_role"
  path        = "/"
  description = "AWS IAM Policy for the lambda_role"
  policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Sid" : "ReadWriteTable",
          "Effect" : "Allow",
          "Action" : [
            "dynamodb:BatchGetItem",
            "dynamodb:GetItem",
            "dynamodb:Query",
            "dynamodb:Scan",
            "dynamodb:BatchWriteItem",
            "dynamodb:PutItem",
            "dynamodb:UpdateItem"
          ],
          "Resource" : "arn:aws:dynamodb:*:*:table/view-count-ddb"
        },
        {
          "Sid" : "GetStreamRecords",
          "Effect" : "Allow",
          "Action" : "dynamodb:GetRecords",
          "Resource" : "arn:aws:dynamodb:*:*:table/view-count-ddb/stream/* "
        },
        {
          "Sid" : "WriteLogStreamsAndGroups",
          "Effect" : "Allow",
          "Action" : [
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ],
          "Resource" : "*"
        },
        {
          "Sid" : "CreateLogGroup",
          "Effect" : "Allow",
          "Action" : "logs:CreateLogGroup",
          "Resource" : "*"
        }
      ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_iam_policy_for_lambda_role_to_lambda_role" {
  role       = aws_iam_role.lamba_role.name
  policy_arn = aws_iam_policy.iam_policy_for_lambda_role.arn
}

data "archive_file" "zip" {
  type        = "zip"
  source_dir  = "${path.module}/lambda/"
  output_path = "${path.module}/packedlambda.zip"
}

resource "aws_lambda_function_url" "url1" {
  function_name      = aws_lambda_function.myfunc.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = ["https://www.toddblakeman.co.uk"]
    allow_methods     = ["*"]
    allow_headers     = ["date", "keep-alive"]
    expose_headers    = ["keep-alive", "date"]
    max_age           = 86400
  }
}