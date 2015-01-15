#!/bin/bash

#
# ./script.sh <YourBotName>
#
# This will create a folder structure require for your bot and player, based on Naive Bot
# After runnig this script, you need to modify the *_bot.py and *_player.py to realize your
# own stregety. You also need to add your bot to the top level config.txt for it to play
#

BOT_NAME_PREFIX=""
#OSX needs this for sed to work, for linux, assign empty string to this variable 
#OSX_SED_EXTRA=""
OSX_SED_EXTRA=".sed.bak"

NAIVE_BOT_NAME_PREFIX="naive"
NAIVE_BOT_NAME_PREFIX_UPPER="Naive"
NAIVE_PY_FILE_PATH="./naive.py"
NAIVE_BOT_PLAYER_DIR_PATH="./bot/naive" 
NAIVE_BOT_PY_PATH="./bot/naive/naive_bot.py" 
NAIVE_PLAYER_PY_PATH="./bot/naive/naive_player.py" 
NAIVE_CONFIG_DIR_PATH="./config/naive" 

if [ $# != 1 ]; then 
	echo "Usage: $0 <BOT_NAME>"
	exit
else
	BOT_NAME_PREFIX="$(echo $1 | tr '[A-Z]' '[a-z]')"
	while true; do
	    read -p "Use '$BOT_NAME_PREFIX' as name? <Y/N> " yn
	    case $yn in
		[Yy]* ) echo "start adding bot with name prefix '$BOT_NAME_PREFIX'..."; 
			echo "";
			break;;
		[Nn]* ) exit;;
		* ) echo "Please answer Y or N.";;
	    esac
	done
fi

# Change the first char to uppercase
BOT_NAME_PREFIX_UPPER="$(tr '[:lower:]' '[:upper:]' <<< ${BOT_NAME_PREFIX:0:1})${BOT_NAME_PREFIX:1}"

# Step 1
# Copy the toplevel .py
PY_FILE_PATH="./$BOT_NAME_PREFIX.py"
cp $NAIVE_PY_FILE_PATH $PY_FILE_PATH 
# Replace text
sed -i"$OSX_SED_EXTRA" "s/$NAIVE_BOT_NAME_PREFIX/$BOT_NAME_PREFIX/g" "$PY_FILE_PATH"
sed -i"$OSX_SED_EXTRA" "s/$NAIVE_BOT_NAME_PREFIX_UPPER/$BOT_NAME_PREFIX_UPPER/g" "$PY_FILE_PATH"
# Clean up
if [ $OSX_SED_EXTRA != "" ]; then 
	rm -f *"$OSX_SED_EXTRA"
fi

#Step 2
# Copy items from the bot/player dir
BOT_PLAYER_DIR_PATH="./bot/$BOT_NAME_PREFIX"
mkdir $BOT_PLAYER_DIR_PATH
BOT_PY_PATH="$BOT_PLAYER_DIR_PATH/$BOT_NAME_PREFIX"_bot.py
PLAYER_PY_PATH="$BOT_PLAYER_DIR_PATH/$BOT_NAME_PREFIX"_player.py
cp $NAIVE_BOT_PY_PATH $BOT_PY_PATH
cp $NAIVE_PLAYER_PY_PATH $PLAYER_PY_PATH
#need the __init__.py for python package
cp "$NAIVE_BOT_PLAYER_DIR_PATH"/__init__.py "$BOT_PLAYER_DIR_PATH"/
# Replace text
sed -i"$OSX_SED_EXTRA" "s/$NAIVE_BOT_NAME_PREFIX/$BOT_NAME_PREFIX/g" "$BOT_PY_PATH"
sed -i"$OSX_SED_EXTRA" "s/$NAIVE_BOT_NAME_PREFIX_UPPER/$BOT_NAME_PREFIX_UPPER/g" "$BOT_PY_PATH"
sed -i"$OSX_SED_EXTRA" "s/$NAIVE_BOT_NAME_PREFIX/$BOT_NAME_PREFIX/g" "$PLAYER_PY_PATH"
sed -i"$OSX_SED_EXTRA" "s/$NAIVE_BOT_NAME_PREFIX_UPPER/$BOT_NAME_PREFIX_UPPER/g" "$PLAYER_PY_PATH"
# Clean up
if [ $OSX_SED_EXTRA != "" ]; then
        rm -f "$BOT_PLAYER_DIR_PATH"/*"$OSX_SED_EXTRA"
fi

#Step 3
# Copy items from the config dir
CONFIG_DIR_PATH="./config/$BOT_NAME_PREFIX"
cp -r $NAIVE_CONFIG_DIR_PATH $CONFIG_DIR_PATH
# Replace the text
sed -i"$OSX_SED_EXTRA" "s/$NAIVE_BOT_NAME_PREFIX/$BOT_NAME_PREFIX/g" "$CONFIG_DIR_PATH"/pokerbot.*
sed -i"$OSX_SED_EXTRA" "s/$NAIVE_BOT_NAME_PREFIX_UPPER/$BOT_NAME_PREFIX_UPPER/g" "$CONFIG_DIR_PATH"/pokerbot.*
# Clean up
if [ $OSX_SED_EXTRA != "" ]; then
        rm -f "$CONFIG_DIR_PATH"/*"$OSX_SED_EXTRA"
fi

echo "Successfully Added Bot Player with Prefix: '$BOT_NAME_PREFIX'!" 
echo ""
echo "-- Now, You Can Modify $BOT_PY_PATH and $PLAYER_PY_PATH with Your Strategy."
echo "-- Afterwards, Add the Bot Player to the config.txt Such As:"
echo "		PLAYER_1_TYPE = FOLDER"
echo "		PLAYER_1_PATH = config/$BOT_NAME_PREFIX"
echo "		PLAYER_1_NAME = $BOT_NAME_PREFIX_UPPER" 



