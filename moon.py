import cv2
import numpy as np
from constants import *
from skimage import io
from keras.models import load_model


def stat_(pred):
    try:
        print(emotion[0] + '   : {0:.2f}'.format(pred.item(0)))
        print(emotion[1] + ' : {0:.2f}'.format(pred.item(1)))
        print(emotion[2] + '    : {0:.2f}'.format(pred.item(2)))
        print(emotion[3] + '   : {0:.2f}'.format(pred.item(3)))
        print(emotion[4] + '     : {0:.2f}'.format(pred.item(4)))
        print(emotion[5] + ': {0:.2f}'.format(pred.item(5)))
        print(emotion[6] + ' : {0:.2f}'.format(pred.item(6)))
    except:
        print('Failed Format')


def discord_er_(url):
    try:
        em = -1
        crit = 0
        pred = 0
        print(">> Received at discord_er_ with url:" + url)
        face_cascade = cv2.CascadeClassifier(casc_path)
        classifier = load_model(model_path)
        print(">> Downloading the image")
        image = io.imread(url)
        print(">> Download Successful\n>> Processing the image")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_color = image[y:y + h, x:x + w]
            face = np.expand_dims(cv2.resize(roi_color, (height,width)), 0)
            print(">> Evaluating the image")
            pred = classifier.predict(face)
            crit = 1
            em = int(np.argmax(pred))
            prob = np.max(pred)
            # label = np.argmax(pred)
            # text = emotion[label] + ': ' + str(prob)
    except:
        msg = discord_(status="fail")
        return msg
    else:
        if(crit!=0):
            stat_(pred=pred)
            msg = discord_(status="success",em=em,prob=prob, url=url)
        else:
            msg = discord_(status="success", em=-1)
        return msg


def discord_(status, em=0,url='',prob=0):
    if status == "fail":
        msg = 'Failed Evaluation'
    elif em == -1:
        msg = "Couldn't find a Face.\nMake sure head is complete and not cropped or covered in any way."
    else:
        msg = "The person in the image has a {0:.2f}".format(prob)+" probability of being "+emotion[em]
    return msg


def main():
    test_image = "https://www.thefamouspeople.com/profiles/images/og-billie-joe-armstrong-868.jpg"
    print(discord_er_(test_image))


if __name__ == '__main__':
    main()
