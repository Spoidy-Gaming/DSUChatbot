import requests
from bs4 import BeautifulSoup
import sqlite3

def fetch_and_parse(url):
    """Fetches the URL content and parses it with BeautifulSoup."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_courses(soup):
    """Extracts courses, fees, and image URLs from the soup object."""
    courses = []
    # Customize selectors based on the actual HTML structure
    course_table = soup.find('table', {'class': 'course-fees-table'})  # Update with the correct class or id
    for row in course_table.find_all('tr')[1:]:  # Skip the header row
        cells = row.find_all('td')
        course_name = cells[0].get_text(strip=True)
        course_fees = cells[1].get_text(strip=True)
        course_facilities = cells[2].get_text(strip=True)  # Assuming facilities are in the third column
        image_url = cells[3].find('img')['src']  # Assuming image URL is in the fourth column
        courses.append((course_name, course_fees, course_facilities, '', image_url))
    return courses

def extract_hostels(soup):
    """Extracts hostels, fees, and image URLs from the soup object."""
    hostels = []
    hostel_section = soup.find('div', {'id': 'hostel-info'})  # Update with the correct identifier
    for hostel in hostel_section.find_all('div', {'class': 'hostel-item'}):  # Update with the correct class
        name = hostel.find('h3').get_text(strip=True)
        fees = hostel.find('p', {'class': 'fees'}).get_text(strip=True)  # Update with the correct class
        facilities = hostel.find('p', {'class': 'facilities'}).get_text(strip=True)  # Update with the correct class
        image_url = hostel.find('img')['src']  # Extract image URL
        hostels.append((name, fees, facilities, '', image_url))
    return hostels

def extract_general_info(soup):
    """Extracts contact information and map links, along with any associated images."""
    info = []
    contact_info = soup.find('div', {'id': 'contact-details'})  # Update with the correct identifier
    address = contact_info.find('p', {'class': 'address'}).get_text(strip=True)
    phone = contact_info.find('p', {'class': 'phone'}).get_text(strip=True)
    email = contact_info.find('p', {'class': 'email'}).get_text(strip=True)
    map_link = contact_info.find('a', {'class': 'map-link'})['href']  # Update with the correct class
    info.append(('address', address, ''))
    info.append(('phone', phone, ''))
    info.append(('email', email, ''))
    info.append(('map', map_link, ''))
    return info

def insert_data_into_database(courses, hostels, general_info):
    """Inserts the extracted data into the SQLite database."""
    conn = sqlite3.connect('college_info.db')
    cursor = conn.cursor()
    
    cursor.executemany('INSERT INTO courses (name, fees, facilities, description, image_url) VALUES (?, ?, ?, ?, ?)', courses)
    cursor.executemany('INSERT INTO hostels (name, fees, facilities, description, image_url) VALUES (?, ?, ?, ?, ?)', hostels)
    cursor.executemany('INSERT INTO general_info (category, info, image_url) VALUES (?, ?, ?)', general_info)
    
    conn.commit()
    conn.close()

def main():
    # URLs to scrape
    courses_url = 'https://www.dsuniversity.ac.in/ad-fee-structure.php'
    info_url = 'https://www.dsuniversity.ac.in/index-01.php'
    
    # Fetch and parse the pages
    courses_soup = fetch_and_parse(courses_url)
    info_soup = fetch_and_parse(info_url)
    
    # Extract data
    courses = extract_courses(courses_soup)
    hostels = extract_hostels(info_soup)
    general_info = extract_general_info(info_soup)
    
    # Insert data into the database
    insert_data_into_database(courses, hostels, general_info)
    print("Data inserted successfully.")

if __name__ == '__main__':
    main()
