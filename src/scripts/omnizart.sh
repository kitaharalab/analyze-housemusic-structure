#!/bin/zsh

docker pull --platform linux/amd64 mctlab/omnizart:latest
docker run --platform linux/amd64 -it --name "omnizart" -v .:/home mctlab/omnizart:latest bash -c "
cd inputs

for file in *.wav *.mp3
do
  echo 'Processing' \$file '...'
  omnizart drum transcribe \$file
  echo 'Done Transcribing' \$file '.'
done
"

for file in data/mp3/*.mp3
do
  base_name=$(basename "$file")
  midi_file_name="\${base_name%.*}.mid"
  docker cp omnizart:/home/$midi_file_name ./data/midi/\$midi_file_name
done

