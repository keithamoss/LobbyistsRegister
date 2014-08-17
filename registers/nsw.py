import requests
from bs4 import BeautifulSoup
from datetime import datetime
from PyPDF2 import PdfFileReader
import os
import re
import time

def lobbyists():
  response = requests.get("http://www.dpc.nsw.gov.au/programs_and_services/lobbyist_register/who_is_on_register")
  soup = BeautifulSoup(response.text)

  lobbyists = []
  for row in soup.find(id="lobbyist-register").find_all("tr")[1:]:
    cells = row.find_all("td")
    lobbyist = {
      "location": "nsw",
      "business_name": cells[1].text,
      "trading_name": cells[2].text,
      "url": cells[1].find("a")["href"],
      "abn": cells[3].text.replace(" ", "").strip() if cells[3].text != "N/A" else ""
    }

    # All this just to get the last updated date :(
    response = requests.get(lobbyist["url"])
    with open("temp.pdf", "wb") as f:
      f.write(response.content)
    time.sleep(0.5) # Be nice

    # We can't know for sure which page the last updated date is on
    with open("temp.pdf", "rb") as f:
      pdf = PdfFileReader(f)
      text = ""
      for i in range(pdf.getNumPages()):
        text += pdf.getPage(i).extractText()
    os.remove("temp.pdf")

    m = re.search("Details last updated: ([0-9]{2}/[0-9]{2}/[0-9]{4})", text)
    if m:
      lobbyist["last_update"] = m.groups()[0]
    else:
      raise Exception("Could not scrape date from PDF for lobbyist " + text)

    if lobbyist["business_name"] == "":
      raise Exception("Empty business name found for lobbyist " + row.prettify())
    if lobbyist["trading_name"] == "":
      raise Exception("Empty trading name found for lobbyist " + row.prettify())
    if lobbyist["abn"] != "" and lobbyist["abn"].isnumeric() == False:
      raise Exception("Non-numeric ABN found for lobbyist " + row.prettify())
    try:
      datetime.strptime(lobbyist["last_update"], "%d/%m/%Y")
    except:
      raise Exception("Invalid last update date found for lobbyist " + row.prettify())

    lobbyists.append(lobbyist)
  return lobbyists
