#!/bin/bash

INPUT_DIR="/Users/justinwulf/Documents/justin/school/main/data/prod/songs/wav"
OUTPUT_DIR="/Users/justinwulf/Documents/justin/school/main/data/prod/allin1"
BACKUP_DIR="${INPUT_DIR}_backup"

cp -r "$INPUT_DIR" "$BACKUP_DIR"

mkdir -p "$OUTPUT_DIR"

find "$INPUT_DIR" -type f -name "*.wav" | while IFS= read -r filename; do
    allin1 -o "$OUTPUT_DIR" "$filename"
    if [ $? -eq 0 ]; then
        rm "$filename"
    fi
done
