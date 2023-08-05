import cv2 as cv
import numpy as np

def draw_faces(img, faces):
    import cv2
    dimg = img.copy()
    for i in range(len(faces)):
        face = faces[i]
        box = face.bbox.astype(int)
        color = (0, 0, 255)
        cv2.rectangle(dimg, (box[0], box[1]), (box[2], box[3]), color, 2)
        if face.kps is not None:
            kps = face.kps.astype(int)
            #print(landmark.shape)
            for l in range(kps.shape[0]):
                color = (0, 0, 255)
                if l == 0 or l == 3:
                    color = (0, 255, 0)
                cv2.circle(dimg, (kps[l][0], kps[l][1]), 1, color,
                            2)
        if face.gender is not None and face.age is not None:
            cv2.putText(dimg,'%s,%d'%(face.sex,face.age), (box[0]-1, box[1]-4),cv2.FONT_HERSHEY_COMPLEX,0.7,(0,255,0),1)

    return dimg

def draw_landmarks(img,faces):
    dimg = img.copy()
    for face in faces:
        landmark = face["landmark_2d_106"]
        lmk = np.round(landmark).astype(np.int32)
        print(lmk.shape)
        for l in range(lmk.shape[0]):
            color = (np.random.randint(0,255), np.random.randint(0,255), np.random.randint(0,255))
            cv.circle(dimg, (lmk[l][0], lmk[l][1]), 1, color,2)
    return dimg


def draw_labels(pred_boxes,dst,x_scale,y_scale,label_names):

    for i in range(len(pred_boxes)):
        x, y, w, h,c, index = pred_boxes[i][0:6]

        cx = int(x*x_scale)
        cy = int(y*y_scale)
        sw = int(w*x_scale)
        sh = int(h*y_scale)

        sx = int(cx - sw/2)
        sy = int(cy - sh/2)

        color = (np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
        cv.rectangle(dst,(sx,sy,sw,sh),color,3)
        label = label_names[int(index)]
        print(label,c)
        txt = f"{label}-{c:.2f}"
        cv.putText(dst,txt,(sx,sy-12),cv.FONT_HERSHEY_COMPLEX,0.8,color,2)


 # 计算IOU
def getIou(box1, box2, inter_area):
    box1_area = box1[2] * box1[3]
    box2_area = box2[2] * box2[3]
    union = box1_area + box2_area - inter_area
    iou = inter_area / union
    return iou

# 计算两个矩形相交的面积
def getInter(box1, box2):
    box1_x1, box1_y1, box1_x2, box1_y2 = box1[0] - box1[2] / 2, box1[1] - box1[3] / 2, \
                                        box1[0] + box1[2] / 2, box1[1] + box1[3] / 2
    box2_x1, box2_y1, box2_x2, box2_y2 = box2[0] - box2[2] / 2, box2[1] - box1[3] / 2, \
                                        box2[0] + box2[2] / 2, box2[1] + box2[3] / 2
    if box1_x1 > box2_x2 or box1_x2 < box2_x1:
        return 0
    if box1_y1 > box2_y2 or box1_y2 < box2_y1:
        return 0
    x_list = [box1_x1, box1_x2, box2_x1, box2_x2]
    x_list = np.sort(x_list)
    x_inter = x_list[2] - x_list[1]
    y_list = [box1_y1, box1_y2, box2_y1, box2_y2]
    y_list = np.sort(y_list)
    y_inter = y_list[2] - y_list[1]
    inter = x_inter * y_inter
    return inter