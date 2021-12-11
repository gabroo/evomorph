from lxml import etree


def converter(request):
    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.parse("three_layer.xml", parser).getroot()

    val = (
        str(request.xValue)
        + ","
        + str(request.yValue)
        + ","
        + str(request.zValue)
    )
    item = root.find(".//Size")
    item.attrib["value"] = val

    item = root.find(".//StopTime")
    item.attrib["value"] = str(request.stopTime)

    for i in root.iterfind(".//CellType"):
        if i.attrib["name"] == "A":
            for j in i.iterfind(".//Constant"):
                if j.attrib["symbol"] == "gamma":
                    j.attrib["value"] = "0." + str(request.gammaA).split(".")[0]
        if i.attrib["name"] == "B":
            for j in i.iterfind(".//Constant"):
                if j.attrib["symbol"] == "gamma":
                    j.attrib["value"] = "0." + str(request.gammaB).split(".")[0]

    for i in root.iterfind(".//Population"):
        if i.attrib["type"] == "A":
            j = i.find(".//InitCircle")
            j.attrib["number-of-cells"] = str(request.numACells)
        if i.attrib["type"] == "B":
            j = i.find(".//InitCircle")
            j.attrib["number-of-cells"] = str(request.numBCells)

    return etree.tostring(root, pretty_print=True).decode()
