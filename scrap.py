import requests
from bs4 import BeautifulSoup
import pandas as pd


job_data = []

try:
    for i in range(0, 9):  
        url = f'https://wuzzuf.net/a/Search-Jobs-in-Egypt?start={i}'
        page = requests.get(url)
        
        if page.status_code != 200:
            print(f"Failed to load page {i}")
            continue  
        
        soup = BeautifulSoup(page.content, "html.parser")
        jobs_block = soup.find('div', {'class': 'css-9i2afk'})
        
        
        jobs = jobs_block.find_all("div", {'class': 'css-1gatmva e1v1l3u10'})
        
        for job in jobs:
            try:
                job_title = job.find("h2", {'class': 'css-m604qf'})
                job_title = job_title.a.text.strip() if job_title and job_title.a else "N/A"

                company_tag = job.find('div', {'class': 'css-d7j1kk'})
                company = company_tag.a.text.strip('-') if company_tag and company_tag.a else "N/A"

                city_tag = company_tag.find('span', {'class': 'css-5wys0k'}) if company_tag else None
                city = city_tag.text.strip().split(',')[1] if city_tag else "N/A"

                field_tags = job.find_all('a', {'class': 'css-o171kl'})
                field_name = field_tags[2].text.strip(' · ') if len(field_tags) > 2 else "N/A"

                skill_tags = job.find_all('a', {'class': 'css-5x9pm1'})
                skills = ', '.join(skill.text.strip(' · ') for skill in skill_tags) if skill_tags else "N/A"

                date_tag = job.find('div', {'class': 'css-d7j1kk'})
                date = date_tag.div.text.strip() if date_tag else "N/A"

                # Add job to list
                job_data.append({
                    'Job Title': job_title,
                    'Company': company,
                    'City': city,
                    'Field': field_name,
                    'Skills': skills,
                    'Date': date
                })

            except Exception as e:
                print(f"Error scraping job: {e}")

    
    df = pd.DataFrame(job_data)
    df.to_excel('wuzzuf_jobs.xlsx', index=False)
    print("Data has been written to 'wuzzuf_jobs.xlsx'")

except Exception as e:
    print("Critical Error:", e)
