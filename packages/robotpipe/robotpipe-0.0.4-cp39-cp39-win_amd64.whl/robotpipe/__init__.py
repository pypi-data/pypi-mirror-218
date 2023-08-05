# coding: utf-8
# pylint: disable=wrong-import-position
"""InsightFace: A Face Analysis Toolkit."""
from __future__ import absolute_import

try:
    #import mxnet as mx
    import onnxruntime
except ImportError:
    raise ImportError(
        "Unable to import dependency onnxruntime. "
    )

__version__ = '0.0.4'


from .face_attribute import *
from .face_detection import *
from .face_landmark import *
from .face_recognition import *
from .face_swapper import *

from .yolo_detect import *
from .utils import *

# 确认文件夹是否已经创建，若无，则创建
import os
root = os.path.expanduser('~/.robotpipe')
model_root = os.path.join(root, 'models')
os.makedirs(model_root,exist_ok=True)


