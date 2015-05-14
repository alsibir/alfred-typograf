# encoding: utf-8

u"""Простой интерфейс к веб-сервису Типографа Студии Артемия Лебедева

Работает в связке с Alfred, но может использоваться отдельно"""

from __future__ import print_function

import sys

import cgi
import httplib, urllib
import unicodedata
import xml.etree.ElementTree as ET

def process(text):
    headers = {"Content-type": "application/xml"}

    template = u"""<?xml version="1.0" encoding="UTF-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\n'
    <soap:Body>'
        <ProcessText xmlns="http://typograf.artlebedev.ru/webservices/">
            <text>{text}</text>
            <entityType>3</entityType>
            <useBr>1</useBr>
            <useP>0</useP>
            <maxNobr>3</maxNobr>
        </ProcessText>
        </soap:Body>
    </soap:Envelope>"""

    conn = httplib.HTTPConnection("typograf.artlebedev.ru")
    conn.request("POST", "/webservices/typograf.asmx",
                 template.format(text=cgi.escape(text)).encode('utf-8'),
                 headers)
    response = conn.getresponse()
    if response.status == 200:
        xml = response.read()
        root = ET.fromstring(xml)
        conn.close()
        result = root.findtext(".//{http://typograf.artlebedev.ru/webservices/}ProcessTextResult")
        result = result.replace("<br />\n", "\n")
        return result
    else:
        conn.close()
        return text

if __name__ == '__main__':
    text = sys.stdin.read().decode('utf-8')
    # http://www.alfredforum.com/topic/1724-script-filter-arguments-are-decomposed/
    # Альфред передаёт данные в декомпозированном виде,
    # т.е. букву ё в виде двух символов е и  ̈
    # Поэтому надо нормализовать переданную строку
    text = unicodedata.normalize('NFC', text)
    processed = process(text)
    sys.stdout.write(processed.encode('utf-8'))

