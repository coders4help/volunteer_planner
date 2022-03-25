from behave import given, then


@given("I go to the homepage")
def impl(context):
    context.browser.get("http://localhost:8000/")


@then('"{title}" is in the page body')
def impl(context, title):
    if title not in context.browser.find_element_by_css_selector("body").text:
        raise Exception("Couldn't find text '%s' in the page." % title)
