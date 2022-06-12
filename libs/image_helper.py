import os
import re
from typing import Union
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from flask_uploads import UploadSet, IMAGES 

IMAGE_SET = UploadSet("images", IMAGES) #set name and allowed extensions

def save_image(image:FileStorage, folder:str=None, name:str=None)-> str:
    """ Take fileStorage and saves it to a folder """
    return IMAGE_SET.save(image, folder, name)


def get_path(filename:str = None, folder:str = None) ->str:
    """ Take image name and folder and return fill path """
    return IMAGE_SET.path(filename, folder)


def find_image_any_format(filename:str = None, folder:str = None) -> Union[str, None]:
    """ Take FileStorage and returns animage on any of the acepted format."""
    for _format in IMAGES:
        image = f"{filename}.{_format}"
        image_path = IMAGE_SET.path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path
    return None


def _retreive_filename(file:Union[str, FileStorage])->str:
    """ Take FileStorage and return the file name.
    Allows our functions to call this with both file names and
    FileStorages and always get back a file name."""
    if isinstance(file, FileStorage):
        return file.filename
    return file


def is_filename_safe(file:Union[str, FileStorage])-> bool:
    """ Check our regex and return whether the string matches or not. """
    filename = _retreive_filename(file)
    allowed_format = "|".join(IMAGES)  # png|svg|jpe|jpg|jpeg
    regex = f"^[a-zA-z0-9][a-zA-z0-9_()-\.]*\.({allowed_format})$"
    return re.match(regex, filename) is not None


def get_basename(file:Union[str, FileStorage])->str:
    """ Return full name of image in the path 
    get_basename('some/folder/image.jpg') renturns 'image.jpg'"""
    filename = _retreive_filename(file)
    return os.path.split(filename)[1]


def get_extension(file:Union[str, FileStorage])->str:
    """ Return file extension 
    get_extension('image.jpg') returns '.jpg'"""
    filename = _retreive_filename(file)
    return os.path.splitext(filename)[1]