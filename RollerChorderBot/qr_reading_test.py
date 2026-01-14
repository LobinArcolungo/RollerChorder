import cv2
import numpy as np

#image = "/Users/maclobin/Downloads/Telegram Desktop/photo_2022-09-08_13-15-02.jpg"
image = "/Users/maclobin/Downloads/Telegram Desktop/photo_2022-09-08_12-34-17.jpg"

def read_qr_code(filename):
    """Read an image and read the QR code.
    
    Args:
        filename (string): Path to file
    
    Returns:
        qr (string): Value from QR code
    """
    img = cv2.imread(filename)
    y=80
    x=0
    h=368
    w=368
    crop_img = img[y:y+h, x:x+w]
    
    img_encode = cv2.imencode('.png', crop_img)[1]
    data_encode = np.array(img_encode)
  
    # Converting the array to bytes.
    byte_encode = data_encode.tobytes()
    crop_img = cv2.imdecode(data_encode, 1)
    cv2.imshow("cropped", crop_img)
    cv2.waitKey(0)
    crop_img = cv2.resize(crop_img,(150,150),interpolation=cv2.INTER_AREA)
    cv2.imshow("cropped", crop_img)
    

    cv2.waitKey(0)

    try:
        print("try")
        img = cv2.imread(filename)
        detect = cv2.QRCodeDetector()
        value, points, straight_qrcode = detect.detectAndDecode(img)
        print("tried: ",value)
        return value
    except:
        return "the reading of QR code has been unsuccesful"

print(read_qr_code(image))