#!/bin/bash
json_info=$1
max_sz=$2

src_profile=$(echo $json_info | jq -r '.src_profile')
dst_profile=$(echo $json_info | jq -r '.dst_profile')

s3_src_file=$(echo $json_info | jq -r '.src_path')
s3_dst_file=$(echo $json_info | jq -r '.dst_path')


aws s3 --profile ${src_profile} cp "${s3_src_file}" - | aws s3 --profile ${dst_profile} cp  --expected-size   $max_sz    - "${s3_dst_file}"
echo "${s3_src_file} =>  ${s3_dst_file}"
exit $?