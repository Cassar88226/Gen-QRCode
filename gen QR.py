# import modules
import qrcode
from PIL import Image
import argparse
import sys

from qrcode import main

# add Argument Parser
parser = argparse.ArgumentParser("Input URL(or Text) and Logo path")


# add Arguments
parser.add_argument('--url', type=str, default="",
                    help='URL')

parser.add_argument('--logo-path', type=str, default="",
                    help='Logo - optional') 

parser.add_argument('--text', type=str, default="",
                    help='Text')

# connect parser
args = parser.parse_args()


url = args.url

logo_path = args.logo_path

# if url is empty,
# exit the script
if not url:
    print("Please put the url argument")
    sys.exit(0)

def encode(url, logo_path, qr_path=None):
    # addingg URL or text to QRcode
    # taking image which user wants 
    # in the QR code center

    if logo_path:
        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            border=1
            )
    else:
        QRcode = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            border=1
            )

    QRcode.add_data(url)

    # generating QR code
    QRcode.make()

    # taking color name from user
    fill_color='black'
    back_color="white"

    # adding color to QR code
    QRimg = QRcode.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')

    # If logo-path is not None
    # Embed the logo image in QR
    if logo_path:
        logo = Image.open(logo_path)
        
        # taking base width
        basewidth = 100
        
        # adjust image size
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
        
        # set size of QR code
        pos = ((QRimg.size[0] - logo.size[0]) // 2,
            (QRimg.size[1] - logo.size[1]) // 2)
        
        QRimg.paste(logo, pos)

    QRimg.save(qr_path)
    
    print('QR code generated!')

def decode(file_path):
    
    import cv2
    
    # Create The Decoder    
    decoder = cv2.QRCodeDetector()
    
    # Load Your Data
    image = cv2.imread(file_path)
    
    # Decode and Print the required information
    link, data_points, straight_qrcode = decoder.detectAndDecode(image)
    
    print(link)



if __name__ == "__main__":    
    qr_path = 'QR Code+3.png'
    
    encode(url, logo_path, qr_path)
    
    # decode(qr_path)