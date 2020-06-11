# Launch container on project dir

docker run --gpus all -v /etc/passwd:/etc/passwd:ro -v /etc/group:/etc/group:ro -v /etc/shadow:/etc/shadow:ro -u $(id -u):$(id -g) -v $(pwd):$(pwd) -v $HOME/datasets:$HOME/datasets -w $(pwd) --shm-size=48G -it mmaction:latest
