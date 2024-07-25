# کتابخانه های مورد نیاز
import cv2
import numpy as np
import glob
import os

#دریافت فولدر عکس ها وتبدیل به لیستی از عکس ها
def fileEntry(file_path, exten, showfilename= False) -> list:
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
        if showfilename == True:
        # چاپ نام فایل
            print(img)
    return images

# تابع برای تبدیل BGR به CMYK
def BGR_to_CMYK(img, CMYK_color, coef = 0.5):
    CMYK_color_list = {"C":(255,255,0),"M":(255,0,255),"Y":(0,255,255),"K":(255,255,255)}
    if CMYK_color not in CMYK_color_list:
        raise ValueError("CMYK_color is not in CMYK_color_list (Created by Servant)")
    #اگر تصویر سیاه سفید بود آن را سه کاناله کن
    img_l = img
    if len(img.shape) != 3:
        img_l = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    l = np.zeros(img_l.shape, dtype=np.uint8) # ایجاد یک تصویر ساده با اندازه مساوی با تصویر تک رنگ C
    l[:] = CMYK_color_list[CMYK_color] # پر کردن تصویر ساده با رنگ ورودی
    img_l = cv2.addWeighted(img_l, coef, l, coef, 0) # ترکیب تصویر تک رنگ C و تصویر ساده با ضرایب 0.5 و 0.5
    return img_l
#اعمال رنگ زنی عکس ها
# تک مسولیتی حفظ شده
def Coloring(images, Cutting_Range, gray=False) -> list:
    colors = ("C","M","Y","K")
    Pictures = []
    # اعمال عملیات اصلی روی هر تصویر
    for image in images:
        # دریافت ارتفاع و عرض عکس
        height, width = image.shape[:2]
        # تعیین مختصات شروع و پایان هر نوار
        start_row = 0
        end_row = height
        start_col = 0
        end_col = width // Cutting_Range # تقسیم عرض عکس به چهار قسمت
        # لیست برای نگه داری نوار ها
        Bars = []
        # حلقه روی چهار نوار
        for i in range(Cutting_Range):
            # برش نوار از عکس اصلی با استفاده از اندیس‌گذاری
            strip = image[start_row:end_row, start_col:end_col]
            # اعمال عملیات رنگ زنی روی نوار
            if len(strip.shape) == 3 and gray == True:
                strip = cv2.cvtColor(strip, cv2.COLOR_BGR2GRAY)
            # تبدیل به فرمت CMYK
            strip_C = BGR_to_CMYK(strip,colors[0])
            strip_M = BGR_to_CMYK(strip,colors[1])
            strip_Y = BGR_to_CMYK(strip,colors[2])
            strip_K = BGR_to_CMYK(strip,colors[3])
            # نمایش نوار
            ##cv2.imshow(f"Strip {i+1}", strip)
            Bars.append((strip_C,strip_M,strip_Y,strip_K))
            # افزایش مختصات ستون برای نوار بعدی
            start_col += width // Cutting_Range
            end_col += width // Cutting_Range 

        # چسباندن نوار ها کنار یکدیگر
        for j in range(len(Bars)):
            blend_img_cm = cv2.addWeighted(Bars[j][0], 0.5, Bars[j][1], 0.5, 0)
            blend_img_cmy = cv2.addWeighted(blend_img_cm, 0.5, Bars[j][2], 0.5, 0)
            blend_img_cmyk = cv2.addWeighted(blend_img_cmy, 0.5, Bars[j][3], 0.5, 0)
            Bars[j] = blend_img_cmyk
        Pictures.append(cv2.hconcat(Bars))
    #خروج لیست عکس ها بافرمت جدید
    return Pictures

# ذخیره در فایل نتایج
def fileDeparture(Pictures, result_path, exten) -> bool:
    cont = 0
    for img in Pictures:
        name = f"{cont}.{exten}"
        includ = result_path+ r"/" + name
        cv2.imwrite(includ, img)
        cont += 1
    return True

def Action(file_path, result_path, inexten, outexten, Cutting_Range, gray=False):
    images = fileEntry(file_path, inexten)
    Pictures = Coloring(images, Cutting_Range, gray=gray)
    result = fileDeparture(Pictures, result_path, outexten)
    return result

# ورودی ها شامل file_path, result_path , ".Extension"(png,jpg or Both), Cutting_Range
file_path = r"C:\Users\takkaj\Desktop\job\Image_prossing\images"
result_path = r"C:\Users\takkaj\Desktop\job\Image_prossing\result"
inexten = "jpg"
outexten = "jpg"
Cutting_Range = 4

b = Action(file_path, result_path, inexten, outexten, Cutting_Range, gray=False)
