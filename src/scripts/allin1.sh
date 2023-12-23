#!/bin/bash

INPUT_DIR="/path/to/input/directory"
OUTPUT_DIR="/path/to/output/directory"

mkdir -p "$OUTPUT_DIR"

find "$INPUT_DIR" -type f -name "*.wav" | while read filename; do
    allin1 -o "$OUTPUT_DIR" "$filename"
done

