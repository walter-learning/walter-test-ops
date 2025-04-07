#!/usr/bin/env bash

#########
# USAGE
#########
display_usage() {
  echo
  echo "Usage: $0"
  echo
  echo " --help
      Display usage instruction"
  echo " -q, --question <question>
      Specify the handler to trigger"
  echo " -p, --port <port>
      Specify the port to use"
  echo " -b, --build
      Builds the requirements before running tests if flag is passed"
  echo
  echo " Example: \"bash run.sh -q 0 -b\""
  echo
}


##################
# DEFAULT VALUES
##################
QUESTION=""
PORT=9000
EVENT_PATH="events/question_${QUESTION}.json"
MOUNT_PATH=""
BUILD=0
IMAGE_TAG="walter-test-ops"

build() {
    echo "before build"
    docker build -f .docker/Dockerfile -t $IMAGE_TAG "./" --no-cache
    echo "before start"
}

run() {  
  # Build check
  if [[ "$BUILD" -eq "1" ]]; then
    echo "[BUILD] Building the image"
    build
  fi

  EVENT_PATH="events/question_${QUESTION}.json"

  # Build path
  echo "[RUN] Run $HANDLER"
  if [[ "$OSTYPE" == "msys"* ]]; then   
    (sleep 4 ; curl -XPOST "http://localhost:$PORT/2015-03-31/functions/function/invocations" -d @$EVENT_PATH -v) &     
    docker run \
      -v "//$PWD/handlers":"/var/task/$WORKER/handlers" \
      -v "//$PWD/data":"/var/task/$WORKER/data" \
      -v "//$PWD/libs":"/opt/site-packages/libs" \
      -e PYTHONPATH="//var/task/${WORKER}/site-packages":"//var/task/${WORKER}":"//opt":"//opt/site-packages" \
      --env-file .env \
      -p $PORT:8080 \
      --rm \
      $IMAGE_TAG $HANDLER
  else
    (sleep 4 ; curl -XPOST "http://localhost:$PORT/2015-03-31/functions/function/invocations" -d @$EVENT_PATH ) &
    docker run \
      -v "$PWD/handlers/$SERVICE/$WORKER":"/var/task/$WORKER/handlers" \
      -v "$PWD/data/$SERVICE/$WORKER":"/var/task/$WORKER/data" \
      -v "$PWD/libs":"/opt/site-packages/libs" \
      -e PYTHONPATH="/var/task/${WORKER}/site-packages":"/var/task/${WORKER}":"/opt":"/opt/site-packages" \
      --env-file .env \
      -p $PORT:8080 \
      --rm \
      $IMAGE_TAG handlers.handle
  fi


}



###################
# COMMAND PARSING
###################
# https://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash
while  test $# -gt 0; do
  case "$1" in
    --help)
      display_usage
      exit 1
      ;;
    -q|--question)
      shift
      QUESTION=$1
      if [[ -z "$QUESTION" ]] || [[ "$QUESTION" =~ ^- ]]; then
        echo "[ERROR] The -q flag must take an argument."
        exit 1      
      else
        shift
      fi
      ;;
    -p|--port)
      shift
      PORT=$1
      shift
      ;;
    -b|--build)
      shift
      if [[ -z $1 ]] || [[ $1 =~ ^- ]]; then
        BUILD=1
      else
        echo "[ERROR] The -b flag does not take any argument."
        exit 1
      fi
      ;;    
    *)
      echo "[ERROR] Invalid option. Run --help to check available flags"
      exit 1
      ;;
  esac
done

#########
# MAIN
#########
run
