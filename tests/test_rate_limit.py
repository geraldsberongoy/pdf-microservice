import requests
import time
from concurrent.futures import ThreadPoolExecutor

URL = "https://pdf-service-374437162930.asia-southeast1.run.app/stats?url=https://docs.google.com/document/d/12Sj91nc5-t2na0UeoUpnIP3cTseSPudJ"
TOTAL_REQUESTS = 40
WORKERS = 10  # Number of concurrent threads

print(f"🚀 Starting Fast Concurrent Rate Limit Test")
print(f"Goal: Send {TOTAL_REQUESTS} requests ASAP")

success_count = 0
blocked_count = 0
error_count = 0

def send_request(index):
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            return "OK"
        elif response.status_code == 429:
            return "BLOCKED"
        else:
            return f"ERROR_{response.status_code}"
    except Exception as e:
        return "FAIL"

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

print("\n--- Fast Test Results ---")
print(f"✅ Successful: {success_count}")
print(f"⛔ Blocked (429): {blocked_count}")
print(f"⚠️ Errors: {error_count}")

if blocked_count > 0:
    print("✅ SUCCESS: Rate limiting triggered correctly.")
else:
    print("❌ FAILURE: No requests were blocked.")
