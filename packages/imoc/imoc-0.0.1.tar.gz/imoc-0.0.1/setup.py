from setuptools import setup,find_packages


VERSION = '0.0.1'
DESCRIPTION = 'Image classifier model that automate every steps in image classification'
LONG_DESCRIPTION = '''This library can be used for any simple image classification problems, You only have to give the data path, #of epochs, and
if you have any model that you created you can give that also (if none given the model if use it's own model).
1. After importing the library create a object of it by providing the path of the data and other parameters.
2. Then call the create_model function with the object.
3. Then the library will starts to work starting with cleaning the data by checking for any unsupported or duplicated files
   and deleting them.
4. After cleanig it will preprocessing the images and splits it to train/test/validation, and it also plots the images 
   according to the classes
5. The if no model is provided it will create it's own model for traning.
6. And Starts to train for the #of epochs given (default=70).
7. You can use the funtion plot_performance() to plot the model loss and accuracy growth.
8. model_evaluation() function evaluate the model based on the test data.
9. And you can use the function predict() to predict any new values.
10. And to save the model use model_save() function'''
czx = 0

setup(
    name='imoc',
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=LONG_DESCRIPTION,
    author='Nikhil',
    author_email='thalappallinikhil@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires = ['tensorflow','opencv','matplotlib','numpy','imghdr'],
    keywords=['image detection','machine learning','computer visionn'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python" ,
    ],
    zip_safe=False)