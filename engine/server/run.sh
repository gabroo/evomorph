#!/bin/bash

while getopts i:o: flag
do
  case "${flag}" in
    i) in=${OPTARG};;
    o) out=${OPTARG};;
  esac
done

if ! command -v morpheus &> /dev/null
then
    echo "morpheus could not be found"
    exit 1
fi

echo "run.sh";
echo "Input: $in";
echo "Output: $out";
echo "calling morpheus ...";

exec morpheus --perf-stats --outdir $out -f $in
