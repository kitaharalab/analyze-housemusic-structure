#!/bin/bash

SOURCE_DIRECTORY="../../images"
OUTPUT_DIRECTORY="../../images/eps"

mkdir -p "$OUTPUT_DIRECTORY"

for file in "$SOURCE_DIRECTORY"/*.png
do
  base=$(basename "$file" .png)

  convert "$file" "$OUTPUT_DIRECTORY/$base.eps"
done

