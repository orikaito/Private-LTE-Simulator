import keras
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
# from keras.utils import to_categorical
from keras.layers.convolutional import Conv2D 
from keras.layers.convolutional import MaxPooling2D 
from keras.layers import Flatten 
from keras.datasets import mnist
from PIL import Image, ImageOps

(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(X_train.shape[0], 28, 28, 1).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 28, 28, 1).astype('float32')

X_train = X_train / 255 
X_test = X_test / 255 

y_train = keras.utils.np_utils.to_categorical(y_train)
y_test = keras.utils.np_utils.to_categorical(y_test)

num_classes = y_test.shape[1] 

def convolutional_model():
    model = Sequential()
    model.add(Conv2D(16, (5, 5), activation='relu', input_shape=(28, 28, 1)))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
    model.add(Conv2D(8, (2, 2), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2))) 
    model.add(Flatten())
    model.add(Dense(100, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy',  metrics=['accuracy'])
    return model

model = convolutional_model()
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=6, batch_size=200)#, verbose=2)

scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: {} \n Error: {}".format(scores[1], 100-scores[1]*100))

model.save('model.h5')

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
