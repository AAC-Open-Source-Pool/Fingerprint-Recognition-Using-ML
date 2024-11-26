from keras.models import load_model
import cv2
import numpy as np
from keras.utils import to_categorical
import os
from skimage.metrics import structural_similarity

IdModel = load_model("IdModel.h5")
FingerModel = load_model("FingerModel.h5")
#prevModel = load_model("CNN_MODEL.h5")


img_size = 96
def load_data(path, train=True):
    print("Loading data from: ", path)
    data = []
    for img in os.listdir(path):
        img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)

        img_resize = cv2.resize(img_array, (img_size, img_size))
        user_img = np.array(img_resize).reshape(-1, img_size, img_size, 1)
        user_img = user_img/255.0

        data.append([IdModel.predict(user_img), FingerModel.predict(user_img)])
        
    return data


def checkSimilarity(inp_img , DB_img):
    img00 = cv2.imread(inp_img, 0)
    img01 = cv2.imread(DB_img, 0)
    ssim , diff = structural_similarity(img00, img01, full=True)
    return ssim

# def extractFeatures:
def verifyUser(id):
    img_size = 96

    user_img = r"C:\ONE_DRIVE_DATA\Desktop\GRIET\AAC\PROJECT\CODE\SoCofing_Model\Input"  # Input path for user image
    DB_path = r'C:\ONE_DRIVE_DATA\Desktop\GRIET\AAC\PROJECT\INPUT\SOCOFing\Real'         # Database path for fingerprint images

    inp_data = load_data(user_img, train=True)

    # "2__F_Right_little_finger.BMP" format for fingerprint image files
    Predicted_ID = np.argmax(inp_data[0][0]) + 1
    Predicted_Finger = np.argmax(inp_data[0][1])
    if Predicted_Finger > 4:
        Predicted_Hand = "Right"
    else:
        Predicted_Hand = "Left"

    fingers = ["little", "ring", "middle", "index", "thumb", "little", "ring", "middle", "index", "thumb"]

    DB_paths = [
        DB_path + '\\' + str(Predicted_ID) + "__" + "M_" + Predicted_Hand + "_" + fingers[int(Predicted_Finger)] + "_finger.BMP",
        DB_path + '\\' + str(Predicted_ID) + "__" + "F_" + Predicted_Hand + "_" + fingers[int(Predicted_Finger)] + "_finger.BMP"
    ]

    if id == Predicted_ID:
        DB_paths = [
            DB_path + '\\' + str(Predicted_ID) + "__" + "M_" + Predicted_Hand + "_" + fingers[int(Predicted_Finger)] + "_finger.BMP",
            DB_path + '\\' + str(Predicted_ID) + "__" + "F_" + Predicted_Hand + "_" + fingers[int(Predicted_Finger)] + "_finger.BMP"
        ]
        try:
            if checkSimilarity(DB_paths[0], user_img + r"\InputImage.BMP") > 0.6:
                return "Access Granted"
            else:
                return "Access Denied"
        except:
            try:
                if checkSimilarity(DB_paths[1], user_img + r"\InputImage.BMP") > 0.6:
                    return "Access Granted" 
                else:
                    return("Access Denied")
            except:
                return("ERROR ACCESSING DB")
    else:
        return("Incorrect ID")


ALLOWED_EXTENSIONS = {'bmp', 'jpg', 'jpeg','png'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
