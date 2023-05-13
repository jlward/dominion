from bs4 import BeautifulSoup


def css_select(response, selector):
    soup = BeautifulSoup(response.content)

    return soup.select(selector)


def _css_select_get_text(response, selector):
    for element in css_select(response, selector):
        yield element.text.strip()


def css_select_get_text(response, selector):
    return list(_css_select_get_text(response, selector))


def _css_select_get_attributes(response, selector, attributes):
    for element in css_select(response, selector):
        yield {attribute: element[attribute] for attribute in attributes}


def css_select_get_attributes(response, selector, attributes):
    return list(_css_select_get_attributes(response, selector, attributes))
