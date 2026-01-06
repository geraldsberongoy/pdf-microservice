import requests
from concurrent.futures import ThreadPoolExecutor

# Using the Production URL as per your previous test suite
# URL = "http://localhost:8080/generate-pdf" 
URL = "https://pdf-service-374437162930.asia-southeast1.run.app/generate-pdf"

DOC_URL = "https://docs.google.com/document/d/12Sj91nc5-t2na0UeoUpnIP3cTseSPudJ"
TOTAL_REQUESTS = 20  # Limit is 10/min, so 20 should easily trigger it
WORKERS = 5

print(f"🚀 Starting PDF Generation Rate Limit Test")
print(f"Target: {URL}")
print(f"Goal: Send {TOTAL_REQUESTS} POST requests (Limit is 10/min)")

success_count = 0
blocked_count = 0
error_count = 0

def send_request(index):
    try:
        # Note: We don't care about the PDF content here, just the status code
        response = requests.post(URL, json={"url": DOC_URL}, stream=True)
        
        # Consuming content is important to close connections properly, 
        # but for a rate limit test we can just check headers/status.
        response.close() 

        if response.status_code == 200:
            return "OK"
        elif response.status_code == 429:
            return "BLOCKED"
        else:
            return f"ERROR_{response.status_code}"
    except Exception as e:
        return f"FAIL_{str(e)}"

# Run requests in parallel
with ThreadPoolExecutor(max_workers=WORKERS) as executor:
    results = list(executor.map(send_request, range(TOTAL_REQUESTS)))

# Tally results
for res in results:
    if res == "OK":
        success_count += 1
    elif res == "BLOCKED":
        blocked_count += 1
    else:
        error_count += 1
        print(f"Error detail: {res}")

print("\n--- PDF Generation Test Results ---")
print(f"✅ Successful (200 OK): {success_count}")
print(f"⛔ Blocked (429): {blocked_count}")
print(f"⚠️ Errors: {error_count}")

if blocked_count > 0:
    print("✅ SUCCESS: Rate limiting triggered correctly on POST endpoint.")
else:
    print("❌ FAILURE: No requests were blocked. Did you update the cloud deployment?")
