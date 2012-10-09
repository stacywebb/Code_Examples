

from lxml import etree

from util.UnicodeConverter import latin1_to_ascii

def emitCDATA(node, name, value):
    newnode = etree.Element(name)
    node.append(newnode)
    newnode.text = etree.CDATA(latin1_to_ascii(value))
    return newnode

def emitElement(node, name, value):
    newnode = etree.Element(name)
    node.append(newnode)
    newnode.text = latin1_to_ascii(value)
    return newnode

def emitXmlContent(operation, isSuccess, content, errorMessage):
    return emitXmlMultiple(operation, isSuccess, {'Content': content}, errorMessage)

def emitXmlMultiple(operation, isSuccess, responseDict, errorMessage):
    root = etree.Element('ServiceHub')
    emitElement(root, "Operation", operation)
    emitElement(root, "Success", str(isSuccess))
    if isSuccess and responseDict != None:
        keys = responseDict.keys()
        keys.sort()
        for key in keys:
            value = responseDict[key]
            if value != None:
                emitCDATA(root, key, value)
    if not isSuccess and errorMessage != None:
        emitElement(root, "Error", errorMessage)
    xmlString = etree.tostring(root, pretty_print=True)
    return xmlString