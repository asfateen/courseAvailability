import requests
import os
import sys

URL = "https://register.nu.edu.eg/PowerCampusSelfService/Sections/AdvancedSearch"

COOKIES = os.getenv("NU_COOKIES")
if not COOKIES:
    print("::error ::Missing NU_COOKIES secret")
    sys.exit(1)

HEADERS = {
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.8",
    "cache-control": "max-age=0",
    "content-type": "application/json",
    "origin": "https://register.nu.edu.eg",
    "priority": "u=1, i",
    "referer": "https://register.nu.edu.eg/PowerCampusSelfService/Registration/Courses",
    "sec-ch-ua": '"Chromium";v="140", "Not=A?Brand";v="24", "Brave";v="140"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "cookie": COOKIES.strip()
}

COURSES = ["arts-201", "ssci101"]

def check_course(course):
    data = {
        "endDateKey": 0,
        "eventId": "",
        "keywords": course,
        "registrationtype": "TRAD",
        "startDateKey": 0,
        "period": "2025/FALL"
    }

    try:
        response = requests.post(URL, headers=HEADERS, json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"::error ::Request failed for {course}: {e}")
        return None

    # Ensure it's valid JSON before processing
    try:
        result = response.json()
    except ValueError:
        print(f"::error ::Invalid JSON for {course}, maybe session expired?")
        return None

    # Debug: Check if result is empty
    if not result:
        print(f"::error ::Empty result for {course}, could be bad cookie/session expired")
        return None

    # Convert to string and check cartable status
    text = response.text
    if '"isCartable":true' in text:
        print(f"::warning ::Seats available for {course.upper()}! Go register NOW!")
        return True
    else:
        print(f"No seats available for {course.upper()}.")
        return False

def main():
    any_available = False
    for course in COURSES:
        status = check_course(course)
        if status is None:
            # treat invalid result as an error (fail the action)
            sys.exit(1)
        elif status:
            any_available = True
    sys.exit(1 if any_available else 0)

if __name__ == "__main__":
    main()
