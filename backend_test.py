#!/usr/bin/env python3
"""
FastAPI CRUD Lab Backend Testing Suite

This script tests all API endpoints against the live backend service.
Tests CRUD operations, validation, search, pagination, and error handling.
"""

import requests
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Any

class FastAPICrudTester:
    """Comprehensive API tester for FastAPI CRUD Lab"""
    
    def __init__(self, base_url: str = "https://fastapi-crud-lab.preview.emergentagent.com"):
        self.base_url = base_url.rstrip('/')
        self.tests_run = 0
        self.tests_passed = 0
        self.created_items = []  # Track items for cleanup
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        
    def log_result(self, test_name: str, success: bool, details: str = ""):
        """Log test results with colored output"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            print(f"✅ {test_name}: PASSED {details}")
        else:
            print(f"❌ {test_name}: FAILED {details}")
        return success

    def test_health_check(self) -> bool:
        """Test GET /api/health endpoint"""
        print(f"\n🔍 Testing Health Check...")
        try:
            response = self.session.get(f"{self.base_url}/api/health", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                details = f"- Status: {response.status_code} - {data.get('message', 'No message')}"
            else:
                details = f"- Expected 200, got {response.status_code}"
                
            return self.log_result("Health Check", success, details)
        except Exception as e:
            return self.log_result("Health Check", False, f"- Error: {str(e)}")

    def test_root_endpoint(self) -> bool:
        """Test GET /api/ root endpoint"""
        print(f"\n🔍 Testing Root API Endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/api/", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                details = f"- Status: {response.status_code} - {data.get('message', 'No message')}"
            else:
                details = f"- Expected 200, got {response.status_code}"
                
            return self.log_result("Root API Endpoint", success, details)
        except Exception as e:
            return self.log_result("Root API Endpoint", False, f"- Error: {str(e)}")

    def test_landing_page(self) -> bool:
        """Test GET / landing page loads"""
        print(f"\n🔍 Testing Landing Page...")
        try:
            response = self.session.get(f"{self.base_url}/", timeout=10)
            success = response.status_code == 200 and "FastAPI CRUD Lab" in response.text
            
            if success:
                details = f"- Status: {response.status_code} - HTML page loads correctly"
            else:
                details = f"- Status: {response.status_code} - Page content issue"
                
            return self.log_result("Landing Page", success, details)
        except Exception as e:
            return self.log_result("Landing Page", False, f"- Error: {str(e)}")

    def test_swagger_docs(self) -> bool:
        """Test GET /api/docs Swagger UI loads"""
        print(f"\n🔍 Testing Swagger Documentation...")
        try:
            response = self.session.get(f"{self.base_url}/api/docs", timeout=10)
            success = response.status_code == 200 and ("swagger" in response.text.lower() or "openapi" in response.text.lower())
            
            if success:
                details = f"- Status: {response.status_code} - Swagger UI accessible"
            else:
                details = f"- Status: {response.status_code} - Swagger UI not loading properly"
                
            return self.log_result("Swagger Documentation", success, details)
        except Exception as e:
            return self.log_result("Swagger Documentation", False, f"- Error: {str(e)}")

    def test_create_item_valid(self) -> Dict[str, Any]:
        """Test POST /api/items with valid data (should return 201)"""
        print(f"\n🔍 Testing Create Item (Valid Data)...")
        
        item_data = {
            "name": "Test Laptop",
            "description": "High-performance laptop for testing",
            "price": 999.99,
            "quantity": 10,
            "category": "Electronics"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/items", json=item_data, timeout=10)
            success = response.status_code == 201
            
            if success:
                created_item = response.json()
                self.created_items.append(created_item["id"])
                details = f"- Status: 201 - Item ID: {created_item['id']}"
                self.log_result("Create Item (Valid)", success, details)
                return created_item
            else:
                details = f"- Expected 201, got {response.status_code} - {response.text}"
                self.log_result("Create Item (Valid)", success, details)
                return {}
        except Exception as e:
            self.log_result("Create Item (Valid)", False, f"- Error: {str(e)}")
            return {}

    def test_create_item_negative_price(self) -> bool:
        """Test POST /api/items with negative price (should return 422)"""
        print(f"\n🔍 Testing Create Item (Negative Price Validation)...")
        
        item_data = {
            "name": "Invalid Item",
            "price": -100.00,  # Invalid: negative price
            "quantity": 5
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/items", json=item_data, timeout=10)
            success = response.status_code == 422
            
            if success:
                details = f"- Status: 422 - Validation correctly rejected negative price"
            else:
                details = f"- Expected 422, got {response.status_code}"
                
            return self.log_result("Create Item (Negative Price)", success, details)
        except Exception as e:
            return self.log_result("Create Item (Negative Price)", False, f"- Error: {str(e)}")

    def test_create_item_empty_name(self) -> bool:
        """Test POST /api/items with empty name (should return 422)"""
        print(f"\n🔍 Testing Create Item (Empty Name Validation)...")
        
        item_data = {
            "name": "",  # Invalid: empty name
            "price": 50.00,
            "quantity": 5
        }
        
        try:
            response = self.session.post(f"{self.base_url}/api/items", json=item_data, timeout=10)
            success = response.status_code == 422
            
            if success:
                details = f"- Status: 422 - Validation correctly rejected empty name"
            else:
                details = f"- Expected 422, got {response.status_code}"
                
            return self.log_result("Create Item (Empty Name)", success, details)
        except Exception as e:
            return self.log_result("Create Item (Empty Name)", False, f"- Error: {str(e)}")

    def test_list_items_pagination(self) -> bool:
        """Test GET /api/items with pagination"""
        print(f"\n🔍 Testing List Items with Pagination...")
        
        try:
            # Test default pagination
            response = self.session.get(f"{self.base_url}/api/items", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                has_pagination_fields = all(field in data for field in ["items", "total", "page", "page_size", "total_pages"])
                success = has_pagination_fields
                
                if success:
                    details = f"- Status: 200 - Total items: {data['total']}, Page: {data['page']}/{data['total_pages']}"
                else:
                    details = f"- Missing pagination fields in response"
            else:
                details = f"- Expected 200, got {response.status_code}"
                
            return self.log_result("List Items (Pagination)", success, details)
        except Exception as e:
            return self.log_result("List Items (Pagination)", False, f"- Error: {str(e)}")

    def test_search_items(self) -> bool:
        """Test GET /api/items?search=laptop"""
        print(f"\n🔍 Testing Search Items...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/items?search=laptop", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                # Check if search actually filters results
                search_worked = True
                for item in data.get("items", []):
                    if "laptop" not in item.get("name", "").lower():
                        search_worked = False
                        break
                
                success = search_worked
                details = f"- Status: 200 - Found {len(data.get('items', []))} items matching 'laptop'"
            else:
                details = f"- Expected 200, got {response.status_code}"
                
            return self.log_result("Search Items", success, details)
        except Exception as e:
            return self.log_result("Search Items", False, f"- Error: {str(e)}")

    def test_filter_by_category(self) -> bool:
        """Test GET /api/items?category=Electronics"""
        print(f"\n🔍 Testing Filter by Category...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/items?category=Electronics", timeout=10)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                # Check if filter actually works
                filter_worked = True
                for item in data.get("items", []):
                    if item.get("category", "").lower() != "electronics":
                        filter_worked = False
                        break
                
                success = filter_worked
                details = f"- Status: 200 - Found {len(data.get('items', []))} Electronics items"
            else:
                details = f"- Expected 200, got {response.status_code}"
                
            return self.log_result("Filter by Category", success, details)
        except Exception as e:
            return self.log_result("Filter by Category", False, f"- Error: {str(e)}")

    def test_get_item_by_id(self, item_id: str) -> bool:
        """Test GET /api/items/{id} with valid ID"""
        print(f"\n🔍 Testing Get Item by ID...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/items/{item_id}", timeout=10)
            success = response.status_code == 200
            
            if success:
                item = response.json()
                details = f"- Status: 200 - Retrieved item: {item.get('name', 'Unknown')}"
            else:
                details = f"- Expected 200, got {response.status_code}"
                
            return self.log_result("Get Item by ID", success, details)
        except Exception as e:
            return self.log_result("Get Item by ID", False, f"- Error: {str(e)}")

    def test_get_nonexistent_item(self) -> bool:
        """Test GET /api/items/{id} with non-existent ID (should return 404)"""
        print(f"\n🔍 Testing Get Non-existent Item...")
        
        fake_id = "00000000-0000-0000-0000-000000000000"
        try:
            response = self.session.get(f"{self.base_url}/api/items/{fake_id}", timeout=10)
            success = response.status_code == 404
            
            if success:
                details = f"- Status: 404 - Correctly returned not found"
            else:
                details = f"- Expected 404, got {response.status_code}"
                
            return self.log_result("Get Non-existent Item", success, details)
        except Exception as e:
            return self.log_result("Get Non-existent Item", False, f"- Error: {str(e)}")

    def test_update_item(self, item_id: str) -> bool:
        """Test PUT /api/items/{id} with partial update"""
        print(f"\n🔍 Testing Update Item...")
        
        update_data = {
            "price": 899.99,
            "quantity": 15
        }
        
        try:
            response = self.session.put(f"{self.base_url}/api/items/{item_id}", json=update_data, timeout=10)
            success = response.status_code == 200
            
            if success:
                updated_item = response.json()
                # Verify update actually happened
                price_updated = updated_item.get("price") == 899.99
                quantity_updated = updated_item.get("quantity") == 15
                success = price_updated and quantity_updated
                
                if success:
                    details = f"- Status: 200 - Price: {updated_item['price']}, Quantity: {updated_item['quantity']}"
                else:
                    details = f"- Update fields not properly applied"
            else:
                details = f"- Expected 200, got {response.status_code}"
                
            return self.log_result("Update Item", success, details)
        except Exception as e:
            return self.log_result("Update Item", False, f"- Error: {str(e)}")

    def test_delete_item(self, item_id: str) -> bool:
        """Test DELETE /api/items/{id}"""
        print(f"\n🔍 Testing Delete Item...")
        
        try:
            response = self.session.delete(f"{self.base_url}/api/items/{item_id}", timeout=10)
            success = response.status_code == 200
            
            if success:
                # Verify item is actually deleted by trying to get it
                get_response = self.session.get(f"{self.base_url}/api/items/{item_id}", timeout=10)
                actually_deleted = get_response.status_code == 404
                success = actually_deleted
                
                if success:
                    details = f"- Status: 200 - Item successfully deleted and verified"
                    # Remove from tracking list
                    if item_id in self.created_items:
                        self.created_items.remove(item_id)
                else:
                    details = f"- Delete responded 200 but item still exists"
            else:
                details = f"- Expected 200, got {response.status_code}"
                
            return self.log_result("Delete Item", success, details)
        except Exception as e:
            return self.log_result("Delete Item", False, f"- Error: {str(e)}")

    def test_statistics_endpoint(self) -> bool:
        """Test GET /api/items/stats/summary"""
        print(f"\n🔍 Testing Statistics Endpoint...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/items/stats/summary", timeout=10)
            success = response.status_code == 200
            
            if success:
                stats = response.json()
                required_fields = ["total_items", "total_quantity", "total_value", "average_price"]
                has_required_fields = all(field in stats for field in required_fields)
                success = has_required_fields
                
                if success:
                    details = f"- Status: 200 - Total items: {stats['total_items']}, Avg price: ${stats['average_price']}"
                else:
                    details = f"- Missing required statistics fields"
            else:
                details = f"- Expected 200, got {response.status_code}"
                
            return self.log_result("Statistics Endpoint", success, details)
        except Exception as e:
            return self.log_result("Statistics Endpoint", False, f"- Error: {str(e)}")

    def cleanup_test_items(self):
        """Clean up any items created during testing"""
        print(f"\n🧹 Cleaning up test items...")
        
        for item_id in self.created_items[:]:  # Copy list to avoid modification during iteration
            try:
                self.session.delete(f"{self.base_url}/api/items/{item_id}", timeout=5)
                print(f"   Cleaned up item: {item_id}")
            except Exception as e:
                print(f"   Failed to cleanup item {item_id}: {e}")
        
        self.created_items.clear()

    def run_all_tests(self) -> Dict[str, Any]:
        """Run comprehensive test suite"""
        print(f"🚀 Starting FastAPI CRUD Lab Backend Testing")
        print(f"📍 Testing against: {self.base_url}")
        print("=" * 80)
        
        # Test basic endpoints first
        self.test_health_check()
        self.test_root_endpoint()
        self.test_landing_page()
        self.test_swagger_docs()
        
        # Test CRUD operations
        created_item = self.test_create_item_valid()
        item_id = created_item.get("id") if created_item else None
        
        # Test validation
        self.test_create_item_negative_price()
        self.test_create_item_empty_name()
        
        # Test read operations
        self.test_list_items_pagination()
        self.test_search_items()
        self.test_filter_by_category()
        
        if item_id:
            self.test_get_item_by_id(item_id)
            self.test_update_item(item_id)
        
        self.test_get_nonexistent_item()
        
        # Test statistics
        self.test_statistics_endpoint()
        
        # Delete test item if it exists
        if item_id:
            self.test_delete_item(item_id)
        
        # Results summary
        print("\n" + "=" * 80)
        print(f"📊 TEST RESULTS SUMMARY")
        print(f"✅ Tests Passed: {self.tests_passed}/{self.tests_run}")
        print(f"📈 Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%")
        
        if self.tests_passed == self.tests_run:
            print(f"🎉 ALL TESTS PASSED! Backend API is working correctly.")
            status = "PASS"
        else:
            print(f"⚠️  Some tests failed. Check the logs above for details.")
            status = "FAIL"
        
        return {
            "status": status,
            "tests_run": self.tests_run,
            "tests_passed": self.tests_passed,
            "success_rate": round(self.tests_passed/self.tests_run*100, 1),
            "backend_url": self.base_url
        }

def main():
    """Main execution function"""
    # Use the public backend URL
    backend_url = "https://fastapi-crud-lab.preview.emergentagent.com"
    
    tester = FastAPICrudTester(backend_url)
    
    try:
        results = tester.run_all_tests()
        
        # Return appropriate exit code
        return 0 if results["status"] == "PASS" else 1
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Testing interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        return 1
    finally:
        # Always cleanup
        tester.cleanup_test_items()

if __name__ == "__main__":
    sys.exit(main())