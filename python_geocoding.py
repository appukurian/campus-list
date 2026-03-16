#!/usr/bin/env python3
"""
Test runner for JSON sample data with comprehensive debugging and analysis
"""

import json
import time
import requests
from typing import List, Dict, Optional, Tuple
from urllib.parse import quote
import os
from datetime import datetime
import logging
import re
from pathlib import Path

class JSONTestRunner:
    def __init__(self, api_key: str, **kwargs):
        self.api_key = api_key
        self.base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        
        # Configuration
        self.config = {
            'request_delay': kwargs.get('request_delay', 0.5),
            'max_retries': kwargs.get('max_retries', 3),
            'retry_delay': kwargs.get('retry_delay', 1.0),
            'timeout': kwargs.get('timeout', 15),
            'debug_mode': kwargs.get('debug_mode', True),
        }
        
        # Kerala district boundaries for validation
        self.kerala_districts = {
            'alappuzha': {'lat_range': (9.13, 9.89), 'lng_range': (76.26, 76.75)},
            'ernakulam': {'lat_range': (9.83, 10.27), 'lng_range': (76.17, 76.83)},
            'idukki': {'lat_range': (9.23, 10.36), 'lng_range': (76.31, 77.29)},
            'kannur': {'lat_range': (11.84, 12.50), 'lng_range': (75.05, 76.47)},
            'kasaragod': {'lat_range': (12.00, 12.80), 'lng_range': (74.66, 75.58)},
            'kollam': {'lat_range': (8.72, 9.21), 'lng_range': (76.48, 77.21)},
            'kottayam': {'lat_range': (9.40, 9.86), 'lng_range': (76.31, 77.29)},
            'kozhikode': {'lat_range': (11.10, 11.93), 'lng_range': (75.53, 76.69)},
            'malappuram': {'lat_range': (10.70, 11.52), 'lng_range': (75.83, 76.69)},
            'palakkad': {'lat_range': (10.29, 11.20), 'lng_range': (76.02, 76.84)},
            'pathanamthitta': {'lat_range': (9.16, 9.69), 'lng_range': (76.50, 77.29)},
            'thiruvananthapuram': {'lat_range': (8.30, 8.97), 'lng_range': (76.88, 77.28)},
            'thrissur': {'lat_range': (10.20, 10.87), 'lng_range': (75.98, 76.90)},
            'wayanad': {'lat_range': (11.58, 11.98), 'lng_range': (75.78, 76.44)}
        }
        
        # Setup logging
        self.setup_logging()
        
        # Test results storage
        self.test_results = []
        self.summary_stats = {
            'total_tested': 0,
            'successful': 0,
            'high_confidence': 0,
            'medium_confidence': 0,
            'low_confidence': 0,
            'invalid': 0,
            'wrong_district': 0,
            'outside_kerala': 0
        }
    
    def setup_logging(self):
        """Setup logging for test runs"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f'geocoding_test_{timestamp}.log'
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"🚀 Starting geocoding test session - Log: {log_filename}")
    
    def load_sample_data(self, json_file_path: str) -> List[Dict]:
        """Load sample data from JSON file"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                sample_data = data
            elif isinstance(data, dict):
                # If it's a dict, look for common keys that might contain the array
                possible_keys = ['campuses', 'colleges', 'data', 'records', 'items']
                sample_data = None
                for key in possible_keys:
                    if key in data:
                        sample_data = data[key]
                        break
                
                if sample_data is None:
                    # If no standard key found, assume the dict itself is a single record
                    sample_data = [data]
            else:
                raise ValueError("JSON data must be a list or dictionary")
            
            self.logger.info(f"✅ Loaded {len(sample_data)} sample records from {json_file_path}")
            
            # Show sample structure
            if sample_data and self.config['debug_mode']:
                self.logger.info("📋 Sample record structure:")
                sample = sample_data[0]
                for key, value in sample.items():
                    self.logger.info(f"  {key}: {value}")
            
            return sample_data
            
        except FileNotFoundError:
            self.logger.error(f"❌ File not found: {json_file_path}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"❌ Invalid JSON format: {e}")
            raise
        except Exception as e:
            self.logger.error(f"❌ Error loading sample data: {e}")
            raise
    
    def normalize_district_name(self, district: str) -> str:
        """Normalize district names"""
        if not district:
            return ""
        
        district = district.strip().lower()
        
        # Handle common variations
        variations = {
            'tvm': 'thiruvananthapuram',
            'trivandrum': 'thiruvananthapuram',
            'kochi': 'ernakulam',
            'cochin': 'ernakulam',
            'calicut': 'kozhikode',
            'trichur': 'thrissur',
            'alleppy': 'alappuzha',
            'alleppey': 'alappuzha'
        }
        
        return variations.get(district, district)
    
    def clean_address_string(self, text: str) -> str:
        """Clean address string for better geocoding"""
        if not text:
            return ''
        
        cleaned = str(text).strip()
        
        # Remove problematic patterns
        patterns_to_remove = [
            r'\([^)]*\)',  # Remove parentheses content
            r'P\.?O\.?\s*Box[^,]*,?\s*',  # Remove PO Box
            r'Pin\s*:?\s*\d+',  # Remove pin codes
            r'Phone[^,]*,?\s*',  # Remove phone numbers
            r'Email[^,]*,?\s*',  # Remove emails
        ]
        
        for pattern in patterns_to_remove:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Clean up spacing and commas
        cleaned = re.sub(r'\s*,\s*', ', ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = re.sub(r'^,\s*|,\s*$', '', cleaned)
        
        return cleaned.strip()
    
    def generate_search_strategies(self, campus: Dict) -> List[str]:
        """Generate multiple search strategies for testing"""
        
        name = campus.get('Name', '').strip()
        address = campus.get('Address', '').strip()
        district = campus.get('District', '').strip()
        
        # Clean and normalize
        cleaned_address = self.clean_address_string(address)
        normalized_district = self.normalize_district_name(district)
        
        strategies = []
        
        # Strategy 1: Address-only (often most accurate)
        if cleaned_address:
            strategies.append({
                'query': f"{cleaned_address}, {normalized_district}, Kerala, India",
                'name': 'Address Only',
                'description': 'Using cleaned address without institution name'
            })
        
        # Strategy 2: Original address
        if address and address != cleaned_address:
            strategies.append({
                'query': f"{address}, {normalized_district}, Kerala, India",
                'name': 'Original Address',
                'description': 'Using original address as provided'
            })
        
        # Strategy 3: Name + District (traditional approach)
        if name:
            strategies.append({
                'query': f"{name}, {normalized_district}, Kerala, India",
                'name': 'Name + District',
                'description': 'Using institution name with district'
            })
        
        # Strategy 4: Simplified name (without institutional words)
        if name:
            simplified = re.sub(r'\b(College|University|Institute|School|Government|Govt)\b', '', name, flags=re.IGNORECASE)
            simplified = re.sub(r'\s+', ' ', simplified).strip()
            if simplified and simplified != name:
                strategies.append({
                    'query': f"{simplified}, {normalized_district}, Kerala, India",
                    'name': 'Simplified Name',
                    'description': 'Using simplified institution name'
                })
        
        # Strategy 5: Address without institution name (if address contains institution name)
        if address and name:
            # Try to remove institution name from address
            addr_without_name = address
            name_words = name.split()[:3]  # First 3 words of name
            for word in name_words:
                if len(word) > 3:  # Only remove meaningful words
                    addr_without_name = re.sub(rf'\b{re.escape(word)}\b', '', addr_without_name, flags=re.IGNORECASE)
            
            addr_without_name = re.sub(r'\s+', ' ', addr_without_name).strip()
            addr_without_name = re.sub(r'^,\s*|,\s*$', '', addr_without_name)
            
            if addr_without_name and addr_without_name != address:
                strategies.append({
                    'query': f"{addr_without_name}, {normalized_district}, Kerala, India",
                    'name': 'Address Without Name',
                    'description': 'Using address with institution name removed'
                })
        
        return strategies
    
    def validate_coordinates(self, lat: float, lng: float, expected_district: str) -> Dict:
        """Validate coordinates against expected district"""
        
        validation = {
            'is_valid': True,
            'confidence': 'HIGH',
            'in_kerala': False,
            'in_expected_district': False,
            'actual_district': None,
            'distance_from_expected': None,
            'warnings': []
        }
        
        # Check if in Kerala bounds
        kerala_bounds = {'lat_min': 8.0, 'lat_max': 12.8, 'lng_min': 74.8, 'lng_max': 77.4}
        
        if (kerala_bounds['lat_min'] <= lat <= kerala_bounds['lat_max'] and 
            kerala_bounds['lng_min'] <= lng <= kerala_bounds['lng_max']):
            validation['in_kerala'] = True
        else:
            validation['is_valid'] = False
            validation['confidence'] = 'INVALID'
            validation['warnings'].append(f"Coordinates outside Kerala: {lat:.4f}, {lng:.4f}")
            return validation
        
        # Find which district the coordinates are actually in
        for district_name, bounds in self.kerala_districts.items():
            lat_range, lng_range = bounds['lat_range'], bounds['lng_range']
            if (lat_range[0] <= lat <= lat_range[1] and lng_range[0] <= lng <= lng_range[1]):
                validation['actual_district'] = district_name
                break
        
        # Check if matches expected district
        normalized_expected = self.normalize_district_name(expected_district)
        
        if validation['actual_district'] == normalized_expected:
            validation['in_expected_district'] = True
            validation['confidence'] = 'HIGH'
        elif validation['actual_district']:
            validation['confidence'] = 'LOW'
            validation['warnings'].append(
                f"Expected {normalized_expected}, found in {validation['actual_district']}"
            )
        else:
            validation['confidence'] = 'MEDIUM'
            validation['warnings'].append("Could not determine district from coordinates")
        
        return validation
    
    def test_campus(self, campus: Dict) -> Dict:
        """Test geocoding for a single campus with all strategies"""
        
        campus_name = campus.get('Name', 'Unknown')
        expected_district = campus.get('District', 'Unknown')
        
        print(f"\n{'='*80}")
        print(f"🧪 TESTING: {campus_name}")
        print(f"📍 Expected District: {expected_district}")
        print(f"{'='*80}")
        
        # Show input data
        print(f"\n📋 INPUT DATA:")
        for key, value in campus.items():
            print(f"  {key}: {value}")
        
        # Generate and test strategies
        strategies = self.generate_search_strategies(campus)
        print(f"\n🔍 TESTING {len(strategies)} SEARCH STRATEGIES:")
        
        results = []
        best_result = None
        best_confidence = 'INVALID'
        
        for i, strategy in enumerate(strategies, 1):
            print(f"\n--- Strategy {i}: {strategy['name']} ---")
            print(f"Description: {strategy['description']}")
            print(f"Query: {strategy['query']}")
            
            try:
                # Make API request
                result = self.make_geocoding_request(strategy['query'])
                
                if result.get('status') == 'OK' and result.get('results'):
                    location = result['results'][0]['geometry']['location']
                    lat, lng = location['lat'], location['lng']
                    formatted_address = result['results'][0].get('formatted_address', '')
                    
                    # Validate coordinates
                    validation = self.validate_coordinates(lat, lng, expected_district)
                    
                    strategy_result = {
                        'strategy': strategy,
                        'coordinates': [lng, lat],
                        'formatted_address': formatted_address,
                        'validation': validation
                    }
                    
                    results.append(strategy_result)
                    
                    # Print results
                    print(f"✅ SUCCESS: {lat:.6f}, {lng:.6f}")
                    print(f"   Address: {formatted_address}")
                    print(f"   Confidence: {validation['confidence']}")
                    print(f"   In Expected District: {'✅' if validation['in_expected_district'] else '❌'}")
                    
                    if validation['actual_district']:
                        print(f"   Detected District: {validation['actual_district']}")
                    
                    if validation['warnings']:
                        for warning in validation['warnings']:
                            print(f"   ⚠️  {warning}")
                    
                    # Track best result
                    confidence_ranking = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1, 'INVALID': 0}
                    if confidence_ranking[validation['confidence']] > confidence_ranking[best_confidence]:
                        best_result = strategy_result
                        best_confidence = validation['confidence']
                
                else:
                    print(f"❌ FAILED: {result.get('status', 'Unknown error')}")
                    results.append({
                        'strategy': strategy,
                        'error': result.get('status', 'Unknown error')
                    })
                
                time.sleep(self.config['request_delay'])
                
            except Exception as e:
                print(f"❌ ERROR: {str(e)}")
                results.append({
                    'strategy': strategy,
                    'error': str(e)
                })
        
        # Summary for this campus
        print(f"\n📊 SUMMARY FOR {campus_name}:")
        print(f"  Strategies Tested: {len(strategies)}")
        successful = [r for r in results if 'coordinates' in r]
        print(f"  Successful: {len(successful)}")
        
        if best_result:
            print(f"  🏆 BEST RESULT:")
            print(f"    Strategy: {best_result['strategy']['name']}")
            print(f"    Confidence: {best_result['validation']['confidence']}")
            print(f"    Coordinates: {best_result['coordinates'][1]:.6f}, {best_result['coordinates'][0]:.6f}")
            print(f"    In Correct District: {'✅' if best_result['validation']['in_expected_district'] else '❌'}")
        else:
            print(f"  ❌ NO SUCCESSFUL RESULTS")
        
        # Store test result
        test_result = {
            'campus': campus,
            'strategies_tested': strategies,
            'results': results,
            'best_result': best_result,
            'timestamp': datetime.now().isoformat()
        }
        
        self.test_results.append(test_result)
        self.update_summary_stats(test_result)
        
        return test_result
    
    def make_geocoding_request(self, query: str) -> Dict:
        """Make geocoding API request"""
        url = f"{self.base_url}?address={quote(query)}&key={self.api_key}&region=in"
        
        response = requests.get(url, timeout=self.config['timeout'])
        response.raise_for_status()
        return response.json()
    
    def update_summary_stats(self, test_result: Dict):
        """Update summary statistics"""
        self.summary_stats['total_tested'] += 1
        
        if test_result['best_result']:
            self.summary_stats['successful'] += 1
            confidence = test_result['best_result']['validation']['confidence']
            
            if confidence == 'HIGH':
                self.summary_stats['high_confidence'] += 1
            elif confidence == 'MEDIUM':
                self.summary_stats['medium_confidence'] += 1
            elif confidence == 'LOW':
                self.summary_stats['low_confidence'] += 1
            else:
                self.summary_stats['invalid'] += 1
            
            if not test_result['best_result']['validation']['in_expected_district']:
                self.summary_stats['wrong_district'] += 1
            
            if not test_result['best_result']['validation']['in_kerala']:
                self.summary_stats['outside_kerala'] += 1
    
    def run_test_batch(self, json_file_path: str) -> Dict:
        """Run test on all samples in JSON file"""
        
        print(f"🚀 STARTING GEOCODING TEST BATCH")
        print(f"📁 File: {json_file_path}")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Load sample data
        sample_data = self.load_sample_data(json_file_path)
        
        # Test each campus
        for i, campus in enumerate(sample_data, 1):
            print(f"\n🔢 TESTING {i}/{len(sample_data)}")
            self.test_campus(campus)
        
        # Generate final summary
        self.generate_final_summary()
        
        # Save results
        self.save_test_results(json_file_path)
        
        return {
            'summary_stats': self.summary_stats,
            'test_results': self.test_results
        }
    
    def generate_final_summary(self):
        """Generate final test summary"""
        stats = self.summary_stats
        total = stats['total_tested']
        
        print(f"\n" + "="*80)
        print(f"📊 FINAL TEST SUMMARY")
        print(f"="*80)
        print(f"Total Campuses Tested: {total}")
        print(f"Successful Results: {stats['successful']} ({stats['successful']/total*100:.1f}%)")
        print(f"")
        print(f"CONFIDENCE BREAKDOWN:")
        print(f"  🟢 High Confidence: {stats['high_confidence']} ({stats['high_confidence']/total*100:.1f}%)")
        print(f"  🟡 Medium Confidence: {stats['medium_confidence']} ({stats['medium_confidence']/total*100:.1f}%)")
        print(f"  🟠 Low Confidence: {stats['low_confidence']} ({stats['low_confidence']/total*100:.1f}%)")
        print(f"  🔴 Invalid: {stats['invalid']} ({stats['invalid']/total*100:.1f}%)")
        print(f"")
        print(f"ISSUES:")
        print(f"  Wrong District: {stats['wrong_district']}")
        print(f"  Outside Kerala: {stats['outside_kerala']}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        high_success_rate = stats['high_confidence'] / total > 0.8
        medium_issues = stats['wrong_district'] / total > 0.2
        outside_issues = stats['outside_kerala'] > 0
        
        if high_success_rate:
            print(f"  ✅ Good overall success rate! Current approach is working well.")
        else:
            print(f"  🔧 Consider implementing multiple search strategies in production.")
        
        if medium_issues:
            print(f"  🎯 High rate of wrong district results - implement district validation.")
        
        if outside_issues:
            print(f"  🚨 Some coordinates outside Kerala - review address cleaning process.")
        
        if stats['invalid'] > stats['total_tested'] * 0.1:
            print(f"  📝 High failure rate - review address data quality.")
    
    def save_test_results(self, original_file_path: str):
        """Save detailed test results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = Path(original_file_path).stem
        results_file = f"test_results_{base_name}_{timestamp}.json"
        
        output_data = {
            'test_metadata': {
                'original_file': original_file_path,
                'test_timestamp': datetime.now().isoformat(),
                'total_tested': self.summary_stats['total_tested']
            },
            'summary_stats': self.summary_stats,
            'detailed_results': self.test_results
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detailed results saved to: {results_file}")


def main():
    """Main function to run the test"""
    
    print("🧪 KERALA CAMPUS GEOCODING TEST RUNNER")
    print("="*50)
    
    # Get API key
    api_key = input("Enter your Google Maps API key: ").strip()
    if not api_key:
        print("❌ API key is required!")
        return
    
    # Get JSON file path
    json_file = input("Enter path to your sample JSON file: ").strip()
    if not json_file:
        print("❌ JSON file path is required!")
        return
    
    if not os.path.exists(json_file):
        print(f"❌ File not found: {json_file}")
        return
    
    # Create test runner
    test_runner = JSONTestRunner(api_key=api_key, debug_mode=True)
    
    # Run tests
    try:
        results = test_runner.run_test_batch(json_file)
        print(f"\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")


if __name__ == "__main__":
    main()


# Example usage for direct execution:

# Initialize geocoder
geocoder = CampusGeocoder(
    api_key="AIzaSyD4l6B4c6O7_AY26Qem7oqAzZbWs8D2Lpc",
    batch_size=25,
    request_delay=0.15
)

# Load and process data
campus_data = geocoder.load_campus_data("db latest data .json")
results = geocoder.process_all_campuses(campus_data)

# Export results
geocoder.export_results(results, "output_with_coordinates.json")
