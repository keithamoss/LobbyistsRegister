import requests
from bs4 import BeautifulSoup
from datetime import datetime

def lobbyists():
  response = requests.get("https://www.lobbyists.wa.gov.au/Pages/WhoIsOnTheRegister.aspx")
  soup = BeautifulSoup(response.text)

  lobbyists = []
  for row in soup.find(id="LeftColumn").find("th", text="Details Last Updated").parent.next_siblings:
    cells = row.find_all("td")
    lobbyist = {
      "location": "wa",
      "business_name": cells[1].text,
      "url": "https://www.lobbyists.wa.gov.au/Pages/" + cells[1].find("a")["href"],
      "abn": cells[2].text if cells[2].text != "No A.B.N" else "",
      "last_update": cells[3].text
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
