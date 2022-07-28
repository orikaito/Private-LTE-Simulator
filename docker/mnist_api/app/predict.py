from email.mime import image
from imp import load_module
import numpy as np
from keras import models
from PIL import Image, ImageOps

model = models.load_model('./model.h5')

def print_array(array):
    for j in array[0]:
        for k in j:
            k = k[0]
            if k == 0:
                print('  ',end='')
            elif k<=9:
                print('  '+str(k),end='')
            elif k>=10 and k<100:
                print(' '+str(k),end='')
            else:
                print(k,end='')
        print()

for i in range(10):
    image1 = "./mnist_test/"+str(i)+".png"
    img = Image.open(image1)
    img = img.convert("L")
    img = ImageOps.invert(img)
    size = 28,28
    img = img.resize(size, Image.ANTIALIAS)
    # img.save('output-'+str(i)+'.png')
    img = np.reshape(img, (28,28,1))
    im2arr = np.array(img)
    im2arr = im2arr.reshape(1,28,28,1)
    print_array(im2arr)
    predict = model.predict(im2arr,verbose=0)
    print(np.argmax(predict,axis=1))
    print(str(predict[0]))