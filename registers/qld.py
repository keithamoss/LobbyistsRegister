import requests
from bs4 import BeautifulSoup
from datetime import datetime

def lobbyists():
  response = requests.get("http://lobbyists.integrity.qld.gov.au/who-is-on-the-register.aspx")
  soup = BeautifulSoup(response.text)

  lobbyists = []
  for row in soup.find(id="content").find("th", text="Last Updated").find_parent("thead").next_sibling.find_all("tr"):
    cells = row.find_all("td")
    lobbyist = {
      "location": "qld",
      "business_name": cells[1].text,
      "trading_name": cells[0].text,
      "url": "", # Argh, what's wrong with a bloody <a>, Queensland?!?
      # "url": "https://www.lobbyists.wa.gov.au/Pages/" + cells[1].find("a")["href"],
      "abn": cells[2].text.replace(" ", "").replace("ABN", "").strip(),
      "last_update": cells[3].text
    }

    if lobbyist["business_name"] == "":
      raise Exception("Empty business name found for lobbyist " + row.prettify())
    # Some rows contain ACNs - too hard for now!
    # if lobbyist["abn"] != "" and lobbyist["abn"].isnumeric() == False:
      # raise Exception("Non-numeric ABN found for lobbyist " + row.prettify())
    try:
      datetime.strptime(lobbyist["last_update"], "%d/%m/%Y")
    except:
      raise Exception("Invalid last update date found for lobbyist " + row.prettify())

    lobbyists.append(lobbyist)
  return lobbyists
