#!/bin/bash

INPUT_DIR="/path/to/input/directory"
OUTPUT_DIR="/path/to/output/directory"

mkdir -p "$OUTPUT_DIR"

find "$INPUT_DIR" -type f -name "*.mp3" | while read filename; do
    base_name=$(basename "$filename" .mp3)
    new_filename="$OUTPUT_DIR/$base_name.wav"

    ffmpeg -i "$filename" "$new_filename"
done

