from PIL import Image
import os
from shutil import rmtree


def crop_photo(url, new_name=""):
    
    try:
        with Image.open(url) as img:

            (_, ext) = os.path.splitext(url)

            # crop first to avoid image stretch
            (fw,fh) = img.size #file w h
            current_ratio = fw/fh
            
            # desired ratio: 1 : 1.2 <=> fw = 1.2*fh
            d_ratio = 1.2
            dw, dh = fw, fh # desired w h (temporary)
            
            
            if current_ratio > d_ratio:
                dw = int(fh * d_ratio)
            else:
                dh = int(fw/d_ratio)
            
            modified = img.crop(((fw-dw)//2,(fh-dh)//2,(fw+dw)//2,(fh+dh)//2))
            
            # resize
            height = 400
            modified = modified.resize((int(height * d_ratio), height))

            # change name
            if not new_name == "":
                tmp = url.split('/')
                if len(tmp) == 1:
                    tmp = url.split('\\')
                url = ""
                for i in range(len(tmp)-1):
                    url = os.path.join(url, tmp[i])
                url = os.path.join(url, new_name+ext)

            modified.save(url, 'JPEG')
    except:
        raise Exception('no such file')


# input: 
#   file_urls - list of urls, ex: [1.jpg,2.jpg,3.jpg]; 
#   template_url - url of the template, ex: './templates/stars.png'
def fill_template(file_urls, template_url):
    
    if not hasattr(file_urls, "__len__" or issubclass(type(file_urls),str)):
        raise Exception('file_urls is not a list')

    try:
        with Image.open(template_url) as template:
            template = template.convert('RGB')
            for i in range(max(3, len(file_urls))):
                    with Image.open(file_urls[i]) as img:
                        (cw,ch) = img.size
                        (pw,ph) = template.size
                        # assuming image size 134x160
                        gap = (pw-cw)//2
                        pos = (gap,ph - (gap//2+ch)*(i+1))#,174,122 + (i*134+14) + 160)
                        # pos = (14,122 + i*(134 + 14))#,174,122 + (i*134+14) + 160)
                        template.paste(img, box=pos)

        template.save('./_cache/ready.jpg')
    except:
        raise Exception('failed to generate image')


# double given image
def double_join(file_path):
    try:
        with Image.open(file_path) as image:
            (fw, fh) = image.size
            blank = Image.new(mode="RGB", size=(int(2*fw),int(fh)))
            blank.paste(image, (0,0))
            blank.paste(image, (image.size[0],0))
            blank.save(file_path)
    except:
        raise Exception('failed to join images')


def clear_cache():
    try:
        rmtree('./_cache')
        os.mkdir('./_cache')
    except:
        raise Exception('failed to clear cache')