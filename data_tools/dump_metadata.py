import argparse
import sys
import os
import os.path as osp
import glob
from pipes import quote
from multiprocessing import Pool, current_process

import mmcv


def dump_frames(vid_item):
    full_path, vid_path, vid_id = vid_item
    vid_name = vid_path.split('.')[0]
    out_full_path = osp.join(args.out_dir, vid_name)
    try:
        os.mkdir(out_full_path)
    except OSError:
        pass
    vr = mmcv.VideoReader(full_path)
    # for i in range(len(vr)):
    #     if vr[i] is not None:
    #         mmcv.imwrite(
    #             vr[i], '{}/img_{:05d}.jpg'.format(out_full_path, i + 1))
    #     else:
    #         print('[Warning] length inconsistent!'
    #               'Early stop with {} out of {} frames'.format(i + 1, len(vr)))
    #         break
    # print('{} done with {} frames'.format(vid_name, len(vr)))
    # sys.stdout.flush()
    return vr.fps, vr.frame_cnt


def parse_args():
    parser = argparse.ArgumentParser(description='extract optical flows')
    parser.add_argument('src_dir', type=str)
    parser.add_argument('out_dir', type=str)
    parser.add_argument('--level', type=int,
                        choices=[1, 2],
                        default=2)
    parser.add_argument('--flow_type', type=str,
                        default=None, choices=[None])
    parser.add_argument('--df_path', type=str,
                        default='/data/mmaction/third_party/dense_flow')
    parser.add_argument("--ext", type=str, default='avi',
                        choices=['avi', 'mp4'], help='video file extensions')
    parser.add_argument("--resume", action='store_true', default=False,
                        help='resume optical flow extraction '
                        'instead of overwriting')
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    args = parse_args()

    if not osp.isdir(args.out_dir):
        print('Creating folder: {}'.format(args.out_dir))
        os.makedirs(args.out_dir)
    if args.level == 2:
        classes = os.listdir(args.src_dir)
        for classname in classes:
            new_dir = osp.join(args.out_dir, classname)
            if not osp.isdir(new_dir):
                print('Creating folder: {}'.format(new_dir))
                os.makedirs(new_dir)

    print('Reading videos from folder: ', args.src_dir)
    print('Extension of videos: ', args.ext)
    if args.level == 2:
        fullpath_list = glob.glob(args.src_dir + '/*/*.' + args.ext)
        done_fullpath_list = glob.glob(args.out_dir + '/*/*')
    elif args.level == 1:
        fullpath_list = glob.glob(args.src_dir + '/*.' + args.ext)
        done_fullpath_list = glob.glob(args.out_dir + '/*')
    print('Total number of videos found: ', len(fullpath_list))
    if args.resume:
        fullpath_list = set(fullpath_list).difference(set(done_fullpath_list))
        fullpath_list = list(fullpath_list)
        print('Resuming. number of videos to be done: ', len(fullpath_list))

    if args.level == 2:
        vid_list = list(map(lambda p: osp.join(
            '/'.join(p.split('/')[-2:])), fullpath_list))
    elif args.level == 1:
        vid_list = list(map(lambda p: p.split('/')[-1], fullpath_list))

    # Only videos with annotations
    annotation_dir = None
    from pathlib import Path
    if 'val' in args.src_dir:
        annotation_dir = Path(args.src_dir).joinpath('../annotations_val')
    elif 'test' in args.src_dir:
        annotation_dir = Path(args.src_dir).joinpath('../annotations_test')
    if annotation_dir:
        annotated_videos = set()
        for filename in annotation_dir.glob('*.txt'):
            if 'readme.txt' == filename.name:
                continue
            # Perhaps should be treat differently?
            # if 'Ambiguous' in filename.name:
            #     continue

            with open(filename, 'r') as fid:
                for line in fid:
                    line = line.strip()
                    instance_i = line.split()
                    assert len(instance_i) == 3
                    annotated_videos.add(instance_i[0])

        get_video_name = lambda x: Path(x).stem
        vid_list = [
            i for i in vid_list
            if get_video_name(i) in annotated_videos
        ]
        fullpath_list = [
            i for i in fullpath_list
            if get_video_name(i) in annotated_videos
        ]

    from pathlib import Path
    if 'val' in args.src_dir:
        metadata_file = Path(args.out_dir).joinpath('METADATA_val.csv')
    elif 'test' in args.src_dir:
        metadata_file = Path(args.out_dir).joinpath('METADATA_test.csv')
    metadata = []
    for i, vid_item in enumerate(vid_list):
        fps, num_frames = dump_frames((fullpath_list[i], vid_item, i))
        video_id = Path(vid_item).stem
        metadata.append([video_id, fps, num_frames])

    print(metadata_file)
    with open(metadata_file, 'w') as fid:
        fid.write('video_id,fps,num_frames\n')
        for line in metadata:
            fid.write('{},{},{}\n'.format(*line))
