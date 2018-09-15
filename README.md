# Smart-Colors

### Description

* Web page that identifies clothes from webcam and provides color combinations and fashion advice @ hackshanghai-2018

### Group

* Ziyi Wang, Weihan Li, Hanyu Wang, Naifeng Zhang

### Introduction

* Creates web page that detects main objects from webcam, use the main colors of the clothes the user wears to present color combinations and suggested clothes to go with. This project uses python to develop, django for server, sqlite for database, beautifulsoup for webscraping fashing advices and darrknet for object detection.

### Run

Make sure Python 3 and all required packages are installed
Clone darknet following the instruction from https://pjreddie.com/darknet/yolo/
Clone darknetpy from https://github.com/danielgatis/darknetpy and follow instructions to set-up
cmd to mysite
python manage.py runserver
open 127.0.0.0:8000\findColors in browser
enable webcam
### Tools

* Python, HTML, CSS, JavaScript
Django, sqlite, beautifulsoup, darknet
### Citation
* Darknet: https://pjreddie.com/darknet/yolo/ YOLO(You Only Look Once) from Darknet
* Darknetpy: https://github.com/danielgatis/darknetpy Python wrapper for Darknet
* YOLO: @article{yolov3,
  title={YOLOv3: An Incremental Improvement},
  author={Redmon, Joseph and Farhadi, Ali},
  journal = {arXiv},
  year={2018}
}
