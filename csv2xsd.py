import pandas as pd
import numpy as np

VERSION = '<?xml version="1.0" encoding="UTF-8"?>'
SCHEMA = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:eCH-0265="http://www.ech.ch/xlmns/eCH-0265/1" xmlns:eCH-0108="http://www.ech.ch/xmlns/eCH-0108/7" xmlns:eCH-0261="http://www.ech.ch/xmlns/eCH-0261/1" xmlns:interlis-geometry="http://www.interlis.ch/geometry/1.0" xmlns:eCH-0007="http://www.ech.ch/xmlns/eCH-0007/6" targetNamespace="http://www.ech.ch/xmlns/eCH-02XX/2" elementFormDefault="qualified" attributeFormDefault="unqualified" version="1.0">	<!-- < targetNamespace muss angepasst werden, wenn von 02XX abgewichen wird. Für den Moment behandle ich das Dokument als v2 von 02XX> --><xs:annotation>		<xs:documentation xml:lang="de">Agrardaten - Nutztiere</xs:documentation></xs:annotation><xs:import namespace="http://www.ech.ch/xmlns/eCH-0007/6" schemaLocation="http://www.ech.ch/xmlns/eCH-0007/6/eCH-0007-6-0.xsd"/>	<xs:import namespace="http://www.ech.ch/xmlns/eCH-0108/7" schemaLocation="http://www.ech.ch/xmlns/eCH-0108/7/eCH-0108-7-0.xsd"/>	<xs:import namespace="http://www.ech.ch/xmlns/eCH-0261/1" schemaLocation="https://www.ech.ch/sites/default/files/imce/eCH-Dossier/0241-0270/eCH-0261/1.0.0/Beilagen/eCH-0261-1-0.xsd"/>	<xs:import namespace="http://www.interlis.ch/geometry/1.0" schemaLocation="https://models.interlis.ch/refhb24/geometry.xsd"/>'

# read downloaded csv. As csv is located behind a restriction, it must be downloaded from here: https://shareech.sharepoint.com/:x:/r/sites/FGAgriFood/_layouts/15/Doc.aspx?sourcedoc=%7BFCED26D9-51D4-482E-943E-FE032039C5F1%7D&file=IST_Zustand_Abgleich.xlsx&action=default&mobileredirect=true


def main():
    df = pd.read_csv("v2_IST_Zustand_Abgleich_aufgeräumt_pahu.csv", sep=";",
                     encoding="CP1252", header=0, skiprows=0)
    """
    df = pd.read_csv("IST_Zustand_Abgleich_aufgeräumt_pahu.csv", sep=";",
                     encoding="CP1252", header=0, skiprows=0)
    """

    # remove empty spaces as they are now allowed in xs:element name and type
    df['Element'] = df['Element'].str.replace(' ', '')
    df['Datentyp'] = df['Datentyp'].str.replace(' ', '')

    # print(df.columns)

    """
    # add correct types
    df['Datentyp'] = df['Datentyp'].str.replace('int', 'xs:int')
    df['Datentyp'] = df['Datentyp'].str.replace('Int', 'xs:int')
    df['Datentyp'] = df['Datentyp'].str.replace(
        'boolean', 'xs:boolean')
    df['Datentyp'] = df['Datentyp'].str.replace(
        'Boolean', 'xs:boolean')
    df['Datentyp'] = df['Datentyp'].str.replace('string', 'xs:string')
    df['Datentyp'] = df['Datentyp'].str.replace('String', 'xs:string')
    df['Datentyp'] = df['Datentyp'].str.replace(
        'timedate', 'xs:dateTime')
    df['Datentyp'] = df['Datentyp'].str.replace(
            'TimeDate', 'xs:dateTime')
    df['Datentyp'] = df['Datentyp'].str.replace(
        'datetime', 'xs:dateTime')
    df['Datentyp'] = df['Datentyp'].str.replace(
        'EnumerationValue', 'eCH-0261:enumeratedItemType')
    df['Datentyp'] = df['Datentyp'].str.replace(
        'TranslatedEnumTyp eOfEnumEquidNotif icationState', 'eCH-0261:enumeratedItemType')
    df['Datentyp'] = df['Datentyp'].str.replace(
        'EnumEquidColor', 'eCH-0261:enumeratedItemType')
    df['Datentyp'] = df['Datentyp'].str.replace(
        'TranslatedEnumTyp eOfEnumEquidSpe cies', 'eCH-0261:enumeratedItemType')
    df['Datentyp'] = df['Datentyp'].str.replace(
        'decimal', 'xs:decimal')
    """

    level_n = []
    themas = df.iloc[:, 0]

    for i in themas:
        level_n.append(i)

    # get name for complex elements. use reversed list for performance
    unique_levels = list(reversed(list(np.unique(level_n))))

    # write to file.
    # with open("eCH-02XX.xsd", "a", encoding="utf-8") as f:

    with open("v2_eCH-02XX.xsd", "a", encoding="utf-8") as f:
        f.write(VERSION)
        f.write(SCHEMA)

        for u in reversed(list(unique_levels)):

            intro = f'<xs:complexType name= "{u}"><xs:annotation><xs:documentation xml:lang="de">BLA</xs:documentation><xs:documentation xml:lang="en">BLA</xs:documentation></xs:annotation><xs:all>'
            f.write(intro)

            for col, val in df[::-1].iterrows():

                if u == val["Thema"]:
                    text = f'<xs:element name="{val["element"]}" type="{val["proposedDatatype"]}"><xs:annotation><xs:documentation xml:lang="de">{val["Beschreibung"]}</xs:documentation></xs:annotation></xs:element>\n'
                    f.write(text)

                else:
                    continue

            level_n.pop()
            outro = '</xs:all></xs:complexType>'
            f.write(outro)

        # add types for complex

        """
        short = f'<xs:simpleType name="short"><xs:restriction base="xs:integer"><xs:minInclusive value="1"/><xs:maxInclusive value="999"/></xs:restriction></xs:simpleType>'
        f.write(short)
        """
        fin = '</xs:schema>'
        f.write(fin)


if __name__ == "__main__":
    main()
