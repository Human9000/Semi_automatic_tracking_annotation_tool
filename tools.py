import cv2


def box_label(image, box, label='', color=(128, 128, 128), txt_color=(255, 255, 0)):
    # 得到目标矩形框的左上角和右下角坐标
    p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
    # 绘制矩形框
    cv2.rectangle(image, p1, p2, color if label[0] not in '0123456789' else (0, 0, 255),
                  thickness=2 if label[0] not in '0123456789' else 10, lineType=cv2.LINE_AA)
    if label:
        # 得到要书写的文本的宽和长，用于给文本绘制背景色
        w, h = cv2.getTextSize(label, 0, fontScale=2, thickness=1)[0]
        # 确保显示的文本不会超出图片范围
        outside = p1[1] - h >= 3
        p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
        # cv2.rectangle(image, p1, p2, color, -1, cv2.LINE_AA)     #填充颜色
        # 书写文本
        cv2.putText(image,
                    label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2),
                    0,
                    2,
                    color if label[0] not in '0123456789' else (0, 0, 255),
                    thickness=2,
                    lineType=cv2.LINE_AA)


def load_check_map(check_label):
    with open(check_label, 'r') as f:
        lines = f.readlines()
        map1 = {}
        for i in lines:
            k, v = i[:-1].split(',')
            map1[int(k)] = v
    return map1


def get_track_name_color(id, check_map=None, color_base=0):
    if check_map is None:
        map1 = {}
    else:
        map1 = load_check_map(check_map)
    simple_name = map1.get(id)
    if simple_name is None:
        simple_name = f'{id}:unknown'
    if len(simple_name.replace(' ', '')) < 1:
        simple_name = f'{id}:unknown'
    if name_dict.get(simple_name) is not None:
        name = simple_name
        color = colors[sname_id[simple_name] % 27]
    else:
        name = f'{id}:unknown'
        color = colors[(color_base + id) % 27]
    return name, color


name_dict = {
    "other": "其他",
    "bj": "保洁",
    "cba": "陈昞翱",
    "dfx": "邓福兴",
    "fk": "符锟",
    "glm": "高黎敏",
    "gsq": "甘三奇",
    "gyc": "顾芸超",
    "hq": "黄强",
    "lcy": "李承阳",
    "lg": "李庚",
    "lh": "刘豪",
    "ljq": "刘洁琴",
    "lwl": "赖文蕾",
    "lxs": "罗昕山",
    "lyq": "刘裕奇",
    "lzj": "刘战举",
    "rzg": "任振国",
    "sch": "申春华",
    "slb": "施立波",
    "wcf": "王彩峰",
    "wp": "吴鹏",
    "xx": "项行",
    "ypc": "袁丕超",
    "yxw": "杨兴炜",
    "zgq": "张光全",
    "zhh": "张浩浩",
    "zsw": "朱所为",
}

snames = list(name_dict.keys())
sname_id = {k: i for i, k in enumerate(snames)}
id_sname = {i: k for i, k in enumerate(snames)}

colors = []
lci = [50, 125, 205]
lcj = [235, 175, 50]
lck = [50, 255, 185]
for i in lci:
    for j in lcj:
        for l in lck:
            colors.append([i, j, l])

if __name__ == '__main__':
    print(sname_id)
    print(id_sname)
