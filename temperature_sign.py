from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import random
import time
import selenium
from selenium.webdriver.chrome.options import Options


# 作者：mxyr、mightnent

def read(a):  # 读取配置文件，以列表形式返回
    out = []
    f = open(a, "r", encoding='utf-8')
    for j in f:
        l = j.split()
        out.append(l)
    f.close()
    return out


def zhtime(a):  # 返回当前时间（中文格式）
    output = time.strftime(a.encode('unicode_escape').decode("utf-8"), time.localtime(time.time())).encode(
        "utf-8").decode('unicode_escape')
    return output


def zhtime_t(a, t):  # 返回给定t的时间（中文格式）
    output = time.strftime(a.encode('unicode_escape').decode("utf-8"), time.localtime(t)).encode(
        "utf-8").decode('unicode_escape')
    return output


qvari = 0  # 上一次随机时间偏移，第一次手工启动初始化为0
n = 0  # 体温登记次数计数器，初始化为0
while True:  # 无限循环
    data = read("./data.txt")  # 读取用户名、密码的数据文件
    data2 = read("./data2.txt")  # 读取身份证号、手机号的数据文件
    log = open("./qiandao_log.txt", "a")  # 创建/寻找日志文件（默认为同目录下的qiandao_log.txt）
    n += 1  # 体温登记次数计数器+1
    print(zhtime("%Y年%m月%d日 %H时%M分%S秒") + "\t" + "第" + str(n) + "次登记:")
    log.writelines(
        zhtime("%Y年%m月%d日 %H时%M分%S秒") + "\t第" + str(n) + "次登记:\n")
    # 打印本次操作时间并写入日志
    ini = time.time()  # 记录开始时间
    # 配置浏览器
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    # 循环读取用户列表
    for i in data:
        try:
            browser = webdriver.Chrome('/root/chromedriver', chrome_options=options)
            browser.get('https://tts.sutd.edu.sg/tt_login.aspx?formmode=expire')
            username = browser.find_element_by_id('pgContent1_uiLoginid')
            username.send_keys(i[0])  # 填写学号
            time.sleep(random.randint(2, 6))  # 随机事件，模仿人类操作
            password = browser.find_element_by_id('pgContent1_uiPassword')
            password.send_keys(i[1])  # 填写密码
            time.sleep(random.randint(2, 6))
            submit = browser.find_element_by_id('pgContent1_btnLogin')
            submit.click()  # 登录
            time.sleep(random.randint(2, 6))
            browser.find_element_by_link_text('Temperature Taking').click()  # 进入体温申报
            browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
            browser.get("https://tts.sutd.edu.sg/tt_temperature_taking_user.aspx")
            select = Select(browser.find_element_by_id('pgContent1_uiTemperature'))
            time.sleep(random.randint(2, 6))
            select.select_by_value('Less than or equal to 37.6°C')  # 申报正常体温
            time.sleep(random.randint(2, 6))
            browser.find_element_by_id('pgContent1_btnSave').click()  # 提交
            browser.quit()  # 退出浏览器
            # 向终端汇报并且写入日志
            print(zhtime("%Y年%m月%d日 %H时%M分%S秒"))
            log.writelines(zhtime("%Y年%m月%d日 %H时%M分%S秒") + "\t")
            print(i[2])
            log.writelines(i[2] + "\t")
            print("体温登记成功！")
            log.writelines("体温登记成功！" + "\n")
        except selenium.common.exceptions.NoSuchElementException as err:
            # 如果发生错误（密码修改导致的登录失败或者网页改版）
            browser.quit()
            # 向终端汇报并且写入日志
            print(zhtime("%Y年%m月%d日 %H时%M分%S秒"))
            log.writelines(zhtime("%Y年%m月%d日 %H时%M分%S秒") + "\t")
            print(i[2])
            log.writelines(i[2] + "\t")
            print("--------体温登记失败（登录失败）！--------")
            log.writelines("--------体温登记失败（登录失败）！--------" + "\n")
    if n % 2 != 0:  # 体温每日需要申报两次，但是个人状态只需申报一次
        for i in data:
            try:  # 按流程填写各项
                browser = webdriver.Chrome('/root/chromedriver', chrome_options=options)
                browser.get('https://tts.sutd.edu.sg/tt_login.aspx?formmode=expire')
                username = browser.find_element_by_id('pgContent1_uiLoginid')
                username.send_keys(i[0])
                time.sleep(random.randint(2, 6))
                password = browser.find_element_by_id('pgContent1_uiPassword')
                password.send_keys(i[1])
                time.sleep(random.randint(2, 6))
                submit = browser.find_element_by_id('pgContent1_btnLogin')
                submit.click()
                time.sleep(random.randint(2, 6))
                browser.find_element_by_link_text('Daily Declaration').click()
                browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
                browser.get("https://tts.sutd.edu.sg/tt_daily_dec_user.aspx")
                time.sleep(random.randint(2, 6))
                browser.find_element_by_id('pgContent1_rbVisitOtherCountryNo').click()
                time.sleep(random.randint(2, 6))
                browser.find_element_by_id('pgContent1_rbNoticeNo').click()
                time.sleep(random.randint(2, 6))
                browser.find_element_by_id('pgContent1_rbContactNo').click()
                time.sleep(random.randint(2, 6))
                browser.find_element_by_id('pgContent1_rbMCNo').click()
                time.sleep(random.randint(2, 6))
                browser.find_element_by_id('pgContent1_btnSave').click()
                time.sleep(random.randint(2, 6))
                browser.quit()
                # 向终端汇报并且写入日志
                print(zhtime("%Y年%m月%d日 %H时%M分%S秒"))
                log.writelines(zhtime("%Y年%m月%d日 %H时%M分%S秒") + "\t")
                print(i[2])
                log.writelines(i[2] + "\t")
                print("每日报告登记成功！")
                log.writelines("每日报告登记成功！" + "\n")
            except selenium.common.exceptions.NoSuchElementException as err:
                # 如果发生错误（密码修改导致的登录失败或者网页改版）
                browser.quit()
                # 向终端汇报并且写入日志
                print(zhtime("%Y年%m月%d日 %H时%M分%S秒"))
                log.writelines(zhtime("%Y年%m月%d日 %H时%M分%S秒") + "\t")
                print(i[2])
                log.writelines(i[2] + "\t")
                print("--------每日报告登记失败（登录失败）！--------")
                log.writelines("--------每日报告登记失败（登录失败）！--------" + "\n")
        for i in data2:  # 循环读取数据2
            browser = webdriver.Chrome('/root/chromedriver', chrome_options=options)
            browser.get('https://temperaturepass.ndi-api.gov.sg/login/PROD-200913519C-7004-SUTD-SE')
            time.sleep(10)  # 这个网页加载得比较慢，因此多等一会
            browser.find_element_by_xpath(
                "/html/body/app-root/app-qrscan/div/div/div/div/div[2]/div[1]/div/img").click()  # 寻找“check in”
            time.sleep(10)  # 这个网页加载得比较慢，因此多等一会
            NRIC = browser.find_element_by_id('mat-input-1')
            NRIC.send_keys(i[0])  # 填写身份证
            time.sleep(random.randint(2, 6))
            phone = browser.find_element_by_id('mat-input-0')
            phone.send_keys(i[1])  # 填写手机
            time.sleep(random.randint(2, 6))
            infoname = "./screenshotlog/" + zhtime("%Y年%m月%d日_%H时%M分%S秒") + "_" + str(
                i[2]) + "_info" + ".png"
            browser.save_screenshot(infoname)
            browser.find_element_by_xpath(
                "/html/body/app-root/app-declaration/div/div/div[3]/div/div/button/span/img").click()
            time.sleep(10)
            name = "./screenshotlog/" + zhtime("%Y年%m月%d日_%H时%M分%S秒") + "_" + str(
                i[2]) + ".png"
            browser.save_screenshot(name)  # 截图作为日后证明
            browser.quit()
            # 向终端汇报并且写入日志
            print(zhtime("%Y年%m月%d日 %H时%M分%S秒"))
            log.writelines(zhtime("%Y年%m月%d日 %H时%M分%S秒") + "\t")
            print(i[2])
            log.writelines(i[2] + "\t")
            print("每日进入学校登记成功！")
            log.writelines("每日进入学校登记成功！" + "\n")
    # 申报流程结束，开始进行总结并写入日志
    print(zhtime("%Y年%m月%d日 %H时%M分%S秒"))
    log.writelines(zhtime("%Y年%m月%d日 %H时%M分%S秒") + "\t")
    d = int(time.strftime("%H", time.localtime(time.time())))  # 获得当前“时”
    final = time.time()
    cost = final - ini
    print("全部登记成功！")
    print("共计用时:" + str(cost) + "秒")
    log.writelines("全部登记成功！" + "\n")
    log.writelines("共计用时:" + str(cost) + "秒" + "\n")
    vari = random.randint(-3600, 3600)  # 随机±一小时，为下一次申报准备（模拟人类行为）
    if d < 12:  # 如果为上午，下一次申报大概在七小时后
        # 向终端汇报程序规划并写入日志
        print("预计下次登记")
        print(zhtime_t("%Y年%m月%d日 %H时%M分%S秒", (time.time() + 25200 + vari - qvari)))
        log.writelines("预计下次登记:" + "\t" + zhtime_t("%Y年%m月%d日 %H时%M分%S秒", (time.time() + 25200 + vari - qvari)) + "\n")
        log.close()
        # 等待大概七小时
        time.sleep(25200 + vari - qvari - cost)
    else:  # 如果为下午，下一次申报大概在十七小时后
        # 向终端汇报程序规划并写入日志
        print("预计下次登记")
        print(zhtime_t("%Y年%m月%d日 %H时%M分%S秒", (time.time() + 61200 + vari - qvari)))
        log.writelines("预计下次登记:" + "\t" + zhtime_t("%Y年%m月%d日 %H时%M分%S秒", (time.time() + 61200 + vari - qvari)) + "\n")
        log.close()
        # 等待大概十七小时
        time.sleep(61200 + vari - qvari - cost)
    # 将本次随机时间写入qvari，作为下一次申报的“前一次随机时间”参数
    qvari = vari
