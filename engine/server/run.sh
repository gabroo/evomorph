#!/bin/bash

while getopts i:o: flag
do
  case "${flag}" in
    i) in=${OPTARG};;
    o) out=${OPTARG};;
  esac
done

echo "Input: $in";
echo "Output: $out";

exec morpheus --perf-stats --outdir $out -f $in
