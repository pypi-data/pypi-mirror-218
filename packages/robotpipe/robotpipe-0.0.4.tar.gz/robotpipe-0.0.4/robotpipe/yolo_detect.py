import numpy as np
import os
import onnxruntime as ort
import cv2 as cv
from .utils import getInter,getIou,draw_labels

class YoloDetector:
    def __init__(self,model_path=None):
        super(YoloDetector, self).__init__()

        # 判断模型地址
        if model_path is None:
            root = os.path.expanduser('~/.robotpipe')
            model_root = os.path.join(root, 'models')
            model_name = "yolov8m.onnx"
            model_path = os.path.join(model_root, model_name)
            if not os.path.exists(model_path):
                print(f"{model_path} is not exists")
        
        # 构造推理对象
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

        # 获取元数据
        meta = self.session.get_modelmeta().custom_metadata_map
        self.label_names = eval(meta["names"])

        height, width = eval(meta["imgsz"])
        self.height = height
        self.width = width
    
    def predict(self,img,conf_thresh=0.3,iou_thresh=0.45):
        height,width = img.shape[0:2]
        # 计算缩放比例
        self.x_scale = width/self.width
        self.y_scale = height/self.height
        # 将图像缩放到模型推理尺寸
        scale_img = cv.resize(img,(self.width,self.height))

        scale_img = scale_img/255
        scale_img = np.transpose(scale_img,(2,0,1))
        data = np.expand_dims(scale_img, axis=0)

        pred = self.session.run([self.output_name],{self.input_name:data.astype(np.float32)})[0]
        # 删除单维度条目
        pred = np.squeeze(pred)
        # 调换数据的维度
        pred = np.transpose(pred,(1,0))

        pred_confs = pred[...,4:]
        max_conf = np.max(pred_confs,axis=1)
        max_conf_index = np.argmax(pred_confs,axis=1)

        # 插入之后数据变成, x, y, w, h, max_conf,max_conf_index
        pred = np.insert(pred, 4, max_conf, axis=1)
        pred = np.insert(pred, 5, max_conf_index, axis=1)
        # 非极大值抑制
        outputs = self.nms(pred,conf_thresh,iou_thresh)
        return outputs
    
    def draw_labels(self,img,outputs):
        dst = img.copy()
        draw_labels(outputs,dst,self.x_scale,self.y_scale,self.label_names)
        return dst

    # 非极大值抑制 x, y, w, h, max_conf,max_conf_index
    def nms(self,pred_values,conf_thresh,iou_thresh):
        # 剔除自信度比较低的数据
        confs = pred_values[..., 4] > conf_thresh
        pred_boxes = pred_values[confs == True]

        # 根据iou删除，重复的框
        sorted_index = np.argsort(pred_boxes[:,4])
        sorted_pred_boxes = pred_boxes[sorted_index]

        # 计算总共有几类数据
        total_class = list(set(sorted_pred_boxes[...,5]))
        outputs = []
        for cls in total_class: # 对每类数据进行非极大值抑制

            current_class_boxes = []
            # 找出当前类所有的框
            for box in sorted_pred_boxes:
                if box[5] == cls:
                    current_class_boxes.append(box)
            
            # 处理当前类的数据
            max_box = current_class_boxes[-1]
            outputs.append(max_box)
            boxes = np.delete(current_class_boxes,-1,axis=0)

            # 将最大的框，从排序的框中删除
            while len(boxes) > 0:
                delete_index = []
                for i,box in enumerate(boxes):
                    # 计算与最大框相交的面积
                    inter_area = getInter(max_box, box)
                    # 计算iou
                    iou = getIou(max_box,box,inter_area)
                    # 判断阈值
                    if iou > iou_thresh:
                        # 若条件成立，则删除这个框
                        delete_index.append(i)
                boxes = np.delete(boxes,delete_index,axis=0)
                if len(boxes) > 0:
                    max_box = boxes[-1]
                    outputs.append(max_box)
                    boxes = np.delete(boxes,-1,axis=0)
        return outputs    
    
    