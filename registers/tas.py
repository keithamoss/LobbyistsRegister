import requests
from bs4 import BeautifulSoup
from datetime import datetime

def lobbyists():
  response = requests.get("http://lobbyists.dpac.tas.gov.au/lobbyist_register")
  soup = BeautifulSoup(response.text)

  lobbyists = []
  for row in soup.find(id="lobbyistsTable").find_all("tr")[1:]:
    cells = row.find_all("td")
    lobbyist = {
      "location": "tas",
      "business_name": cells[1].text,
      "trading_name": cells[2].text,
      "url": cells[1].find("a")["href"],
      "abn": cells[3].text.replace(" ", ""),
      "last_update": datetime.strptime(cells[4].text.strip(), "%d %b %Y").strftime("%d/%m/%Y")
    }

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
