import cv2
import numpy as np
from tools import box_label, load_check_map, get_track_name_color

video_name = "10.10.10.211_1699943780.mp4"

video_path = f"D:/video/{video_name}"
auto_track_label = f"D:/video/track_label/{video_name}.auto_track"
check_map_path = f"D:/video/track_label/{video_name}.check_map"

# 加载视频，获得相关参数
cap = cv2.VideoCapture(video_path)
cv2.namedWindow("YOLOv8 Checking", 0)
cv2.resizeWindow("YOLOv8 Checking", 1000, 600)
id = 0  # 跟踪到的目标


def load_auto_track(auto_track_label):
    # 读取自动跟踪的结果
    track_data = []
    with open(auto_track_label, "r") as f:
        for line in f.readlines():
            track_data.append(line[:-1].split(" "))
    track_arr = np.asarray(track_data)
    return track_arr


track_arr = load_auto_track(auto_track_label).astype(np.int32)

# 配置信息
index_cap = []  # 视频帧索引
n_track = 0  # 当前跟踪到的片段id
key = 0  # 按键
n = 0  # 当前帧数
cap.grab()  # 预读一帧


def show_bbox(frame, n_track, track_arr):
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
        name, color = get_track_name_color(id, check_map_path, track_arr[n_track, 1].min())
        # 绘制框和名字
        box_label(frame, box, name, color)
    return n_track  # ,frame


# 视频帧循环
while cap.isOpened():
    _, frame = cap.retrieve()  # 解码一帧

    if _ is False:
        break
    n_track = show_bbox(frame, n_track, track_arr)
    cv2.imshow("YOLOv8 Checking", frame)  # 显示标记好的当前帧图像
    cv2.waitKey(1)
    key = cv2.waitKey(0)

    if key & 0xFF == ord("q"):  # 'q'按下时，终止运行
        break
    elif key in [
        ord('p'),
        ord('a'),
        ord('s'),
        ord('d'),
                 ord(' ')]:
        map1 = load_check_map(check_map_path)
        n_track_temp = n_track

        # 获取当前帧的track状态
        while map1.get(track_arr[n_track, 1]) is not None:
            if n_track >= len(track_arr) - 1:
                break
            if map1.get(track_arr[n_track, 1]).__len__() <= 1:
                break
            n_track += 1

        # 自动跟踪到的id为
        track_id = track_arr[n_track, 1]
        n2 = track_arr[n_track, 0]
        n_track = n_track_temp
        # 往后跳转的帧数为
        while n < n2:
            n += 1
            cap.grab()
            print(n)
            if (n2 - n) % (25 * 3) == 0:
                _, frame = cap.retrieve()  # 解码一帧
                n_track = show_bbox(frame, n_track, track_arr)
                cv2.imshow("YOLOv8 Checking", frame)  # 显示标记好的当前帧图像
                cv2.waitKey(1)

        n_track = n_track_temp
    elif key == ord("r"):  # 'a' 重置
        n = 0
        n_track = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        cap.grab()
    # elif key == ord("s"):  # 'd'按下时，暂停
    #     n += 1
    #     cap.grab()
    # elif key == ord("d"):  # 'd'按下时，暂停
    #     n += 25
    #     for i in range(25):
    #         cap.grab()
    # elif key == ord("f"):  # 'd'按下时，暂停
    #     n += 25 * 10
    #     for i in range(25 * 10):
    #         cap.grab()

# 释放视频捕捉对象，并关闭显示窗口
cap.release()
cv2.destroyAllWindows()
