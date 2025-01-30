# Example usages
# Build and don't push: ./integrations/push.sh metalcraft
# Build and push: ./integrations/push.sh pdq2 push

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 431105233043.dkr.ecr.us-west-2.amazonaws.com
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin  public.ecr.aws
echo "Pruning images older than 10 days"
docker system prune -af --filter "until=240h"
CUSTOMER=$1
PUSH=$2
DB=$3
DIR_TO_PRESERVE=$(cat <config.yaml | grep -A1 Paperless | grep dir_to_preserve: | cut -d: -f2 | tr -d ' "')
if [ -z "$DIR_TO_PRESERVE" ]; then
  echo "Are you sure you've added 'dir to preserve' to your config?"
  exit 1
fi
if [ "$PUSH" == "pushrelease" ]; then
  IMAGE_TYPE="release"
else
  IMAGE_TYPE="dev"
fi
if [ "$DB" == "pervasive" ]; then
  DOCKER_PATH="integrations/Dockerfile-Pervasive"
else
  DOCKER_PATH="integrations/Dockerfile"
fi
if [ -z "$CUSTOMER" ]
then
  echo "Please pass a customer name. Quitting"
else
  echo "Copying files and building Docker container"
  # copy all files to new directory except integrations and the secrets files
  rsync -a . ./"${CUSTOMER}_copy" --exclude={'integrations','secrets.ini','secrets_prod2sandbox.ini','secrets_sandbox2sandbox.ini','*.txt'}
  mkdir "${CUSTOMER}_copy"/integrations
  # copy baseintegration into new directory
  rsync -a ./integrations/baseintegration ./"${CUSTOMER}_copy"/integrations
  # copy correct ERP system into new directory
  rsync -a ./integrations/$DIR_TO_PRESERVE ./"${CUSTOMER}_copy"/integrations
  # copy Dockerfile
  if [ "$DB" == "pervasive" ]; then
    rsync -a ./integrations/Dockerfile-Pervasive ./"${CUSTOMER}_copy"/integrations
    rsync -a ./integrations/bash_profile_pervasive ./"${CUSTOMER}_copy"/integrations
  else
    rsync -a ./integrations/Dockerfile ./"${CUSTOMER}_copy"/integrations
  fi
  # copy requirements.txt
  rsync -a ./integrations/requirements.txt ./"${CUSTOMER}_copy"/integrations
  # copy check_connection.py
  rsync -a ./integrations/check_connection.py ./"${CUSTOMER}_copy"/integrations
  # copy database_diff.py
  rsync -a ./integrations/database_diff.py ./"${CUSTOMER}_copy"/integrations
  # copy manage.py
  rsync -a ./integrations/manage.py ./"${CUSTOMER}_copy"/integrations
  cd "${CUSTOMER}_copy" || exit 1
  docker build -t 431105233043.dkr.ecr.us-west-2.amazonaws.com/$CUSTOMER:$IMAGE_TYPE -f $DOCKER_PATH . || exit 1
  if [ -n "$PUSH" ]; then
    docker push 431105233043.dkr.ecr.us-west-2.amazonaws.com/$CUSTOMER:$IMAGE_TYPE || exit 1
  fi
  # delete excess copy dir
  cd ..
  rm -rf "${CUSTOMER}_copy"
fi
