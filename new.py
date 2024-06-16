import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import string
import ssl
import webbrowser
import tempfile
import os

# Backend functions
def genData(data):
    newd = []
    for i in data:
        newd.append(format(i, '08b'))
    return newd

def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
                            imdata.__next__()[:3] +
                            imdata.__next__()[:3]]
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode_image():
    img = filedialog.askopenfilename(title="Select Image",
                                      filetypes=(("PNG files", "*.png"),
                                                 ("JPEG files", "*.jpg;*.jpeg"),
                                                 ("All files", "*.*")))
    image = Image.open(img, 'r')

    data = tk.simpledialog.askstring("Hide Text", "Enter text to hide:")
    if len(data) == 0:
        raise ValueError('Data is empty')

    newimg = image.copy()
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(data.encode())  # Store encrypted text

    # Generate random OTP
    otp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    encode_enc(newimg, encrypted_text)

    new_img_name = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=(("PNG files", "*.png"), ("All files", "*.*")))

    if new_img_name:
        newimg.save(new_img_name)
        email = simpledialog.askstring("Email Address", "Enter your email address:")
        if email:
            send_email(email, key.decode(), otp)
            messagebox.showinfo("Success",
                                "Text hidden and image saved successfully. Key and OTP sent to email.")
        else:
            messagebox.showwarning("Warning", "Email address is required.")
    else:
        messagebox.showwarning("Warning", "Save path is required.")


def send_email( recipient_email, key, otp):
    sender_email = "keertan224@gmail.com"  # Update with your email
    password = "xtutydhjpgorktpa"
    # Update with your email password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Key and OTP for Image Steganography"

    body = f"Here is the key to decrypt the hidden text: {key}\n\nOTP: {otp}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {str(e)}")
def decode_image():
    try:
        image_path = filedialog.askopenfilename(title="Select Image to Extract Text")
        if image_path:
            # Key and OTP verification from email
            key = simpledialog.askstring("Enter Key", "Enter the key received in email:")
            if key:
                otp = simpledialog.askstring("Enter OTP", "Enter the OTP received in email:")
                if otp:
                    image = Image.open(image_path)
                    decoded_data = decode(image)

                    # Fernet decryption
                    cipher_suite = Fernet(key.encode())
                    # Code to decrypt text from image
                    extracted_text = cipher_suite.decrypt(decoded_data).decode()
                    messagebox.showinfo("Decoded Data", extracted_text)
                else:
                    messagebox.showwarning("Warning", "OTP is required.")
            else:
                messagebox.showwarning("Warning", "Key is required.")


    except Exception as e:
        messagebox.showerror("Error", str(e))

def decode(image):
    data = ''
    imgdata = iter(image.getdata())
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                            imgdata.__next__()[:3] +
                            imgdata.__next__()[:3]]
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data
def project_info():
    file_html = '''  
    <!DOCTYPE html>
    <html>
    <head>
    <title>Project Details</title>
    <style>
    body{  
    background-color:sandybrown;
    font-size:17px;
    }
    table, th, td {
      border: 1px solid black;
      border-collapse: collapse;
      border-color:dark black;
    }
    </style>
    </head>
    <body>
       <h2> <center>PROJECT INFORMATION</center> </h2>        
    <center><h1>Image Steganography</h1></center>
    <center> <table style="width:40%">
      <tr>
        <th><b>Project Details</b></th>
        <th>Value</th> 
      </tr>
      <tr>
        <td>Project Name</td>
        <td>Image Steganography</td>
      </tr>
      <tr>
        <td>Project Description</td>
        <td>Implementing to conceal secret data within an image without altering its visual appearance.</td>
      </tr>
      <tr>
        <td>Project Start Date</td>
        <td>17-02-2024</td>
      </tr>
      <tr>
        <td>Project End Date</td>
        <td>17-03-2024</td>
      </tr>
      <tr>
        <td>Project Status</td>
        <td><b>Completed</b></td>
      </tr>
    </table>
    </center>
    <h3><center>Developer Details</center></h3>
    <center> <table style="width:40%">
      <tr>
        <th><b>Name</b></th>
        <th>Email</th> 
      </tr>
      <tr>
        <td>ST3IS#6108</td>
        <td>jyothish@gmail.com</td>
      </tr>
       <tr>
        <td>ST3IS#6110</td>
        <td>sathv@gmail.com</td>
      </tr>
      <tr>
        <td>ST3IS#6111</td>
        <td>keertan@gmail.com</td>
      </tr>
      <tr>
        <td>ST3IS#6112</td>
        <td>devisrinivas@gmail.com</td>
      </tr>
      <tr>
        <td>ST3IS#6113</td>
        <td>vineetha@gmail.com</td>
      </tr>
    </table>
    </center>

    </table>
    </center>
    <h3><center>Company Details</center></h3>
    <center> <table style="width:40%">
      <tr>
        <th><b>Company</b></th>
        <th>Contact Email</th> 
      </tr>
      <tr>
        <td>Name</td>
        <td>Anonymous Cyber Solutions</td>
      </tr>
      <tr>
        <td>Email</td>
        <td>contact@stegnos.com</td>
      </tr>
    </table>
    </center>

    </body>
    </html>'''

    # Saving the data into the HTML file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html') as temp_file:
        temp_file.write(file_html)
        temp_file_path = temp_file.name

    # Opening HTML file in a web browser window
    webbrowser.open("file://" + os.path.realpath(temp_file_path))

root = tk.Tk()
root.title("Image Steganography")
root.geometry("449x396")
root.configure(bg="black")
label_header = tk.Label(root, text="Image Steganography", font=("Helvetica", 16), bg="black", fg="white")
label_header.pack(pady=10)

frame_buttons = tk.Frame(root, bg="grey")
frame_buttons.pack(pady=10)

button_project_info = tk.Button(frame_buttons, text="Project Info", bg="red", fg="white",
                                command=project_info,font=("Arial", 12, "bold"), width=10)
button_project_info.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

lock_image = Image.open("lock_image.png")
lock_image = lock_image.resize((200, 200))
lock_image = ImageTk.PhotoImage(lock_image)
lock_label = tk.Label(image=lock_image, bg="black")
lock_label.pack()

frame_buttons = tk.Frame(root, bg="grey")
frame_buttons.pack(pady=10)

button_hide_text = tk.Button(frame_buttons, text="Hide Text", font=("Arial", 12, "bold"), bg="red", fg="white",
                             command=encode_image, width=10)
button_hide_text.grid(row=1, column=0, padx=10, pady=10)

button_extract_text = tk.Button(frame_buttons, text="Extract Text", bg="red", fg="white", command=decode_image,
                                font=("Arial", 12, "bold"), width=10)
button_extract_text.grid(row=1, column=1, padx=10, pady=10)

root.mainloop()