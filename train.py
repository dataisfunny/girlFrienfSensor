
# coding: utf-8

# In[1]:


from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import cv2, numpy as np, os.path
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model



class Model(object):

    FILE_PATH = './faces6.h5'

    def __init__(self):
        self.model = None

    def train(self, batch_size, classes,epochs):
        print (classes)
        #self.batch_size=batch_size
        #self.epochs=epochs
        self.model = Sequential()
        self.model.add(Conv2D(32, (3, 3), input_shape=(3, 150, 150)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Conv2D(32, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))
        
        self.model.add(Conv2D(64, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Dropout(0.25))

        self.model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
        self.model.add(Dense(1000))
        self.model.add(Activation('relu'))
        self.model.add(Dense(classes))
        self.model.add(Activation('softmax'))
        self.model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
        self.model.summary()
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)
        test_datagen = ImageDataGenerator(rescale=1./255)
        train_generator = train_datagen.flow_from_directory(
            'data/train',  # this is the target directory
            target_size=(150, 150),  # all images will be resized to 150x150
            batch_size=batch_size,
            class_mode='categorical')  # since we use binary_crossentropy loss, we need binary labels

        
        validation_generator = test_datagen.flow_from_directory(
            'data/validation',
            target_size=(150, 150),
            batch_size=batch_size,
            class_mode='categorical')

        steps_per_epoch=5000 // batch_size
        validation_steps=400 // batch_size
        
        
        self.model.fit_generator(
            generator=train_generator,
            steps_per_epoch=steps_per_epoch,
            epochs=epochs,
            validation_data=validation_generator,
            validation_steps=validation_steps)
        
  

    def save(self, file_path=FILE_PATH):
        print('Model Saved.')
        self.model.save(file_path)

    def load(self, file_path=FILE_PATH):
        print('Model Loaded.')
        self.model = load_model(file_path)

    def predict(self, image):
        
        image=cv2.resize(image,(150,150),interpolation=cv2.INTER_CUBIC)
        #print(image.shape)
        image=img_to_array(image)
        #print(image.shape)
        image = image.reshape((1,) + image.shape)
        #print(image.shape)
        image = image.astype('float32')
        image /= 255
        result = self.model.predict_proba(image)
        #print(result)
        result = self.model.predict_classes(image)

        return result
        


if __name__ == '__main__':
    model = Model()
    fname=model.FILE_PATH
    if os.path.isfile(fname) is True: 
        #model.load()
        print("模型已存在")
    else :
        print("開始訓練")
        model.train(batch_size=32, classes=8,epochs=15)
        model.save()
        
        

    


# In[2]:



'''
model = Model()
image = cv2.imread('./data/train/5/8.jpg')

image = image[:,:,::-1]
model.load()
model.predict(image)
print(model.predict(image))

'''

