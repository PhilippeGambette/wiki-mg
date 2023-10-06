# -*- coding: utf-8 -*-
import csv, glob, os, re, requests, sys, time
from xml.dom import minidom

# Get the current folder
folder = os.path.abspath(os.path.dirname(sys.argv[0]))
fileName = "mgwiki-latest-pages-articles.xml"
# Open the dump file of wikipedia in Malagasy
wikipedia = minidom.parse(fileName)
metadataFile = open("pages.csv", "w", encoding="utf8", errors="ignore")

pageNb = 0
for page in wikipedia.getElementsByTagName("page"):
   title = ""
   for titleTag in page.getElementsByTagName("title"):
      if titleTag.firstChild != None:
         title = str(titleTag.firstChild.nodeValue)
         print(title)
   text = ""
   size = 0
   for textTag in page.getElementsByTagName("text"):
      if textTag.firstChild != None:
         text = str(textTag.firstChild.nodeValue)
         size = str(textTag.getAttribute("bytes"))
         print(size)
   pageNb += 1
   print("page #" + str(pageNb))
   if int(size) > 500:
      outputFile = open("page" + str(pageNb) + ".txt", "w", encoding="utf8", errors="ignore")
      outputFile.writelines(title + "\n")
      outputFile.writelines(text)
      outputFile.close()
   metadataFile.writelines(str(title) + "\t" + str(size) +"\n")
metadataFile.close()

# Wikidata query
# 100 639 results on 2023-10-06
"""
#Éléments ayant un lien de site Wikipedia en malgache
SELECT ?item ?itemLabel ?article
WITH {
  SELECT *
  WHERE {
    ?article schema:about ?item ;
      schema:isPartOf <https://mg.wikipedia.org/> .
  }
  LIMIT 1000000
} AS %i
WHERE {
  INCLUDE %i
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" . }
}
"""