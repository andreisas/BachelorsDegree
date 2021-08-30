from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom

xmlout = "Data/XMLFile.xml"

comparatorDict = {" lt ": "<", " gt ": ">", " le ": "<=", " ge ": ">=", " eq ":"==", " not ": "!=", " and ": "&&", " or ": "||"}
comparatorRevDict = {"<": " lt ", ">": " gt ", "<=": " le ", ">=": " ge ", "==": " eq ", "!=": " not ", "&&": " and ", "||": " or "}


def prettify(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def CCondToXMLCond(condtext):
	'''
	Translates a condition from C to XML form
	'''
	for comp in comparatorRevDict:
		if comp in condtext:
			condtext = condtext.replace(comp, comparatorRevDict[comp])
	return condtext

def updateXML(mySTM):
    '''
    Write the current STM into a file as an XML
    '''
    f = open(xmlout, "wt")

    stm = Element("stm")

    states = SubElement(stm, 'states')
    stateselements = [
        Element('state', name=mySTM.statesDict[st].name)
        for st in mySTM.statesDict

    ]
    states.extend(stateselements)

    transitions = SubElement(stm, 'transitions')
    transitionselements = [
        Element('transition', name=mySTM.transitionsDict[tr].name, cond=CCondToXMLCond(mySTM.transitionsDict[tr].cond),
                src=mySTM.transitionsDict[tr].src.name, dest=mySTM.transitionsDict[tr].dest.name)
        for tr in mySTM.transitionsDict
    ]
    transitions.extend(transitionselements)

    f.write(prettify(stm))

    print("Updated XML file")