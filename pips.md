## pip installing this list will install all the libraries needed.

flask==1.1.2
python-dotenv==0.14.0
waitress==2.0.0
python-telegram-bot >= 12.8
emoji==1.6.3
instagram-private-api @ git+https://git@github.com/ping/instagram_private_api.git@1d70e99bc11591161b0cd71cff3f0c08cd04b34f
igramscraper==0.3.5

--I had issues installing igramscraper on windows, but not on linux.
--If pip install -r requirements.txt throws an error because of igramscraper,
delete it from the list and rerun the command, then follow the instruction in '.instagram-scraper/README.md'
