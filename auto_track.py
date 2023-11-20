import os
import sys
import cv2

from tools import get_track_name_color, box_label, colors

os.environ['YOLO_VERBOSE'] = str(False)
from ultralytics import YOLO

import time

cv2.namedWindow("auto track", 0)
cv2.resizeWindow("auto track", 1000, 600)
n = 0  # 当前帧数
def show_bbox(frame, n, n_track, track_arr):
    while track_arr[n_track, 0] < n:  # 跳到当前帧的track结果
        if n_track >= track_arr.shape[0] - 1:
            break
        n_track += 1

    while track_arr[n_track, 0] == n:  # 当前帧有目标
        if n_track >= track_arr.shape[0] - 1:
            break
        n_track += 1
        box = track_arr[n_track, 2:6]  # 边框信息
        id = track_arr[n_track, 1]  # 目标id
        # 获取check后的名字
        name, color = get_track_name_color(id, None, track_arr[n_track, 1].min())
        # 绘制框和名字
        box_label(frame, box, name, color)
    return n_track  # ,frame


def do(video_path, auto_track_label, check_label, info=""):
    cap = cv2.VideoCapture(video_path)
    # 创建空文件 auto_track_label 和 check_label
    with open(auto_track_label, "w") as f:
        pass
    with open(check_label, "w") as f:
        pass

    # 记录当前跟踪到的片段id
    track_id_dict = {"end": -1, }

    # 重置到视频的开头
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    n = -1
    # 视频帧循环
    while cap.isOpened():
        n += 1
        # 读取一帧图像
        success, frame = cap.read()
        if not success:  # 视频播放结束时退出循环
            break
        print(f"\rFrame : {n},Find {track_id_dict['end'] + 1}, {info} ", end='     ')
        # 在帧上运行YOLOv8跟踪，persist为True表示保留跟踪信息，conf为0.3表示只检测置信值大于0.3的目标
        results = model.track(frame, conf=0.1, persist=True)
        # 得到该帧的各个目标的ID
        if results[0].boxes.id != None:
            track_ids = results[0].boxes.id.int().cpu().tolist()
            # 遍历该帧的所有目标
            for track_id, box in zip(track_ids, results[0].boxes.data):
                if box[-1] == 0:  # 检测目标为人
                    if track_id_dict.get(track_id) is None:
                        end = track_id_dict['end'] + 1
                        track_id_dict['end'] = end
                        track_id_dict[track_id] = end
                        with open(check_label, "a") as f:
                            f.write(f"{end},\n")
                    track_id = track_id_dict[track_id]
                    x1, y1, x2, y2 = box[:4].int().cpu().tolist()
                    line = str(n) + " " + str(track_id) + " " + str(x1) + " " + str(y1) + " " + str(
                        x2) + " " + str(y2)

                    with open(auto_track_label, "a") as f:
                        f.write(line + "\n")

                    box_label(frame, box, str(track_id), colors[(track_id) % 27])
        # frame = show_bbox(frame, n, n_track)
        cv2.imshow('auto track', frame)
        cv2.waitKey(1)
    print()
    # 释放视频捕捉对象，并关闭显示窗口
    cap.release()


if __name__ == '__main__':
    print("Loading YOLO model...")
    model = YOLO('yolov8x.pt').cuda()
    print("Loading video...")

    video_root = r"D:\video"
    label_root = r"D:\video\track_label"
    f = os.listdir(video_root)
    f.sort()

    arguments = sys.argv
    #
    # if len(arguments) < 4:
    #     exit(-1)

    fs = []
    # for n in f:
    #     ip = n.split('_')[0].split('.')[-1]
    #     if ip == arguments[1]:
    #         fs.append(n)
    fs = arguments[1:]
    # [
    #     # '10.10.10.212_1699936578.mp4',
    #       '10.10.10.212_1699940179.mp4'
    #
    #       ]
    index = -1
    for i in fs:
        time_clock = i.split('_')[-1].split('.')[0]
        local_time = time.localtime(int(time_clock))
        h = local_time.tm_hour
        md = local_time.tm_mon * 100 + local_time.tm_mday
        print(h)
        if h < 7 or h > 19:  # 7点之前的屏蔽  # 19点之后的屏蔽
            continue
        print(md)
        if md < 1114:  # 11.14号之前的屏蔽掉
            continue
        index += 1
        # if index % int(arguments[2]) != int(arguments[3]):  # 不是当前的fold
        #     continue
        video_path = f'{video_root}/{i}'
        auto_track_label = f'{label_root}/{i}.auto_track'
        check_label = f'{label_root}/{i}.check_map'
        temp = '.temp'
        # if os.path.exists(auto_track_label):
        #     continue
        do(video_path, auto_track_label + temp, check_label + temp,
           info=f"{i}: {local_time.tm_mon}/{local_time.tm_mday} {local_time.tm_hour}:{local_time.tm_sec}")
        os.rename(auto_track_label + temp, auto_track_label)
        os.rename(check_label + temp, check_label)
