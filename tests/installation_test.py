import os
import subprocess

from nose.tools import istest, assert_equals
from selenium import webdriver
from starboard import find_local_free_tcp_port as find_port

from tempdir import create_temporary_dir


@istest
def selenium_is_working():
    browser = webdriver.Firefox()
    browser.close()

    
# TODO: assert that apache has stopped
@istest
def running_apache2_after_installation_shows_default_page():
    with create_temporary_dir() as temp_dir:
        port = find_port()
        install_apache2(temp_dir, port=port)
        process = subprocess.Popen(
            ["bin/httpd", "-DNO_DETACH"],
            cwd=temp_dir
        )
        try:
            assert_default_apache_page_is_visible(port=port)
        finally:
            process.terminate()


@istest
def apachectl_has_httpd_location_updated():
    with create_temporary_dir() as temp_dir:
        port = find_port()
        install_apache2(temp_dir, port=port)
        subprocess.check_call(
            ["bin/apachectl", "start"],
            cwd=temp_dir
        )
        try:
            assert_default_apache_page_is_visible(port=port)
        finally:
            subprocess.check_call(
                ["bin/apachectl", "stop"],
                cwd=temp_dir
            )


def install_apache2(directory, port):
    path = os.path.join(os.path.dirname(__file__), "..")
    subprocess.check_call(["whack", "install", path, directory, "-pport={0}".format(port), "--no-cache"])

def assert_default_apache_page_is_visible(port):
    url = "http://localhost:{0}/".format(port)
    browser = webdriver.Firefox()
    try:
        browser.get(url)
        element = browser.find_element_by_css_selector("h1")
        assert_equals("It works!", element.text)
    finally:
        browser.close()
