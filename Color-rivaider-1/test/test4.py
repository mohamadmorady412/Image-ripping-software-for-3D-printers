import cv2
import numpy as np

# تابع برای تبدیل BGR به CMYK
def BGR_to_CMYKtoople(img, CMYK_color):
    CMYK_color_list = {"C":(255,255,0),"M":(255,0,255),"Y":(0,255,255),"K":(255,255,255)}
    if CMYK_color not in CMYK_color_list:
        raise ValueError("CMYK_color is not in CMYK_color_list (Created by Servant)")
    img_l = img #cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    l = np.zeros(img_l.shape, dtype=np.uint8) # ایجاد یک تصویر ساده با اندازه مساوی با تصویر تک رنگ C
    l[:] = CMYK_color_list[CMYK_color] # پر کردن تصویر ساده با رنگ ورودی
    img_l = cv2.addWeighted(img_l, 0.5, l, 0.5, 0) # ترکیب تصویر تک رنگ C و تصویر ساده با ضرایب 0.5 و 0.5
    return img_l


img = cv2.imread(r"C:\Users\takkaj\Desktop\Image_prossing\OIP.jpg", cv2.IMREAD_GRAYSCALE)
result = BGR_to_CMYKtoople(img, "M")
cv2.imwrite("hello.jpg", result)
cv2.waitKey(0) # انتظار برای فشردن یک کلید
cv2.destroyAllWindows() # بستن پنجره‌ها