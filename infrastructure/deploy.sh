docker build -t flask/sentapp .
docker tag flask/sentapp:latest 333094945036.dkr.ecr.us-east-2.amazonaws.com/sentapp:latest
aws-vault exec us-east
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 333094945036.dkr.ecr.us-east-2.amazonaws.com
docker push 333094945036.dkr.ecr.us-east-2.amazonaws.com/sentapp