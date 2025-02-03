#!/bin/bash
# runs the repeat work importer, and checks for 1 days that the containers still up, and restarts it if not
# run w the command: nohup bash repeat_work_starter.sh {CUSTOMER_NAME} &
# prints logs to: /home/paperless/connector/{CUSTOMER_NAME}/repeat_work_starter.txt

# Get the CUSTOMER_NAME input parameter and store it in a variable
CUSTOMER=$1

if [ -z "$CUSTOMER" ]; then
  echo "Please pass a customer name to run the repeat work starter script" >> $LOG_FILE
  exit 1
fi

# Define the log file
LOG_FILE=/home/paperless/connector/$CUSTOMER/repeat_work_starter.txt

# Start the container and log the step
echo "$(date) Starting the container for customer $CUSTOMER" >> $LOG_FILE
CONTAINER_ID=$(docker run -d -m 1g --memory-reservation=256m -v ~/connector/$CUSTOMER/secrets.ini:/home/custom_integration/secrets.ini -v ~/connector/$CUSTOMER/logs:/home/custom_integration/logs -v ~/connector/$CUSTOMER/sql_database_copy.db:/home/custom_integration/sql_database_copy.db -it 431105233043.dkr.ecr.us-west-2.amazonaws.com/$CUSTOMER:release python connector.py importer --repeat-part-id 'first')
echo "$(date) Container ID for customer $CUSTOMER: $CONTAINER_ID" >> $LOG_FILE

echo "Checking every 120 seconds for 1 full day whether container is still up and there is no successfully exited container" >> $LOG_FILE
# Check if the container is running every 120 seconds for 1 day
for i in {1..720}; do
    # Sleep for 120 seconds and log the step
    echo "$(date) Sleeping for 120 seconds" >> $LOG_FILE
    sleep 120

    # Check if the container is running and log the step
    if [ ! "$(docker ps -q -f ancestor=431105233043.dkr.ecr.us-west-2.amazonaws.com/$CUSTOMER:release)" ]; then
        if [ "$(docker ps -q -a -f exited=0 -f ancestor=431105233043.dkr.ecr.us-west-2.amazonaws.com/$CUSTOMER:release)" ]; then
            echo "We found a container that exited w a success error code. Killing the monitor service" >> $LOG_FILE
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