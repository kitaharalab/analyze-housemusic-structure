#!bin/bash

for file in songs_omnizart/*/*.mp3; do
	omnizart drum transcribe "$file"
done

