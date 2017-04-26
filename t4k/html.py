from xml.dom import minidom

# This provisional dom is used as an element factory
DOM = minidom.Document()

def element(tag_name, attributes={}):
    elm = DOM.createElement(tag_name)
    bind_attributes(elm, attributes)
    return elm 

def bind_attributes(element, attributes):
    for attribute in attributes:
        element.setAttribute(attribute, attributes[attribute])
    return element

def div(attributes={}):
    return element('div', attributes)

def span(attributes={}):
    return element('span', attributes)

def text(text_content):
    return DOM.createTextNode(text_content)

