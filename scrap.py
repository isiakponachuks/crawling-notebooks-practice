import requests
import matplotlib.pyplot as plt # Import this!
from bs4 import BeautifulSoup
from collections import defaultdict


# --- (Previous functions: get_soup, extract_job_postings, clean_job_data,
#      filter_jobs_by_keyword, count_jobs_by_field) ---

# Assume these functions are defined as in previous examples.
# For brevity, I'm only including the `count_jobs_by_field` here,
# but remember you'd need all the preceding data processing steps.

def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def extract_job_postings(soup_object):
    all_job_cards = soup_object.find_all("div", class_="card-content")
    jobs_list = []
    for job_card_element in all_job_cards:
        title_element = job_card_element.find("h2", class_="title")
        company_element = job_card_element.find("h3", class_="company")
        location_element = job_card_element.find("p", class_="location")
        link_element = job_card_element.find("a", string="Apply")

        title = title_element.text.strip() if title_element else "N/A"
        company = company_element.text.strip() if company_element else "N/A"
        location = location_element.text.strip() if location_element else "N/A"
        link = link_element['href'] if link_element else "N/A"

        jobs_list.append({
            "title": title,
            "company": company,
            "location": location,
            "link": link
        })
    return jobs_list

def clean_job_data(jobs):
    cleaned_jobs = []
    for job in jobs:
        cleaned_job = {}
        cleaned_job['title'] = job.get('title', 'N/A').strip()
        cleaned_job['company'] = job.get('company', 'N/A').strip()
        cleaned_job['location'] = job.get('location', 'N/A').strip()
        cleaned_job['link'] = job.get('link', 'N/A').strip()
        cleaned_jobs.append(cleaned_job)
    return cleaned_jobs

def count_jobs_by_field(jobs, field):
    field_counts = defaultdict(int)
    for job in jobs:
        field_value = job.get(field, '').strip()
        if field_value:
            field_counts[field_value] += 1
    return dict(field_counts)

# --- Your plotting functions (as corrected above) ---
def plot_jobs_by_location(job_counts):
    if not job_counts:
        print("No job location data to plot.")
        return
    locations = list(job_counts.keys())
    counts = list(job_counts.values())
    plt.figure(figsize=(10, 6))
    plt.bar(locations, counts, color='skyblue')
    plt.xlabel("Location")
    plt.ylabel("Number of Job Postings")
    plt.title("Number of Job Postings by Location")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_top_companies(job_counts, top_n=5):
    if not job_counts:
        print("No data to plot.")
        return
    sorted_companies = sorted(job_counts.items(), key=lambda item: item[1], reverse=True)
    top_n_companies = sorted_companies[:top_n]
    company_names = [company[0] for company in top_n_companies]
    job_counts_values = [company[1] for company in top_n_companies]
    if len(sorted_companies) > top_n:
        other_count = sum(company[1] for company in sorted_companies[top_n:])
        company_names.append(f'Other ({len(sorted_companies) - top_n} companies)')
        job_counts_values.append(other_count)
    plt.figure(figsize=(8, 8))
    plt.pie(job_counts_values, labels=company_names, autopct='%1.1f%%', startangle=140, pctdistance=0.85)
    plt.title(f"Top {top_n} Companies by Job Postings")
    plt.axis('equal')
    plt.show()

# --- Main Execution ---
job_url = "https://realpython.github.io/fake-jobs/"
soup = get_soup(job_url)
raw_jobs = extract_job_postings(soup)
cleaned_jobs = clean_job_data(raw_jobs)

# Get job counts by location
location_job_counts = count_jobs_by_field(cleaned_jobs, 'location')

# Plot jobs by location
print("\nGenerating Job Postings by Location Bar Chart...")
plot_jobs_by_location(location_job_counts)


# Get job counts by company
company_job_counts = count_jobs_by_field(cleaned_jobs, 'company')

# Plot top companies
print("\nGenerating Top Companies by Job Postings Pie Chart...")
plot_top_companies(company_job_counts, top_n=10) 
# You can adjust top_n
