import boto3
import json


class AwsClient:
    region = "us-east-2"
    comprehend = boto3.client(service_name='comprehend', region_name=region)

    def get_sentiment(self, text):
        print('Calling DetectSentiment')
        print(json.dumps(self.comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
        print('End of DetectSentiment\n')
