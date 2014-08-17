import requests
from bs4 import BeautifulSoup
from datetime import datetime

def lobbyists():
  response = requests.get("http://www.lobbyistsregister.vic.gov.au/lobbyistsRegister/index.cfm?event=whoIsOnRegister")
  soup = BeautifulSoup(response.text)

  lobbyists = []
  for row in soup.find(id="contentLeft").find("td", text="Details Last Updated").parent.find_next_siblings("tr"):
    cells = row.find_all("td")
    lobbyist = {
      "location": "vic",
      "business_name": cells[1].text.strip(),
      "url": "http://www.lobbyistsregister.vic.gov.au/lobbyistsRegister/" + cells[1].find("a")["href"],
      "abn": cells[2].text.replace(" ", "").strip() if cells[2].text.strip() != "No A.B.N" else "",
      "last_update": cells[3].text.strip()
    }

    if lobbyist["business_name"] == "":
      raise Exception("Empty business name found for lobbyist " + row.prettify())
    if lobbyist["abn"] != "" and lobbyist["abn"].isnumeric() == False:
      raise Exception("Non-numeric ABN found for lobbyist " + row.prettify())
    try:
      datetime.strptime(lobbyist["last_update"], "%d/%m/%Y")
    except:
      raise Exception("Invalid last update date found for lobbyist " + row.prettify())

    lobbyists.append(lobbyist)
  return lobbyists
