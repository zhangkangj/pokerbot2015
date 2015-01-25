#!/bin/bash


OPPONENT="Nash"
RUN_ERROR=""
WIN_FILE_PATH="big_hand_data/MixedNewA1.txt"
GREP_STR="$OPPONENT[1-9]* wins the pot ([1-9][0-9][0-9])"
GREP_CMD="cat log/test/*.txt | grep -B30 -A4 '$GREP_STR' > $WIN_FILE_PATH"
./clean_up.sh

java -jar engine.jar

RUN_ERROR=$(cat *.dump | grep -i "error" | grep -v "no suitable")

if ["$RUN_ERROR" == ""]; then
	echo "--Engine Successfully Ran Without Erorr ..." 
	rm big_hand_data/*

	echo "--Grapping all large wins for $OPPONENT into $WIN_FILE_PATH..."
	echo "--Executing: $GREP_CMD"
	eval "$GREP_CMD" 
else
	echo "Engine Failed To Run, Erorr: " + $RUN_ERROR
fi
