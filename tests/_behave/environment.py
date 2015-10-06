from selenium import webdriver

# This file is picked up by behave, and is where we tie behave and Selenium
# together.


def before_all(context):
    """
    Steps to be executed before behave features are run.
    Serves to fire up PhantomJS.
    """
    context.browser = webdriver.PhantomJS()


def after_all(context):
    """
    Steps to execute after all features have run.
    Serves to stop PhantomJS again.
    """
    context.browser.quit()
