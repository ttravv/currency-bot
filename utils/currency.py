import httpx
import time
from xml.etree import ElementTree as ET


def time_for_now():
    return time.strftime("%d/%m/%Y")


r = httpx.get(f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={time_for_now()}")
tree = ET.fromstring(r.content.decode("windows-1251"))


def xml_to_dict(element) -> dict:
    result = {element.tag: {} if element.attrib else None}
    children = list(element)

    if children:
        dd = {}
        for dc in map(xml_to_dict, children):
            for k, v in dc.items():
                if k in dd:
                    if not isinstance(dd[k], list):
                        dd[k] = [dd[k]]
                    dd[k].append(v)
                else:
                    dd[k] = v
        result = {element.tag: dd}
    if element.attrib:
        result[element.tag].update(("@" + k, v) for k, v in element.attrib.items())
    if element.text:
        text = element.text.strip()
        if children or element.attrib:
            if text:
                result[element.tag]["#text"] = text
        else:
            result[element.tag] = text
    return result


cb_response = xml_to_dict(tree)["ValCurs"]["Valute"]

valutes = [dct["CharCode"] for dct in cb_response if "CharCode" in dct]

print(cb_response)
