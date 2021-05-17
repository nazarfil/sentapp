import boto3

from app import Config


class AwsClient:
    name = "AWS"

    def __init__(self, region="us-east-2"):
        config = Config()
        """
        :type region: string
        """
        if config.USE_FOREIGN_AWS:
            self.comprehend = boto3.client(service_name='comprehend',
                                           aws_access_key_id=config.AWS_ACCESS_KEY,
                                           aws_secret_access_key=config.AWS_SECRET_KEY,
                                           region_name=region)
        else:
            self.comprehend = boto3.client(service_name='comprehend',
                                           region_name=region)

    def get_sentiment(self, text):
        """

        :type text: string
        """
        return self.comprehend.detect_sentiment(Text=text, LanguageCode='en')
