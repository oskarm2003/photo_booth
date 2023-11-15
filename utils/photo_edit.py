from PIL import Image
import os
from shutil import rmtree


def crop_photo(url):
    
    try:
        with Image.open(url) as img:
            (filename, ext) = os.path.splitext(url)
            dw, dh = 160, 134 #desired w h
            (fw,fh) = img.size #file w h
            cropped = img.crop(((fw-dw)/2,(fh-dh)/2,(fw+dw)/2 ,(fh+dh)/2))
            cropped.save(url,'JPEG')
    except:
        raise Exception('no such file')


# input: 
#   file_urls - list of urls, ex: [1.jpg,2.jpg,3.jpg]; 
#   template_url - url of the template, ex: './templates/stars.png'
def fill_template(file_urls, template_url):
    
    if not hasattr(file_urls, "__len__" or issubclass(type(file_urls),str)):
        raise Exception('file_urls not a list')

    try:
        with Image.open(template_url) as template:
            for i in range(min(3, len(file_urls))):
                    with Image.open(file_urls[i]) as img:
                        # assuming image size 134x160
                        pos = (14,122 + i*(134 + 14))#,174,122 + (i*134+14) + 160)
                        template.paste(img, box=pos)

        template.save('./_cache/ready.jpg')
    except:
        raise Exception('failed to generate image')


def clear_cache():
    try:
        rmtree('./cache')
    except:
        raise Exception('failed to clear cache')

