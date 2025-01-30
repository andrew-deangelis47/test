#!/bin/bash
# This is a script which can be run either locally or on a PPMC to pull the latest image down from AWS and run the integration
# Please change the value of "customer" at the beginning of the shell script to whatever your AWS ECR repository name is# Example runs
# Command for running import sandbox to sandbox: ./repeat_work_starter_icc.sh CUSTOMER="momentum" IMAGE_TAG="dev" ENV="sandbox2sandbox"
# Command for running import prod to prod: ./repeat_work_starter_icc.sh CUSTOMER="podium" IMAGE_TAG="dev" ENV="prod"

# parses command line arguments in the form of ARGUMENT="VALUE"
for ARGUMENT in "$@"
do

    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)

    case "$KEY" in
      CUSTOMER)              CUSTOMER=${VALUE} ;;
      IMAGE_TAG)              IMAGE_TAG=${VALUE} ;;
      ENV)    ENV=${VALUE} ;;
      DEBUG)    DEBUG=${VALUE} ;;
      ROOT_DIR)    ROOT_DIR=${VALUE} ;;
            *)
    esac
done

if [ -z "$ROOT_DIR" ]; then
  ROOT_DIR="/usr/bin/paperless"
  echo "Root directory not set defaulting to $ROOT_DIR"
fi

# Print variables
echo "Customer is $CUSTOMER"
echo "Image is $IMAGE_TAG"
echo "Environment is $ENV"
echo "Root dir is $ROOT_DIR"
echo "Debug is $DEBUG"

KERNEL_NAME="$(uname -s)"
OLD_CONFIG=~/.docker/config.json
if [ "$KERNEL_NAME" == "Darwin" ]; then
  echo "Mac detected, not removing old Docker config"
elif test -f "$OLD_CONFIG"; then
  echo "Removing old Docker config to avoid bug"
  rm ~/.docker/config.json
fi

# Either bind the prod config or the sandbox config
if [ "$ENV" == "prod" ]; then
  SECRETS_FILENAME="secrets.ini"
elif [ "$ENV" == "prod2sandbox" ]; then
  SECRETS_FILENAME="secrets_prod2sandbox.ini"
elif [ "$ENV" == "sandbox2sandbox" ]; then
  SECRETS_FILENAME="secrets_sandbox2sandbox.ini"
else
  echo "Did not recognize env. Please try again"
  exit 1
fi
OUT_SECRETS_FILENAME="secrets.ini"

