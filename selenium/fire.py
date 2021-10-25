import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestRrr(object):
    def setup_method(self, method):
        self.driver = webdriver.Firefox()
        self.vars = {}
        self.login()
        self.count = 0
        self.num = 0
        self.url = ''

    def teardown_method(self, method):
        self.driver.quit()

    def login(self):
        # self.driver.get("https://passport.jd.com/uc/login?ltype=logout&ReturnUrl=https://item.jd.com/100026667878.html")
        self.driver.get(
            "https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F%3Fcu%3Dtrue%26utm_source%3Dbaidu-pinzhuan%26utm_medium%3Dcpc%26utm_campaign%3Dt_288551095_baidupinzhuan%26utm_term%3D0f3d30c8dba7459bb52f2eb5eba8ac7d_0_f3d7ccb91bd44600beef5ac83d7d8b82")
        # self.driver.find_element(By.ID, "tryBtn").click()
        time.sleep(10)
        self.test_rrr()

    def test_rrr(self):
        # self.driver.get("https://marathon.jd.com/seckill/seckill.action?skuId=100014366717&num=1&rid=1633426563")
        self.driver.get("https://item.jd.com/100014366717.html")

        self.driver.find_element(By.CSS_SELECTOR, ".item:nth-child(2) > a > i").click()
        # 14 | click | linkText=256GB |
        self.driver.find_element(By.LINK_TEXT, "256GB").click()
        # 15 | click | linkText=【1年期官方AppleCare+版】 |
        self.driver.find_element(By.LINK_TEXT, "【1年期官方AppleCare+版】").click()
        self.driver.set_window_size(1520, 580)
        self.driver.execute_script("window.scrollTo(0,638.4000244140625)")

    def click(self):
        self.url = self.driver.current_url

        if str(self.url).startswith("https://item.jd.com/100014366717"):
            self.driver.find_element(By.ID, "btn-reservation").click()
            self.count += 1
            print(f'点击了{self.count}次')
            self.url = self.driver.current_url
            if str(self.url).startswith("https://yushou.jd.com"):
                self.driver.get("https://item.jd.com/100014366717.html")
            # self.driver.get("https://pro.jd.com/mall/active/3hTNPS52FkTKYHsrCnFYzB5JxGPa/index.html")
        else:
            self.driver.find_element(By.CSS_SELECTOR, ".checkout-submit > b").click()
            # 15 | assertAlert | 很遗憾没有抢到，再接再厉哦。 |
            assert self.driver.switch_to.alert.text == "很遗憾没有抢到，再接再厉哦。"
            self.num += 1
            print(f'抢购了{self.num}次')


if __name__ == '__main__':
    p = TestRrr()
    p.setup_method(None)

    while 1:
        sec = random.uniform(0.01, 0.5)
        try:
            p.click()
            # time.sleep(0)
        except Exception as e:
            print(e)
