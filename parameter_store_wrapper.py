import boto3

ssm_client = boto3.client('ssm')
ssm_client.get_parameter(Name="environment")
