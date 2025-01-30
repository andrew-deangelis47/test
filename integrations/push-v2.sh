# Example usages
# Only build: ./integrations/push-v2.sh customer-name
# Build and tag: ./integrations/push-v2.sh customer-name testtag
# Build, tag, and push to ECR: ./integrations/push-v2.sh customer-name testtag push
# Note: we are not pushing release images from here

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 431105233043.dkr.ecr.us-east-1.amazonaws.com
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin  public.ecr.aws
echo "Pruning images older than 10 days"
docker system prune -af --filter "until=240h"
CUSTOMER=$1
TAG=$2
PUSH=$3

# 1) build the image
if [ -z "$CUSTOMER" ]
then
  echo "Please pass a customer name. Quitting"
  exit
else
  docker buildx bake customer-"$CUSTOMER"
fi

# 2) tag the image if a tag is passed
if [ -z "$TAG" ]
then
  echo "Image was built locally: integrations/customers/"$CUSTOMER":development"
  exit
else
  docker tag integrations/customers/"$CUSTOMER":development 431105233043.dkr.ecr.us-east-1.amazonaws.com/integrations/customers/"$CUSTOMER":"$TAG"
fi

# 3) push the image, only if push argument exists and equals "push"
if [ -z "$PUSH" ]
then
  echo "No push argument given. Image was built locally and tagged: 431105233043.dkr.ecr.us-east-1.amazonaws.com/integrations/customers/"$CUSTOMER":"$TAG""
  exit
else
  if [ "$PUSH" != "push" ]
  then
      echo "Push argument is not 'push'. Image was built locally and tagged: 431105233043.dkr.ecr.us-east-1.amazonaws.com/integrations/customers/"$CUSTOMER":"$TAG""
      exit
  else
    docker push 431105233043.dkr.ecr.us-east-1.amazonaws.com/integrations/customers/"$CUSTOMER":"$TAG"
    echo "Image was built, tagged, and pushed image to ECR: 431105233043.dkr.ecr.us-east-1.amazonaws.com/integrations/customers/"$CUSTOMER":"$TAG""
  fi
fi