#/usr/bin/python
import os
import json
from fastapi import FastAPI, File, UploadFile
from PIL import Image, ImageEnhance
from tesserocr import PyTessBaseAPI, RIL



app = FastAPI()


@app.post("/get_ocr")
async def image(image: UploadFile = File(...), json_boxes : str = """{"name": 		{"x":0,"y":0,"w":300,"h":300} }"""):
    print(image.file, json_boxes)
    
    try:
        os.mkdir("images")
        print(os.getcwd())
    except Exception as e:
        print(e) 
    file_name = os.getcwd()+"/images/"+image.filename.replace(" ", "-")
    with open(file_name,'wb+') as f:
        f.write(image.file.read())
        f.close()
    
    results = {}
    scale_factor = 2
    image = Image.open(file_name) #TODO: remove store to FS!!!
    (width, height) = (image.width * scale_factor, image.height * scale_factor)
    image = image.resize((width, height))
    
    image = image.convert('L').convert('RGB')
    
    enhancer = ImageEnhance.Contrast(image)
    factor_contrast = 1.5
    image = enhancer.enhance(factor_contrast)
    
    enhancer = ImageEnhance.Brightness(image)
    factor_brightness = 0.6 #darkens the image
    image = enhancer.enhance(factor_brightness)
    
    with PyTessBaseAPI() as api:
        api.SetImage(image)
        #boxes = api.GetComponentImages(RIL.TEXTLINE, True)
        #print('Found {} textline image components.'.format(len(boxes)))
        boxes =json.loads(json_boxes) 
        print(boxes)
        for key, box in  boxes.items():
            # im is a PIL image object
            # box is a dict with x, y, w and h keys
            api.SetRectangle(box['x']*scale_factor, box['y']*scale_factor, box['w']*scale_factor, box['h']*scale_factor)
            ocrResult = api.GetUTF8Text()
            conf = api.MeanTextConf()
            print(key)
            
            print(u"Box[{0}]: x={x}, y={y}, w={w}, h={h}, "
                  "confidence: {1}, text: {2}".format(key, conf, ocrResult, **box))
            results[key] = ocrResult

    return results
