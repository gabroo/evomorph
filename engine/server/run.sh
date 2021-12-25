#!/bin/bash

while getopts i:o: flag
do
  case "${flag}" in
    i) in=${OPTARG};;
    o) out=${OPTARG};;
  esac
done


echo "run.sh";
echo "Input: $in";
echo "Output: $out";
echo "calling morpheus ...";

if [[ -e morpheus ]]
then
  echo 'morpheus!'
else
  echo 'no morpheus :('
fi

exec morpheus --perf-stats --outdir $out -f $in
