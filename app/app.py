#/usr/bin/python
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from tesserocr import PyTessBaseAPI, RIL



app = FastAPI()


@app.post("/get_ocr")
async def image(image: UploadFile = File(...), json : str = "{'name':[x,y,w,h]}"):
    print(image.file, json)
    
    # print('../'+os.path.isdir(os.getcwd()+"images"),"*************")
    try:
        os.mkdir("images")
        print(os.getcwd())
    except Exception as e:
        print(e) 
    file_name = os.getcwd()+"/images/"+image.filename.replace(" ", "-")
    with open(file_name,'wb+') as f:
        f.write(image.file.read())
        f.close()
    
    
    image = Image.open(file_name) #TODO: remove store to FS!!!
    with PyTessBaseAPI() as api:
        api.SetImage(image)
        boxes = api.GetComponentImages(RIL.TEXTLINE, True)
        print('Found {} textline image components.'.format(len(boxes)))
        for i, (im, box, _, _) in enumerate(boxes):
            # im is a PIL image object
            # box is a dict with x, y, w and h keys
            api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
            ocrResult = api.GetUTF8Text()
            conf = api.MeanTextConf()
            print(u"Box[{0}]: x={x}, y={y}, w={w}, h={h}, "
                  "confidence: {1}, text: {2}".format(i, conf, ocrResult, **box))
        
        
    file = jsonable_encoder({"imagePath":file_name})
    new_image = await add_image(file)
    return {"filename": new_image}
