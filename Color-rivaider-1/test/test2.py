import cv2
import numpy as np

# تابع برای تبدیل BGR به CMYK
def BGR_to_CMYKtoople(img, CMYK_color):
    CMYK_color_list = {"C":(255,255,0),"M":(255,0,255),"Y":(0,255,255),"K":(255,255,255)}
    if CMYK_color not in CMYK_color_list:
        raise ValueError("CMYK_color is not in CMYK_color_list (Created by Servant)")
    #img_l = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img_l = img
    l = np.zeros(img_l.shape, dtype=np.uint8) # ایجاد یک تصویر ساده با اندازه مساوی با تصویر تک رنگ C
    l[:] = CMYK_color_list[CMYK_color] # پر کردن تصویر ساده با رنگ ورودی
    img_l = cv2.addWeighted(img_l, 0.5, l, 0.5, 0) # ترکیب تصویر تک رنگ C و تصویر ساده با ضرایب 0.5 و 0.5
    return img_l



# بارگذاری دو تصویر تک رنگ
image = cv2.imread(r'C:\Users\takkaj\Desktop\Image_prossing\OIL.jpg')
# لیست رنگ ها
colors = ("C","M","Y","K")
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
for i in range(4):
    # برش نوار از عکس اصلی با استفاده از اندیس‌گذاری
    strip = image[start_row:end_row, start_col:end_col]
    # تبدیل به فرمت CMYK
    strip_C = BGR_to_CMYKtoople(strip,colors[0])
    strip_M = BGR_to_CMYKtoople(strip,colors[1])
    strip_Y = BGR_to_CMYKtoople(strip,colors[2])
    strip_K = BGR_to_CMYKtoople(strip,colors[3])
    # نمایش نوار
    ##cv2.imshow(f"Strip {i+1}", strip)
    Bars.append((strip_C,strip_M,strip_Y,strip_K))
    # افزایش مختصات ستون برای نوار بعدی
    start_col += width // 4
    end_col += width // 4 

im1c = Bars[0][0]
im1m = Bars[0][1]
im1y = Bars[0][2]
im1k = Bars[0][3]

im2c = Bars[1][0]
im2m = Bars[1][1]
im2y = Bars[1][2]
im2k = Bars[1][3]

im3c = Bars[2][0]
im3m = Bars[2][1]
im3y = Bars[2][2]
im3k = Bars[2][3]

im4c = Bars[3][0]
im4m = Bars[3][1]
im4y = Bars[3][2]
im4k = Bars[3][3]


#cv2.imshow("OutC",im1c)
#cv2.imshow("OutY",im1y)
#cv2.imshow("OutM",im1m)
#cv2.imshow("OutK",im1k)

blend_img1_cm = cv2.addWeighted(im1c, 0.5, im1m, 0.5, 0)
blend_img1_cmy = cv2.addWeighted(blend_img1_cm, 0.5, im1y, 0.5, 0)
blend_img1_cmyk = cv2.addWeighted(blend_img1_cmy, 0.5, im1k, 0.5, 0)

blend_img2_cm = cv2.addWeighted(im2c, 0.5, im2m, 0.5, 0)
blend_img2_cmy = cv2.addWeighted(blend_img2_cm, 0.5, im2y, 0.5, 0)
blend_img2_cmyk = cv2.addWeighted(blend_img2_cmy, 0.5, im2k, 0.5, 0)

blend_img3_cm = cv2.addWeighted(im3c, 0.5, im3m, 0.5, 0)
blend_img3_cmy = cv2.addWeighted(blend_img3_cm, 0.5, im3y, 0.5, 0)
blend_img3_cmyk = cv2.addWeighted(blend_img3_cmy, 0.5, im3k, 0.5, 0)

blend_img4_cm = cv2.addWeighted(im4c, 0.5, im4m, 0.5, 0)
blend_img4_cmy = cv2.addWeighted(blend_img4_cm, 0.5, im4y, 0.5, 0)
blend_img4_cmyk = cv2.addWeighted(blend_img4_cmy, 0.5, im4k, 0.5, 0)

liss = [blend_img1_cmyk,blend_img2_cmyk,blend_img3_cmyk,blend_img4_cmyk]
picture = cv2.hconcat(liss)

cv2.imshow("CMYK", picture)
cv2.imshow("RGB", image)

cv2.waitKey(0)
cv2.destroyAllWindows()