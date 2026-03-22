#!/bin/sh
set -eu

if [ -z "${S3_DEFAULT_BUCKETS:-}" ]; then
  exit 0
fi

old_ifs=$IFS
IFS=','
for bucket in $S3_DEFAULT_BUCKETS; do
  bucket=$(echo "$bucket" | xargs)
  if [ -n "$bucket" ]; then
    awslocal s3api create-bucket --bucket "$bucket" >/dev/null 2>&1 || true
  fi
done
IFS=$old_ifs
