#!/bin/bash

INPUT_DIR="../../data/prod/songs/mp3_tmp"
OUTPUT_DIR="../../data/prod/songs/wav"

mkdir -p "$OUTPUT_DIR"

find "$INPUT_DIR" -type f -name "*.mp3" | while IFS= read -r filename; do
    base_name=$(basename "$filename" .mp3)
    new_filename="$OUTPUT_DIR/$base_name.wav"

    # MP3をWAVに変換し、既存のファイルは上書き
    ffmpeg -y -i "$filename" "$new_filename"

    # 変換後、元のMP3ファイルが存在する場合は削除
    if [ -f "$filename" ]; then
        rm "$filename"
    fi
done