echo "Logging into ECR"
RAW_AWS_KEY=$(awk -F "=" '/aws_access_key/ {print $2}' $ROOT_DIR/icc/connector/$CUSTOMER/$SECRETS_FILENAME)
export AWS_ACCESS_KEY_ID=${RAW_AWS_KEY//[$'\t\r\n ']}
RAW_AWS_SECRET=$(awk -F "=" '/aws_secret_key/ {print $2}' $ROOT_DIR/icc/connector/$CUSTOMER/$SECRETS_FILENAME)
export AWS_SECRET_ACCESS_KEY=${RAW_AWS_SECRET//[$'\t\r\n ']}
export AWS_DEFAULT_REGION="us-west-2"
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 431105233043.dkr.ecr.us-west-2.amazonaws.com 2>&1

echo "Pruning images older than 10 days"
docker system prune -af --filter "until=240h"
RAW_CUSTOMER_SLUG=$(awk -F "=" '/customer_slug/ {print $2}' $ROOT_DIR/icc/connector/$CUSTOMER/$SECRETS_FILENAME)
CUSTOMER_SLUG=${RAW_CUSTOMER_SLUG//[$'\t\r\n ']}

IMAGE_HOST="431105233043.dkr.ecr.us-west-2.amazonaws.com"
IMAGE_NAME="${IMAGE_HOST}/$CUSTOMER:$IMAGE_TAG"
FALLBACK_IMAGE_NAME="${IMAGE_HOST}/$CUSTOMER_SLUG:$IMAGE_TAG"

if [ "$IMAGE_TAG" == "dev" ]; then
  echo "Pulling down latest dev image"
fi

if [ "$IMAGE_TAG" == "dev" ] || [ "$IMAGE_TAG" == "release" ]; then
  # Pull down latest image
  docker pull ${IMAGE_NAME} 2>&1 || {
    IMAGE_NAME=$FALLBACK_IMAGE_NAME
    docker pull ${IMAGE_NAME}
  }
else
  echo "Did not recognize image tag"
  exit 1
fi

DOCKER_COMMAND="--rm -m 1g --memory-reservation=256m -v $ROOT_DIR/icc/connector/$CUSTOMER/$SECRETS_FILENAME:/home/custom_integration/$OUT_SECRETS_FILENAME"

# if running on M1 mac, we need to specify the platform

if [ "$KERNEL_NAME" == "Darwin" ]; then
  CPU_BRAND="$(sysctl -n machdep.cpu.brand_string)"
  if [[ "$CPU_BRAND" =~ "Apple" ]]; then
    DOCKER_COMMAND="${DOCKER_COMMAND} --platform linux/amd64"
  fi
fi

if [ -z "$DEBUG" ]; then
  PYTHON_STR="python connector.py"
else
  echo "Setting in debug mode"
  PYTHON_STR="python connector.py --debug debug"
  DOCKER_COMMAND="${DOCKER_COMMAND} -p 5678:5678"
fi

DOCKER_COMMAND="${DOCKER_COMMAND} -v $ROOT_DIR/icc/connector/$CUSTOMER/logs:/home/custom_integration/logs"

# Check if exists/create the sql_database_copy.db file
FILE="$ROOT_DIR/icc/connector/$CUSTOMER/sql_database_copy.db"
if test -f "$FILE"; then
  echo "$FILE - Database exists."
else
  echo "Creating database: $FILE"
  touch "$FILE"
fi

# Mount the sql_database_copy.db file into the docker container
DOCKER_COMMAND="${DOCKER_COMMAND} -v $ROOT_DIR/icc/connector/$CUSTOMER/sql_database_copy.db:/home/custom_integration/sql_database_copy.db"

echo "Image that is being run is $IMAGE_NAME"

# Either run tests, run single order, or run listener
DOCKER_COMMAND="${DOCKER_COMMAND} ${IMAGE_NAME} ${PYTHON_STR} importer --repeat-part-id 'first'"

LOG_FILE=$ROOT_DIR/$CUSTOMER/repeat_work_starter.txt

echo "$(date) Starting the container for customer $CUSTOMER" >> $LOG_FILE
echo "Command being run is $DOCKER_COMMAND"
CONTAINER_ID=$(docker run -d -it ${DOCKER_COMMAND})
echo "$(date) Container ID for customer $CUSTOMER: $CONTAINER_ID" >> $LOG_FILE

echo "Checking every 120 seconds for 1 full day whether container is still up and there is no successfully exited container" >> $LOG_FILE
# Check if the container is running every 120 seconds for 1 day
for i in {1..720}; do
    # Sleep for 120 seconds and log the step
    echo "$(date) Sleeping for 120 seconds" >> $LOG_FILE
    sleep 120

    # Check if the container is running and log the step
    if [ ! "$(docker ps -q -f ancestor=${IMAGE_NAME})" ]; then
        if [ "$(docker ps -q -a -f exited=0 -f ancestor=${IMAGE_NAME})" ]; then
            echo "We found a container that exited with a success error code. Killing the monitor service" >> $LOG_FILE
            exit 0
        fi
        echo "$(date) Container for customer $CUSTOMER is not running. Restarting..." >> $LOG_FILE
        # Restart the container and update the container ID variable
        docker restart $CONTAINER_ID >> $LOG_FILE 2>&1
        CONTAINER_ID=$(docker ps -q -f id=$CONTAINER_ID)
        echo "$(date) Container ID for customer $CUSTOMER: $CONTAINER_ID" >> $LOG_FILE
        docker exec -it $CONTAINER_ID python connector.py importer --repeat-part-id 'first'
    else
        echo "$(date) Container for customer $CUSTOMER is still running" >> $LOG_FILE
    fi
done