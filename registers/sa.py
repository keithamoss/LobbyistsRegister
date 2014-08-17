import requests
from bs4 import BeautifulSoup
from datetime import datetime

def lobbyists():
  response = requests.get("http://www.dpc.sa.gov.au/lobbyist-who-register")
  soup = BeautifulSoup(response.text)

  lobbyists = []
  for row in soup.find("th", text="LAST UPDATED").find_parent("table").find("tbody").find_all("tr"):
    cells = row.find_all("td")
    lobbyist = {
      "location": "sa",
      "business_name": cells[0].text.split("|")[0].strip(),
      "trading_name": cells[1].text,
      "url": cells[0].find("a")["href"],
      # "abn": cells[2].text if cells[2].text != "No A.B.N" else "",
      "last_update": cells[2].text
    }

    # Patch for the single dodgy date stamp
    if lobbyist["last_update"] == "03/0702014":
      lobbyist["last_update"] = "03/07/2014"

    if lobbyist["business_name"] == "":
      raise Exception("Empty business name found for lobbyist " + row.prettify())
    if lobbyist["trading_name"] == "":
      raise Exception("Empty trading name found for lobbyist " + row.prettify())
    # if lobbyist["abn"] != "" and lobbyist["abn"].isnumeric() == False:
    #   raise Exception("Non-numeric ABN found for lobbyist " + row.prettify())
    try:
      datetime.strptime(lobbyist["last_update"], "%d/%m/%Y")
    except:
      raise Exception("Invalid last update date found for lobbyist " + row.prettify())

    lobbyists.append(lobbyist)
  return lobbyists
