#/usr/bin/python
from fastapi import FastAPI, File, UploadFile

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
   file = jsonable_encoder({"imagePath":file_name})
   new_image = await add_image(file)
   return {"filename": new_image}
