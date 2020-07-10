#! /usr/bin/bash env

cd ../
python build_rawframes.py ../data/activitynet/v1-2/train ../data/activitynet/rawframes/ --level 2 --flow_type tvl1 --ext all --ignore_level_out | tee activitynet/log_v1-2_train.txt &&
echo "Raw frames (RGB and tv-l1) Generated for v1-2 train"

python build_rawframes.py ../data/activitynet/v1-2/val ../data/activitynet/rawframes/ --level 2 --flow_type tvl1 --ext all --ignore_level_out | tee activitynet/log_v1-2_val.txt &&
echo "Raw frames (RGB and tv-l1) Generated for v1-2 val"

python build_rawframes.py ../data/activitynet/v1-2/test ../data/activitynet/rawframes/ --level 2 --flow_type tvl1 --ext all --ignore_level_out | tee activitynet/log_v1-2_test.txt &&
echo "Raw frames (RGB and tv-l1) Generated for v1-2 test"

python build_rawframes.py ../data/activitynet/v1-3/train_val ../data/activitynet/rawframes --level 2 --flow_type tvl1 --ext all --ignore_level_out/ | tee activitynet/log_v1-3_train_val.txt &&
echo "Raw frames (RGB and tv-l1) Generated for v1-3 train_val"

python build_rawframes.py ../data/activitynet/v1-3/test ../data/activitynet/rawframes/ --level 2 --flow_type tvl1 --ext all --ignore_level_out | tee activitynet/log_v1-3_test.txt &&
echo "Raw frames (RGB and tv-l1) Generated for v1-3 test"

cd activitynet/
