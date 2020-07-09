#! /usr/bin/bash env

DATA_DIR="../../data/activitynet/"

if [[ ! -d "${DATA_DIR}" ]]; then
  echo "${DATA_DIR} does not exist. Creating";
  mkdir -p ${DATA_DIR}
fi

mkdir $DATA_DIR/annotations
wget http://ec2-52-25-205-214.us-west-2.compute.amazonaws.com/files/activity_net.v1-3.min.json && mv activity_net.v1-3.min.json $DATA_DIR/annotations
wget http://ec2-52-25-205-214.us-west-2.compute.amazonaws.com/files/activity_net.v1-2.min.json && mv activity_net.v1-2.min.json $DATA_DIR/annotations
