# step_functions.tf

resource "aws_sfn_state_machine" "data_processing_workflow" {
  name     = "data-processing-workflow"
  role_arn = aws_iam_role.step_functions_role.arn

  definition = jsonencode({
    Comment = "Data Processing Workflow"
    StartAt = "FileValidation"
    States = {
      FileValidation = {
        Type     = "Task"
        Resource = aws_lambda_function.file_validation.arn
        Next     = "DataProcessing"
        Catch = [{
          ErrorEquals = ["States.ALL"]
          Next        = "FailState"
        }]
      }
      DataProcessing = {
        Type     = "Task"
        Resource = aws_lambda_function.data_processing.arn
        End      = true
        Catch = [{
          ErrorEquals = ["States.ALL"]
          Next        = "FailState"
        }]
      }
      FailState = {
        Type  = "Fail"
        Cause = "Data Processing Failed"
      }
    }
  })
}

resource "aws_iam_role" "step_functions_role" {
  name = "step_functions_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "states.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "step_functions_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaRole"
  role       = aws_iam_role.step_functions_role.name
}