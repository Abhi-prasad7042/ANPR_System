from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from paddleocr import PaddleOCR, draw_ocr
import cv2
import os
import numpy as np
import torch
import re

file_path = os.path.join(os.path.dirname(__file__), 'best.pt')
model = torch.hub.load('ultralytics/yolov5', 'custom', path=file_path, force_reload=True)

def image_process(src):
    sharpening_kernel = np.array([[0, -1, 0],
                             [-1, 5, -1],
                             [0, -1, 0]])
    normalize = cv2.normalize(
            src, np.zeros((src.shape[0], src.shape[1])), 0, 155, cv2.NORM_MINMAX
        )

    sharpened_image = cv2.filter2D(normalize, -1, sharpening_kernel)
    return sharpened_image

def ocr(src):
    ocr = PaddleOCR(use_angle_cls=True,lang="en", show_log=False)
    img = cv2.imread(src)
    if img is None:
            return "not found"
    sharpened_image = image_process(img)
    result = ocr.ocr(sharpened_image, cls=True)
    if result:
        if len(result[0]) == 1:
            text, conf_score = result[0][0][1][0], result[0][0][1][1]
            text = re.sub(r"[^A-Z0-9- ]", "", text).strip("- ")
            return [text, conf_score]

        elif len(result[0])==2:
            text1, conf_score1 = result[0][0][1][0], result[0][0][1][1]
            text2, conf_score2 = result[0][1][1][0], result[0][1][1][1]
            text = text1+text2
            # text = re.sub(r"[^A-Z0-9- ]", "", text).strip("- ")
            conf_score=np.mean([conf_score1,conf_score2])
            return [text, conf_score]
        else:
            text = ""
            conf_score = 1
            for i in range(len(result[0])):
                text= text+result[0][i][1][0]
                conf_score = np.mean([conf_score, result[0][i][1][1]])
            return [text, conf_score]
    return []


def detection(src):
    ocr = PaddleOCR(use_angle_cls=True,lang="en", show_log=False)
    img = cv2.imread(src)
    img1 = model(img)
    df = img1.pandas().xyxy[0]
    if len(df)==0:
        return ["not found", 0]
    xmin= int(df[df["name"]=="NumberPlate"]["xmin"].values[0])+15
    xmax = int(df[df["name"]=="NumberPlate"]["xmax"].values[0])
    ymin = int(df[df["name"]=="NumberPlate"]["ymin"].values[0])
    ymax = int(df[df["name"]=="NumberPlate"]["ymax"].values[0])

    cropped_image = cropped_image = img[ymin:ymax, xmin:xmax]
    shrp_image = image_process(cropped_image)

    result = ocr.ocr(shrp_image, cls=True)
    if result:
        if len(result[0]) == 1:
            text, conf_score = result[0][0][1][0], result[0][0][1][1]
            text = re.sub(r"[^A-Z0-9- ]", "", text).strip("- ")
            return [text, conf_score]

        elif len(result[0])==2:
            text1, conf_score1 = result[0][0][1][0], result[0][0][1][1]
            text2, conf_score2 = result[0][1][1][0], result[0][1][1][1]
            text = text1+text2
            # text = re.sub(r"[^A-Z0-9- ]", "", text).strip("- ")
            conf_score=np.mean([conf_score1,conf_score2])
            return [text, conf_score]
    return ["not found", 0]

# Create your views here.
def index(request):
    if request.method == 'POST':
        image = request.FILES.get("image")
        instance = ImageOCR.objects.create(image=image)
        image_url = os.path.join('/media/', instance.image.name)
        file_path = os.path.join("number", instance.image.name)  
        file_path = file_path.replace("\\", "/") #correcting the filepath
        
        # checking which button is called 
        if 'anpr' in request.POST:
            det = ocr(file_path)
        elif 'detection' in request.POST:
            det = detection(file_path)

        context = {
             'image_url': image_url,
             "number": det[0],
             "conf_score": det[1]
        }
        return render(request, "index.html", context)
    return render(request,"index.html")