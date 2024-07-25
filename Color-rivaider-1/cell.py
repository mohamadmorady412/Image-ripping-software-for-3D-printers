# کتابخانه های مورد نیاز
import cv2
import numpy as np
import glob
import os

# ورودی ها شامل file_path, result_path , ".Extension"(png,jpg or Both), Cutting_Range
file_path = r"C:\Users\takkaj\Desktop\job\Image_prossing\images"
result_path = r"C:\Users\takkaj\Desktop\job\Image_prossing\result"
exten = "png"
Cutting_Range = 4

# بررسی اینکه فایل عکس وجود دارد یا خیر
if os.path.exists(file_path):
    # بررسی اینکه فرمت فایل png است یا خیر
    filename, extension = os.path.splitext(f"{file_path}/news.{exten}")
    if extension != f".{exten}":

        raise ValueError("The file format is not png (Created by Servant)")

else:
    raise ValueError("No file in dict (Created by Servant)")


# ایجاد یک لیست خالی برای نگهداری عکس‌ها
images = []

# حلقه بر روی تمام فایل‌هایی که با الگوی file_path/*.png مطابقت دارند
for img in glob.glob(f"{file_path}/*.{exten}"):
    # خواندن عکس با استفاده از اپن سی وی
    n = cv2.imread(img)
    # اضافه کردن عکس به لیست
    images.append(n)
    # چاپ نام فایل
    ##print(img)
#تابع تبدیل RGB و GBR به CNYK
def CMYK_to_RGBtoople(C=0,M=0,Y=0,K=0, aproach="RGB"):
    if C>1 or M>1 or Y>1 or K>1:
        raise ValueError("CMYK must be Less than 1 (Created by Servant)")
    elif aproach not in ("RGB", "BGR"):
        raise ValueError("aproach must be GBR or RGB (Created by Servant)")
    # استفاده از فرمول مشخصه
    R = 255*(1-C)*(1-K)
    G = 255*(1-M)*(1-K)
    B = 255*(1-Y)*(1-K)
    if aproach == "BGR":
        return(B,G,R)
    return (R,G,B)
# تابع برای تبدیل BGR به CMYK
def BGR_to_CMYKtoople(img, CMYK_color):
    CMYK_color_list = {"C":(255,255,0),"M":(255,0,255),"Y":(0,255,255),"K":(255,255,255)}
    if CMYK_color not in CMYK_color_list:
        raise ValueError("CMYK_color is not in CMYK_color_list (Created by Servant)")
    img_l = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    l = np.zeros(img_l.shape, dtype=np.uint8) # ایجاد یک تصویر ساده با اندازه مساوی با تصویر تک رنگ C
    l[:] = CMYK_color_list[CMYK_color] # پر کردن تصویر ساده با رنگ ورودی
    img_l = cv2.addWeighted(img_l, 0.5, l, 0.5, 0) # ترکیب تصویر تک رنگ C و تصویر ساده با ضرایب 0.5 و 0.5
    return img_l

# لیست رنگ ها
colors = ("C","M","Y","K")
# لیست برای نگه داری عکس های جدید
Pictures = []
# اعمال عملیات اصلی روی هر تصویر
for img in images:
    # بارگذاری عکس 
    image = img
    # دریافت ارتفاع و عرض عکس
    height, width = image.shape[:2]
    # تعیین مختصات شروع و پایان هر نوار
    start_row = 0
    end_row = height
    start_col = 0
    end_col = width // 4 # تقسیم عرض عکس به چهار قسمت
    # لیست برای نگه داری نوار ها
    Bars = []
    # حلقه روی چهار نوار
    for i in range(Cutting_Range):
        # برش نوار از عکس اصلی با استفاده از اندیس‌گذاری
        strip = image[start_row:end_row, start_col:end_col]
        # اعمال عملیات رنگ زنی روی نوار
        if len(strip.shape) == 3:
            strip = cv2.cvtColor(strip, cv2.COLOR_BGR2GRAY)
        else:
            raise ValueError("Invalid strip shape for cut (Created by Servant)")
        # تبدیل به فرمت CMYK
        strip = BGR_to_CMYKtoople(strip,colors[i])
        # نمایش نوار
        ##cv2.imshow(f"Strip {i+1}", strip)
        Bars.append(strip)
        # افزایش مختصات ستون برای نوار بعدی
        start_col += width // Cutting_Range
        end_col += width // Cutting_Range 

    # چسباندن نوار ها کنار یکدیگر
    picture = cv2.hconcat(Bars)

    Pictures.append(picture)
    # انتظار برای فشردن کلید
    cv2.waitKey(0)
    # بستن پنجره‌ها
    cv2.destroyAllWindows()

##print(Pictures[0].shape)
##cv2.imwrite(r"fh.png",Pictures[2])
    
# ذخیره در فایل نتایج
cont = 0
for img in Pictures:
    name = f"{cont}.{exten}"
    includ = result_path+ r"/" + name
    cv2.imwrite(includ, img)
    cont += 1
