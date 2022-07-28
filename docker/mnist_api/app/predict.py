from imp import load_module
import numpy as np
from keras import models
from PIL import Image

model = models.load_model('./model.h5')

for i in range(10):
    image1="./data/"+str(i)+".jpg"
    im = Image.open(image1)
    img = im.convert("L")
    img = np.resize(img, (28,28,1))
    im2arr = np.array(img)
    im2arr = im2arr.reshape(1,28,28,1)
    predict = model.predict(im2arr,verbose=0)
    print(np.argmax(predict,axis=1))
    print(str(predict[0]))