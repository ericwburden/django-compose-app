#!/bin/bash

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#
# Main                                                                                 #
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

# Set Variables =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

FILENAME="deploy/env-template.csv"
OLDIFS="$IFS"
IFS=","

# Exit Checks =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

# Check formatting and exit early if need be
[ ! -f $FILENAME ] && { echo "$FILENAME file not found"; exit 1; }
[ -z "$1" ] && { echo "Need to provide a deployment directory name"; exit 1; }
[ ! -d "deploy/$1" ] && { echo "No deployment directory '$1'"; exit 1; }
[ -f "deploy/$1/.env" ] &&  { echo "'deploy/$1/.env' file already exists, delete or rename it to proceed"; exit 1; }

# Display Message =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

clear
echo "Please enter values to pass to your deployment through the '.env' file."
echo "Pressing 'Enter' without typing will accept the default value, which is"
echo "not recommended in most cases. Control+D will fill in all remaining fields"
echo "with default values (even more 'not recommended')."
echo -e "\n"

# Take User Input =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=#

sed 1d $FILENAME | while IFS=, read -r FIELD MSG DEF COM; do
  echo "$MSG (Default: $DEF)" # Display instructions
  read -u 1 -p "$FIELD: " VAL # Take user input
  [ -z "$VAL" ] && VAL="$DEF" # If no user input, use the default

  echo -e "$FIELD=$VAL\n"  # Show variable definition
  echo -e "$FIELD=$VAL" >> "deploy/$1/.env" # Write to .env file
done

IFS=$OLDIFS # Reset IFS