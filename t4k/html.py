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

def table(attributes={}):
    return element('table', attributes)

def tr(attributes={}):
    return element('tr', attributes)

def td(attributes={}):
    return element('td', attributes)


def build_table(fields):
    table = t4k.html.table({'class': 'performance'})
    first_row = True
    for row in fields:
        if first_row:
            tr = table.appendChild(t4k.html.tr({'class': 'first-row'}))
            first_row = False
        else:
            tr = table.appendChild(t4k.html.tr())
                
        first_cell = True
        for cell in row:
            if first_cell:
                td = tr.appendChild(t4k.html.td({'class': 'first-cell'}))
                first_cell = False
            else:
                td = tr.appendChild(t4k.html.td())
            td.appendChild(text(cell))

    return table
