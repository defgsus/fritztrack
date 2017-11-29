# coding=utf-8
from __future__ import unicode_literals, print_function

from time import sleep
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from fritzlog.tools.fritzbox_credentials import LOGIN_PASSWORD


class FritzBrowser(object):

    def __init__(self):
        self.driver = webdriver.PhantomJS()
        #self.driver = webdriver.Chrome()
        #self.driver = webdriver.Firefox()
        self.get("http://fritz.box")
        self.links = []
        self._sid = None

    def __del__(self):
        self.driver.close()

    def sleep(self, min_sec, max_sec=0):
        sleep(random.uniform(min_sec, max(min_sec, max_sec)))

    def get(self, url):
        self.driver.get(url)

    def elem_login_password_field(self):
        return self.driver.find_element_by_css_selector('input[type="password"]')

    def elem_login_button(self):
        return self.driver.find_element_by_css_selector('button[type="submit"]')

    def get_links(self):
        elems = self.driver.find_elements_by_css_selector("a.menu_item")
        self.links = [e.get_attribute("href") for e in elems]
        return self.links

    def get_session_id(self):
        if self._sid is None:
            self._sid = self.driver.execute_script("return main.sid")
        return self._sid

    def open_link(self, name):
        qname = "lp=%s" % name
        for l in self.links:
            if qname in l:
                self.get(l)
                self.sleep(3)
                return True
        return False

    def login(self):
        elem = self.elem_login_password_field()
        elem.send_keys(LOGIN_PASSWORD)
        elem.send_keys(Keys.RETURN)
        self.sleep(1)
        self.get_links()

    def open_log(self):
        return self.open_link("log")

    def open_capture(self):
        self.get("http://fritz.box/html/capture.html")
        self.login()

    def get_capture_url(self, iface="3-0"):
        sid = self.get_session_id()
        return "http://fritz.box/cgi-bin/capture_notimeout?sid=%s&capture=Start&snaplen=1600&ifaceorminor=%s" % (
            sid, iface,
        )

    def get_capture_stop_url(self):
        sid = self.get_session_id()
        return "http://fritz.box/cgi-bin/capture_notimeout?iface=all&minor=0&type=3&capture=Stop&sid=%s&xhr=1" % sid

    def get_log_strings(self):
        elems = self.driver.find_elements_by_css_selector("a.print")
        return [e.text for e in elems]


if __name__ == "__main__":

    b = FritzBrowser()
    b.login()
    b.open_log()
    print(b.get_log_strings())

    #req = requests.get("http://fritz.box")
    #print(req.content)