from registers import *
import scraperwiki

for l in wa.lobbyists():
  scraperwiki.sqlite.save(unique_keys=['business_name', 'location'], data=l)

for l in sa.lobbyists():
  scraperwiki.sqlite.save(unique_keys=['business_name', 'location'], data=l)

for l in nsw.lobbyists():
  scraperwiki.sqlite.save(unique_keys=['business_name', 'location'], data=l)

for l in qld.lobbyists():
  scraperwiki.sqlite.save(unique_keys=['business_name', 'location'], data=l)

for l in vic.lobbyists():
  scraperwiki.sqlite.save(unique_keys=['business_name', 'location'], data=l)

for l in tas.lobbyists():
  scraperwiki.sqlite.save(unique_keys=['business_name', 'location'], data=l)

for l in fed.lobbyists():
  scraperwiki.sqlite.save(unique_keys=['business_name', 'location'], data=l)
