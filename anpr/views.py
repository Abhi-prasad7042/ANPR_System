from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from paddleocr import PaddleOCR, draw_ocr
import cv2
import os
import numpy as np
import torch
import re
from PIL import Image, ImageDraw,ImageFont
from io import BytesIO
import base64
import json

file_path = os.path.join(os.path.dirname(__file__), 'best.pt')
model = torch.hub.load('ultralytics/yolov5', 'custom', path=file_path, force_reload=True)

def draw_bounding_boxes(image_path, dataframe):
    # Open the image
    img = Image.open(image_path)
    
    # Create a draw object
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 24)
    # Iterate over the DataFrame rows
    for index, row in dataframe.iterrows():
        # Extract bounding box coordinates and class name
        xmin = row['xmin']
        ymin = row['ymin']
        xmax = row['xmax']
        ymax = row['ymax']
        class_name = row['name']
        
        # Define the bounding box coordinates
        bbox = [(xmin, ymin), (xmax, ymax)]
        
        # Draw the bounding box rectangle
        if class_name == "Vehicle":
            draw.rectangle(bbox, outline="red", width=4)
        else:
            draw.rectangle(bbox, outline="yellow", width=4)
        
        # Add text label
        if class_name == "Vehicle":
            draw.text((xmin+5, ymax-30), class_name, fill="red", font=font)
        else:
            draw.text((xmin+20, ymax), class_name, fill="yellow", font=font)
        
    
    return img


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
    ocr = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)
    img = cv2.imread(src)
    img1 = model(img)
    df = img1.pandas().xyxy[0]
    
    results = []
    
    for index, row in df[df["name"] == "NumberPlate"].iterrows():
        xmin = int(row["xmin"]) + 15
        xmax = int(row["xmax"])
        ymin = int(row["ymin"])
        ymax = int(row["ymax"])

        cropped_image = img[ymin:ymax, xmin:xmax]
        shrp_image = image_process(cropped_image)

        result = ocr.ocr(shrp_image, cls=True)
        if result:
            if len(result[0]) == 1:
                text, conf_score = result[0][0][1][0], result[0][0][1][1]
                text = re.sub(r"[^A-Z0-9- ]", "", text).strip("- ")
                results.append([text, conf_score])

            elif len(result[0]) == 2:
                text1, conf_score1 = result[0][0][1][0], result[0][0][1][1]
                text2, conf_score2 = result[0][1][1][0], result[0][1][1][1]
                text = text1 + text2
                # text = re.sub(r"[^A-Z0-9- ]", "", text).strip("- ")
                conf_score = np.mean([conf_score1, conf_score2])
                results.append([text, conf_score])
        else:
            results.append(["not found", 0])
    
    return [results, df]



# Create your views here.
def index(request):
    if request.method == 'POST':
        image = request.FILES.get("image")
        instance = ImageOCR.objects.create(image=image)
        image_url = os.path.join('/media/', instance.image.name)
        file_path = os.path.join("number", instance.image.name)  
        file_path = file_path.replace("\\", "/")  # Correcting the filepath
        
        # Call the function to draw bounding boxes
        if 'anpr' in request.POST:
            det = ocr(file_path)
            context = {
                'image_url': image_url,
                'result': det[0],  # Pass the image with bounding boxes to HTML
                'score': det[1]
            }
            return render(request, "index.html", context)
        elif 'detection' in request.POST:
            results, det = detection(file_path)
            img_with_boxes = draw_bounding_boxes(file_path, det)
            # Convert PIL image to bytes for displaying in HTML
            img_io = BytesIO()
            img_with_boxes.save(img_io, format='JPEG')
            img_io.seek(0)
            img_bytes = img_io.getvalue()
            img_base64 = "data:image/jpeg;base64," + base64.b64encode(img_bytes).decode()

            context = {
                'image_url': image_url,
                'image_base64': img_base64,  # Pass the image with bounding boxes to HTML
                'result': results,
                'result_json': json.dumps(results)
            }
            return render(request, "index.html", context)
        
    return render(request, "index.html")