## Preparing ActivityNet v1.3

> WIP: For more details, please refer to the [official website-TODO](). We provide scripts with documentations. Before we start, please make sure that the directory is located at `$MMACTION/data_tools/activitynet/`.

### Prepare annotations

First of all, run the following script to prepare annotations.

```shell
bash download_annotations.sh
```

### Prepare videos

[Contact](https://docs.google.com/forms/d/e/1FAIpQLSeKaFq9ZfcmZ7W0B0PbEhfbTHY41GeEgwsa7WobJgGUhn4DTQ/viewform) the dataset maintainers to get access to the download links.

PR-Welcome: script to automate this.

After uncompressing the data, the folder should look like this:

```
activitynet
├── v1-3
│   ├── train_val
│   │   ├── v_TIjwhYSIRgg.mp4
│   ├── test
├── v1-2
│   ├── val
│   ├── train
│   ├── test
├── annotations
```

> Note: not all the videos use the `mp4` container.

### Extract frames

Now it is time to extract frames from videos.
Before extraction, please refer to `DATASET.md` for installing [dense_flow].
If you have some SSD, then we strongly recommend extracting frames there for better I/O performance.

```shell
# execute these two line (Assume the SSD is mounted at "/mnt/SSD/")
mkdir /mnt/SSD/thumos14_extracted/
ln -s /mnt/SSD/thumos14_extracted/ ../data/thumos14/rawframes/
```

Afterwards, run the following script to extract frames.
```shell
bash extract_frames.sh
```
