import httpx
import os
from dotenv import load_dotenv
from groq_llm import explain_recommendations
from utils import logger, log_search
from bs4 import BeautifulSoup
import requests

load_dotenv()

NEWSDATA_API_KEY = os.getenv("NEWSDATA_API_KEY")
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "in")
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "en")

def fetch_news(query):
    url = f"https://newsdata.io/api/1/news?apikey={NEWSDATA_API_KEY}&q={query}&country={DEFAULT_COUNTRY}&language={DEFAULT_LANGUAGE}"
    try:
        response = httpx.get(url, timeout=15)
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        logger.error(f"News API error: {e}")
        return []

def fetch_jobs(prompt):
    url = f"https://internshala.com/internships/keywords-{prompt.replace(' ', '%20')}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')

    jobs = []
    for job_card in soup.find_all('div', class_='individual_internship', limit=10):
        try:
            title_tag = job_card.find('h3')
            title = title_tag.text.strip() if title_tag else 'N/A'

            link_tag = job_card.find('a')
            link = 'https://internshala.com' + link_tag['href'] if link_tag and link_tag.has_attr('href') else 'N/A'

            company_tag = job_card.find('a', class_='link_display_like_text')
            company = company_tag.text.strip() if company_tag else 'N/A'

            details_tag = job_card.find('div', class_='internship_other_details_container')
            details = details_tag.text.strip().replace('\n', ' ') if details_tag else 'N/A'

            stipend_tag = job_card.find('span', class_='stipend')
            stipend = stipend_tag.text.strip() if stipend_tag else 'N/A'

            description = f"{company} - {details} - Stipend: {stipend}"

            jobs.append({
                "title": title,
                "url": link,
                "company": company,
                "description": description,
            })
        except Exception as e:
            logger.error(f"Error parsing job: {e}")
            continue

    return jobs

def recommend_articles(prompt, page=1, page_size=5):
    log_search(prompt)
    articles = fetch_news(prompt)
    titles = [a.get("title", "") for a in articles]
    explanations = explain_recommendations(prompt, titles)

    recs = []
    for article, explanation in zip(articles, explanations):
        recs.append({
            "type": "news",
            "title": article.get("title"),
            "url": article.get("link"),
            "description": article.get("description", ""),
            "pubDate": article.get("pubDate", ""),
            "why": explanation
        })

    start = (page - 1) * page_size
    end = start + page_size
    return recs[start:end]

def recommend_jobs(prompt, page=1, page_size=5):
    log_search(prompt)
    jobs = fetch_jobs(prompt)
    filtered_jobs = [job for job in jobs if prompt.lower() in job.get("title", "").lower()]

    titles = [job.get("title", "") for job in filtered_jobs]
    explanations = explain_recommendations(prompt, titles)

    recs = []
    for job, explanation in zip(filtered_jobs, explanations):
        recs.append({
            "type": "job",
            "title": job.get("title"),
            "url": job.get("url"),
            "company": job.get("company"),
            "description": job.get("description"),
            "why": explanation
        })

    start = (page - 1) * page_size
    end = start + page_size
    return recs[start:end] or [{"type": "job", "title": f"No jobs found with '{prompt}' in the title", "url": "", "why": "Try another search term."}]
