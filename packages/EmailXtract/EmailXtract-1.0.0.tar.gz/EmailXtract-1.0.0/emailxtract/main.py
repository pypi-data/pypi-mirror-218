from emailxtract.scraper import EmailScraper

url = 'http://testphp.vulnweb.com/'
scraper = EmailScraper(url)
scraper.scrape_emails()

emails = scraper.get_emails()

if len(emails) > 0:
    for email in emails:
        print(email)
else:
    print("No emails found on", url)
