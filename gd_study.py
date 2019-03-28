from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
# import tkinter as tk
from PIL import Image, ImageEnhance
import pytesseract

options = Options()
options.binary_location = "./chrome/chrome.exe"
# options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
options.add_argument('--mute-audio')  # 关闭声音
options.add_argument('--window-size=800,600')
# options.add_argument('--window-position=800,0')
driver = webdriver.Chrome(executable_path="./chromedriver.exe", chrome_options=options)  # 实例化chrome

# driver.maximize_window()
# driver = webdriver.Chrome()
driver.get("https://gbpx.gd.gov.cn/gdceportal/index.aspx")
elem_user = driver.find_element_by_id("txtLoginName")
elem_user.clear()
elem_user.send_keys("XXX")
elem_pwd = driver.find_element_by_id("txtPassword")
elem_pwd.clear()
elem_pwd.send_keys("XXXXXX!")
elem_code = driver.find_element_by_id("txtValid")
elem_login = driver.find_element_by_id("lnkbtnLogin")

# imgElement = driver.find_element_by_id('imgValid')
# imgElement = driver.find_element_by_class_name("user-code-img")
# print(imgElement.size, imgElement.location)
# imgSize = imgElement.size   #获取验证码图片的大小
# imgLocation = imgElement.location #获取验证码元素坐标
# rangle = (int(imgLocation['x']),int(imgLocation['y']),int(imgLocation['x'] + imgSize['width']),int(imgLocation['y']+imgSize['height']))  #计算验证码整体坐标

# location = imgElement.location # 获取验证码x,y轴坐标
# size = imgElement.size # 获取验证码的长宽
# rangle = (int(location['x']),int(location['y']),int(location['x']+size['width']),int(location['y']+size['height'])) # 写成我们需要截取的位置坐标
# print(rangle)
    
#保存屏幕内容
driver.save_screenshot("tmp.png")
yanzhengmaPic = Image.open("tmp.png")
yanzhengmaBox = (1018,480,1105,516)
yanzhengmaPic.crop(yanzhengmaBox).save("yzm.png")
# yanzhengmaPic.crop(rangle).save("yzm02.png")

# imageCode = Image.open("yzm.png")
# sharp_img = ImageEnhance.Contrast(imageCode).enhance(3.0)
# sharp_img.save("yzm01.png")
# # sharp_img = Image.open("yzm01.png")
# sharp_img = Image.open("yzm01.png")
# time.sleep(1)
# # print(sharp_img)
# grey = sharp_img.convert("L")
# print(type(sharp_img), type(grey))
# bw = grey.point(lambda x:0 if x<110 else 255,'1')#如果RGB数值小于140的变成1，否则是255。也就是将验证码背景变成白色，具体字符变成黑色。
# bw.save("aa.png")
# code = pytesseract.image_to_string(bw).strip()
# print(code)
# window = tk.Tk()
# window.title("验证码：")
# window.geometry('200X300')
# e = tk.Entry(window, show=None)
# e.pack()
# print(e.get())
# window.mainloop()
yanzhengma = input("验证码：")



elem_code.send_keys(yanzhengma)
elem_login.click()
time.sleep(5)
elem_jinruxuexi = driver.find_element_by_id("ctl00_CPHMain_btnStudy")
elem_jinruxuexi.click()
time.sleep(5)

elem_zaixuekecheng = driver.find_element_by_id("tvSecondMenut2")
elem_zaixuekecheng.click()

time.sleep(5)
#列表课程

driver.get("https://gbpx.gd.gov.cn/gdceportal/Study/LearningCourse.aspx?mid=8b2901672f0a497da5106c7a97c64543")
time.sleep(2)
# for link in driver.find_elements_by_xpath("//*[@href]"):
    # print(link.get_attribute('href'))

elem_next = driver.find_element_by_id("btnNextPage") #下一页
#找到当前页面所有未学过的课的连接
lstname = []
lstname_score = []
while 1:
    iflag = 0
    icount = 0 #当前页面计数
    for link in driver.find_elements_by_xpath("//*[@href]"):
        if link.get_attribute("id")[:6] == "gvList" and link.get_attribute("title")[:3]!="已学习" and link.get_attribute("title")!="":
            print(link.get_attribute("title"))
            icount += 1
            tmp = []
            tmp.append(link.get_attribute("title"))
            tmp.append(link.get_attribute("id"))
            tmp.append(link.get_attribute("href")[35:-3])
            if tmp in lstname:
                iflag = 1
                break
            lstname.append(tmp)
    if icount == 0:
        iflag = 1

    # 找到当前页面的分数,每1分要20分钟
    for i in range(2, icount+2):
        if iflag == 1:
            break
        a1 = driver.find_element_by_xpath(".//*[@id='gvList']/tbody/tr[" + str(i) + "]/td[2]")
        a1_baifenbi = driver.find_element_by_xpath(".//*[@id='gvList']/tbody/tr[" + str(i) + "]/td[5]")
        # print(a1.text)
        # lstname[i-2].append(a1.text)
        lstname_score.append([a1.text, a1_baifenbi.text])

    if iflag == 1:
        break
    elem_next = driver.find_element_by_id("btnNextPage") #下一页
    elem_next.click()
    
# a1 = driver.find_element_by_xpath(".//*[@id='gvList']/tbody/tr[" + str(2) + "]/td[2]")
# aa = lstname[0][2]
aaHref = "https://gbpx.gd.gov.cn/gdceportal/Study/CourseDetail.aspx?id="
# driver.get(aa) #打开学习页面

for item in zip(lstname, lstname_score):
    if float(item[1][1][:-1])>=60:
        continue
    xuexishijian = int(30*float(item[1][0])) #30分对应60%
    print(item[0][0], xuexishijian)
    aa = aaHref+item[0][2]
    driver.get(aa)
    elem_study = driver.find_element_by_id("btnStudy")
    time.sleep(2)
    elem_study.click()
    try:
        driver.switch_to_frame("scoFrame")
        # driver.switch_to.frame()
        try:
            elem_learn = driver.find_element_by_class_name("learn")
            elem_learn.click()
        except:
            pass
        
        try:
            elem_learn = driver.find_element_by_id("beginStudyButton")
            elem_learn.click()
        except:
            pass

    except:
        pass
    time.sleep(60*xuexishijian)
    driver.get("https://gbpx.gd.gov.cn/gdceportal/Study/LearningCourse.aspx?mid=8b2901672f0a497da5106c7a97c64543")
    time.sleep(10)

# winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
# import time
# time.sleep(3)

# # 进入登录页面
# # driver.get("https://gbpx.gd.gov.cn/gdceportal/index.aspx")
# elem_jinruxuexi = driver.find_element_by_id("ctl00_CPHMain_btnStudy")
# elem_jinruxuexi.click()
