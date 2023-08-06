from scrapers import malawi_voice

malawi_voice_scraper = malawi_voice.MalawiVoiceScraper()
print(malawi_voice_scraper.scrape_news())