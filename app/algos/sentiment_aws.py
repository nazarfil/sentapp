import boto3
import json


class AwsClient:
    region = "us-east-2"
    comprehend = boto3.client(service_name='comprehend', region_name=region)
    name = "AWS"

    def get_sentiment(self, text):
        return self.comprehend.detect_sentiment(Text=text, LanguageCode='en')
