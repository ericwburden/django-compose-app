#!/bin/bash

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# Functions                                                                            #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

# Help -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

Help() {
  echo "usage: ./deploy.sh [-h] [-f] [-b] TAG"
  echo ""
  echo "positional arguments:"
  echo "  TAG          The tag associated with your deployment. (dev, prod, etc.)"
  echo ""
  echo "optional arguments:"
  echo "  -h, --help   Show this help message and exit"
  echo "  -f, --flush  Flush the database when deploying the docker stack. Does nothing"
  echo "               if deploying the default `prod` environment."
  echo "  -b, --build  Rebuild images when deploying the docker stack."
  echo "  -c, --clean  Cleans up build files and exits. Be careful, doing this"
  echo "               makes `docker-compose down` a lot down more difficult."
}

# Copy -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

Copy() {
  cp "deploy/$1/.env" ".env"
  cp "deploy/$1/Dockerfile" "Dockerfile"
  cp "deploy/$1/docker-compose.yml" "docker-compose.yml"
  cp "deploy/$1/requirements.txt" "requirements.txt"
  cp "deploy/$1/entrypoint.sh" "app/entrypoint.sh"
  chmod +x "app/entrypoint.sh"
}

# Cleanup-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

Cleanup() {
  rm ".env"
  rm "Dockerfile"
  rm "docker-compose.yml"
  rm "requirements.txt"
  rm "app/entrypoint.sh"
}

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# Parse Args                                                                           #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

PARAMS=""
FLUSH=""
BUILD=""
CLEAN=""

while (( "$#" )); do
  case "$1" in 
    -h|--help)
      Help
      exit
      ;;
    -f|--flush)
      FLUSH='true'
      shift
      ;;
    -b|--build)
      BUILD='true'
      shift
      ;;
    
    -c|--clean)
      Cleanup
      exit
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done # set positional arguments in their proper place

eval set -- "$PARAMS"

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# Main                                                                                 #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

# Copy Files -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

if [ -d "deploy/$1" ]; then
  # If the tag points to a real directory, copy the files
  echo "Copying"
  Copy $1
else
  echo "'$1' is not a valid tag, no 'deploy/$1' directory!"
  exit 1
fi

# Set Flush =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

if [ "$FLUSH" ]; then
  echo -e "\n\nFLUSH_DB=$FLUSH" >> ".env"
fi

# Docker Compose -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

COMPOSE_COMMAND="docker-compose up -d"

if [ "$BUILD" ]; then
  COMPOSE_COMMAND="$COMPOSE_COMMAND --build"
fi

eval "$COMPOSE_COMMAND"