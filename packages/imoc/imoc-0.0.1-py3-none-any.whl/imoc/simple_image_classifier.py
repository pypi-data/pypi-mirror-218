
import tensorflow as tf
import os
import cv2
import imghdr
import numpy as np
from matplotlib import pyplot as plt


class Imageclassification:
    
    def __init__(self,path,model=None,epochs=70):
        self.data_dir = path
        self.train_data = None
        self.test_data = None
        self.validation_data = None
        self.model = model
        self.epochs = epochs
        self.history = None
        self.class_names = None

                    
    def data_cleaning(self):
        #Unsupported files
        for image_class in os.listdir(self.data_dir):
            for image in os.listdir(os.path.join(self.data_dir,image_class)):
                image_path = os.path.join(self.data_dir,image_class,image)
                try:
                    img = cv2.imread(image_path)
                    tip = imghdr.what(image_path)
                    if tip not in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
                        print('Image not in ext list {}'.format(image_path))
                        os.remove(image_path)
                except Exception as e:
                    print("Issue with image {}".format(image_path))
                    
        #duplicate images
        for image_class in os.listdir(self.data_dir):
            duplicates = []
            hash_keys = dict()
            for image in os.listdir(os.path.join(self.data_dir,image_class)):
                if os.path.isfile(image):
                    with open(image,'rb') as f:
                        filehash = hashlib.md5(f.read()).hexdigest()
                    if filehash not in hash_keys:
                        hash_keys[filehash] = index
                    else:
                        duplicates.append((index,hash_keys[filehash]))
            for index in duplicates:
                os.remove(filelist[index[0]])
                print('{} duplicates removed from {}'.format(len(duplicates),image_class))
        
        #Tensorflow Unsupported files
        for image_class in os.listdir(self.data_dir):
            for image in os.listdir(os.path.join(self.data_dir,image_class)):
                image_path = os.path.join(self.data_dir,image_class,image)
                with open(image_path, 'rb') as f:
                    image_data = f.read()
                try:
                    image = tf.image.decode_image(image_data)
                except:
                    print(image_file)
                    print("unspported")
                    os.remove(image_path)
                    
    def setup_data(self):
        data = tf.keras.utils.image_dataset_from_directory(self.data_dir)
        self.class_names = data.class_names
        print("The classes are {}".format(self.class_names))
        data_iterator = data.as_numpy_iterator()
        batch = data_iterator.next()
        fig, ax = plt.subplots(ncols=len(self.class_names))
        i,idx,classes=0,0,set()
        while i<len(self.class_names):
            if batch[1][idx] not in classes:
                img = batch[0][idx]
                ax[i].imshow(img.astype(int))
                ax[i].set_title(self.class_names[batch[1][idx]])
                i+=1
            classes.add(batch[1][idx])
            idx+=1
        fig.suptitle("Pictures and Respected Classes")
        plt.show()
            
        data = data.map(lambda x,y:(x/255,y))
        
        train_size = int(len(data)*.7)
        validation_size = int(len(data)*.2)
        test_size = int(len(data)*.1) 
        
        
        self.train_data = data.take(train_size)
        self.validation_data = data.skip(train_size).take(validation_size)
        self.test_data = data.skip(train_size+validation_size).take(test_size)
        
        print("Whole Data Size= {}, Train Size = {}, Test Size = {}, Validation Size = {}".format(len(data),len(self.train_data),
                                                                                                  len(self.validation_data),len(self.test_data)))
        
    
    def model_setup(self,output_num):
        from tensorflow.keras.models import Sequential 
        from tensorflow.keras import layers

        model = tf.keras.Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3)))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(128, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(128, (3, 3), activation='relu'))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Flatten())
        model.add(layers.Dense(512, activation='relu'))
        model.add(layers.Dropout(0.5))  
        model.add(layers.Dense(256, activation='relu'))
        
        if output_num <= 2:
            model.add(layers.Dense(1,activation='sigmoid'))
        else:
            model.add(layers.Dense(output_num,activation='softmax'))
        
        if output_num <=2:
            model.compile('adam',loss=tf.losses.BinaryCrossentropy(),metrics=['accuracy'])
        else:
            model.compile('adam',loss=tf.losses.sparse_categorical_crossentropy,metrics=['accuracy'])
            
        return model
        
    def create_model(self):
        print("Cleaning the images")
        self.data_cleaning()
        print("Cleaning is Done")
        print("Next process is Data Collection and Data Preprocessing")
        self.setup_data()
        print("Process Completed")
        print("Model Training")
        if self.model == None:
            self.model = self.model_setup(len(self.class_names))
        log_dir = 'new_log'
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir = log_dir)
        print("Training started")
        from datetime import datetime
        start = datetime.now()
        self.history = self.model.fit(self.train_data,epochs=self.epochs,validation_data=self.validation_data,callbacks=[tensorboard_callback])
        print("Model trainng ended, time taken to train = {} ".format(datetime.now()-start))
    
    def plot_model_performance(self):
        fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(10,5)) 
        
        ax[0].plot(self.history.history['loss'],color='teal',label='loss')
        ax[0].plot(self.history.history['val_loss'],color='orange',label='val_loss')
        ax[0].set_title('Loss')
        ax[0].legend(loc='upper left')
        
        ax[1].plot(self.history.history['accuracy'],color='teal',label='Accuracy')
        ax[1].plot(self.history.history['val_accuracy'],color='orange',label='val_accuracy')
        ax[1].set_title('Accuracy')
        ax[1].legend(loc='upper left')
        
        fig.suptitle("Model Performance")
        plt.show()
        
    def model_evaluation(self):
        from tensorflow.keras.metrics import Precision,Recall
        pre = Precision()
        re = Recall()
        for batch in self.test_data.as_numpy_iterator():
            print("sd")
            X, y = batch
            y_pred = self.model.predict(X)
            y_pred = np.argmax(y_pred,axis=1)
            pre.update_state(y,y_pred)
            re.update_state(y,y_pred)
        precision = pre.result().numpy()
        recall = re.result().numpy()
        if len(self.class_names)>2:
            print("Precision {}\nRecall {}\nF1 Score {}".format(precision,recall,2 * (precision * recall) / (precision + recall)))
        else:
            print("Precision {}\nRecall {}\n".format(precision,recall))
        
    def predict(self,image):
        img = cv2.imread(image)
        plt.imshow(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        plt.show()
        resize = tf.image.resize(img,(256,256))
        y_pred = self.model.predict(np.expand_dims(resize/255,0))
        if len(self.class_names)>2:
            idx = np.argmax(y_pred)
            print("The image belongs to {}".format(self.class_names[idx]))
        else:
            if y_pred>0.5:
                print("The image belongs to {}".format(self.class_names[1]))
            else:
                print("The image belongs to {}".format(self.class_names[0]))
                
    def model_save(self,name):
        self.model.save(name+'.h5')
        




