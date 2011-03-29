#!/bin/sh

# launch audio

if [ -s mplayer.pid ]; then
	kill $(cat mplayer.pid)
fi

mplayer -volume 20 -softvol -loop 0 -shuffle soundtrack/*.ogg soundtrack/*.mp3  >/dev/null 2>&1 &
echo "$!" >mplayer.pid

while true; do
	./editor-master.py
	sleep 1
done

