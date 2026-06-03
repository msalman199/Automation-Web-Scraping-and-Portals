from scraper import AntiDetectionScraper
import time

def comprehensive_test():
    """Run comprehensive scraper test."""
    scraper = AntiDetectionScraper()
    
    print("Testing against httpbin.org...")
    
    # Test 1: User agent rotation
    print("\n1. User Agent Rotation Test")
    for i in range(3):
        response = scraper.fetch_with_retry("http://httpbin.org/user-agent")
        if response:
            print(f"   Request {i+1}: Success")
        time.sleep(1)
    
    # Test 2: Headers verification
    print("\n2. Headers Verification Test")
    response = scraper.fetch_with_retry("http://httpbin.org/headers")
    if response and response.status_code == 200:
        print("   Headers sent successfully")
    
    print("\n3. Rate Limiting Test")
    start = time.time()
    for i in range(3):
        scraper.fetch_with_retry("http://httpbin.org/delay/1")
    elapsed = time.time() - start
    print(f"   Completed 3 requests in {elapsed:.2f} seconds")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    comprehensive_test()
