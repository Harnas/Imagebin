# Description
**Imagebin** is an open source software project for fast share uncompressed images. 
Also implements AI based on Mobilenetv2 neural net trained on imagenet datasets, what mean is ultra fast and can recognize 1000 categories. 
This power is used for quick auto-tagging.

Used technologies:
```
- Django
- Tensorflow
- Keras
- SQLite3
```
Before first run:
```
conda install keras
pip install -r requirements.txt
python manage.py makemigrations images
python manage.py migrate
```
To run app:
```
- python manage.py runserver
```
And navigate to: http://127.0.0.1:8000/image/


