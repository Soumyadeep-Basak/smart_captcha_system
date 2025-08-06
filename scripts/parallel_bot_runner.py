#!/usr/bin/env python3
"""
Parallel Bot Test Runner
- Runs multiple optimized bots in sequence with timing analysis
- Tests selective honeypot triggering across different bot types
- Enhanced result display and performance metrics
"""

import time
import subprocess
import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests

class ParallelBotRunner:
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
        
    def check_prerequisites(self):
        """Check if backend and frontend are running"""
        print("🧪 Checking prerequisites...")
        
        # Check backend
        try:
            response = requests.get("http://127.0.0.1:5000/health", timeout=5)
            backend_ok = response.status_code == 200
            print(f"   🔧 Backend: {'✅ RUNNING' if backend_ok else '❌ NOT RUNNING'}")
        except:
            backend_ok = False
            print(f"   🔧 Backend: ❌ NOT ACCESSIBLE")
        
        # Check frontend
        try:
            response = requests.get("http://localhost:3000/register", timeout=5)
            frontend_ok = response.status_code == 200
            print(f"   🌐 Frontend: {'✅ RUNNING' if frontend_ok else '❌ NOT RUNNING'}")
        except:
            frontend_ok = False
            print(f"   🌐 Frontend: ❌ NOT ACCESSIBLE")
        
        return backend_ok and frontend_ok
    
    def run_bot_script(self, script_path, bot_name, timeout=60):
        """Run a single bot script and capture results"""
        print(f"\n🤖 Running {bot_name}...")
        print("-" * 40)
        
        start_time = time.time()
        
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd="d:\\hack\\botv1"
            )
            
            duration = time.time() - start_time
            
            if result.returncode == 0:
                # Parse output for key metrics
                output = result.stdout
                
                # Extract honeypot information
                honeypot_triggered = "honeypot" in output.lower() and ("triggered" in output.lower() or "yes" in output.lower())
                
                # Extract duration if available
                if "Duration:" in output:
                    try:
                        duration_line = [line for line in output.split('\n') if 'Duration:' in line][0]
                        extracted_duration = float(duration_line.split('Duration:')[1].split('s')[0].strip())
                        duration = extracted_duration
                    except:
                        pass
                
                # Determine success indicators
                success_indicators = [
                    "completed successfully" in output.lower(),
                    "form submitted" in output.lower(),
                    "✅" in output
                ]
                
                success = any(success_indicators)
                
                self.test_results[bot_name] = {
                    "status": "SUCCESS" if success else "COMPLETED_WITH_ISSUES",
                    "duration": duration,
                    "honeypot_triggered": honeypot_triggered,
                    "output_length": len(output),
                    "error_count": output.lower().count("❌"),
                    "success_count": output.count("✅")
                }
                
                print(f"✅ {bot_name} completed in {duration:.1f}s")
                if honeypot_triggered:
                    print(f"   🍯 Honeypot triggered")
                    
            else:
                duration = time.time() - start_time
                self.test_results[bot_name] = {
                    "status": "FAILED",
                    "duration": duration,
                    "honeypot_triggered": False,
                    "error": result.stderr[:200] if result.stderr else "Unknown error"
                }
                print(f"❌ {bot_name} failed in {duration:.1f}s")
                
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            self.test_results[bot_name] = {
                "status": "TIMEOUT",
                "duration": duration,
                "honeypot_triggered": False,
                "error": f"Timeout after {timeout}s"
            }
            print(f"⏰ {bot_name} timed out after {duration:.1f}s")
            
        except Exception as e:
            duration = time.time() - start_time
            self.test_results[bot_name] = {
                "status": "ERROR",
                "duration": duration,
                "honeypot_triggered": False,
                "error": str(e)
            }
            print(f"❌ {bot_name} error: {e}")
    
    async def run_parallel_tests(self):
        """Run multiple bot tests in controlled sequence"""
        print("🚀 Parallel Bot Test Runner")
        print("=" * 60)
        
        # Check prerequisites
        if not self.check_prerequisites():
            print("\n❌ Prerequisites not met. Please start backend and frontend first.")
            return
        
        print("\n✅ Prerequisites met. Starting bot tests...")
        
        # Test configurations
        bot_tests = [
            # Scripts folder optimized bots
            ("scripts/form_bot_optimized_v3.py", "Optimized Form Bot v3 (Async)"),
            ("scripts/form_bot_improved_v2_fixed.py", "Fixed Form Bot v2"),
            
            # Bot attacks folder optimized bots
            ("bot_attacks/basic/basic_bot_optimized.py", "Basic Optimized Bot"),
            ("bot_attacks/advanced/form_bot_optimized.py", "Advanced Form Bot"),
            ("bot_attacks/advanced/form_bot_improved_optimized.py", "Improved Optimized Bot"),
            ("bot_attacks/advanced/form_bot_improved_v2_optimized.py", "Enhanced v2 Optimized Bot"),
        ]
        
        print(f"\n📋 Running {len(bot_tests)} optimized bot tests...")
        
        # Run tests in sequence with brief delays
        for script_path, bot_name in bot_tests:
            self.run_bot_script(script_path, bot_name, timeout=90)
            
            # Brief pause between tests to avoid conflicts
            time.sleep(2)
        
        # Display comprehensive results
        self.display_comprehensive_results()
    
    def display_comprehensive_results(self):
        """Display enhanced results analysis"""
        total_duration = time.time() - self.start_time
        
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE BOT TEST RESULTS")
        print("=" * 80)
        
        # Summary statistics
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results.values() if result["status"] in ["SUCCESS", "COMPLETED_WITH_ISSUES"])
        honeypot_triggered_count = sum(1 for result in self.test_results.values() if result.get("honeypot_triggered", False))
        
        print(f"\n📈 SUMMARY STATISTICS:")
        print(f"   🧪 Total Tests: {total_tests}")
        print(f"   ✅ Successful: {successful_tests}")
        print(f"   ❌ Failed: {total_tests - successful_tests}")
        print(f"   🍯 Honeypots Triggered: {honeypot_triggered_count}")
        print(f"   ⏱️ Total Duration: {total_duration:.1f}s")
        print(f"   📊 Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        print(f"   🎯 Honeypot Rate: {(honeypot_triggered_count/total_tests)*100:.1f}%")
        
        # Detailed results
        print(f"\n📋 DETAILED RESULTS:")
        for bot_name, result in self.test_results.items():
            status_icon = {
                "SUCCESS": "✅",
                "COMPLETED_WITH_ISSUES": "⚠️",
                "FAILED": "❌",
                "TIMEOUT": "⏰",
                "ERROR": "💥"
            }.get(result["status"], "❓")
            
            honeypot_icon = "🍯" if result.get("honeypot_triggered", False) else "⭕"
            
            print(f"   {status_icon} {bot_name}")
            print(f"      ⏱️ Duration: {result['duration']:.1f}s")
            print(f"      {honeypot_icon} Honeypot: {'YES' if result.get('honeypot_triggered', False) else 'NO'}")
            print(f"      📊 Status: {result['status']}")
            
            if result["status"] in ["FAILED", "ERROR", "TIMEOUT"] and "error" in result:
                print(f"      ❌ Error: {result['error'][:100]}...")
        
        # Performance analysis
        durations = [result['duration'] for result in self.test_results.values() if result['status'] != 'ERROR']
        if durations:
            avg_duration = sum(durations) / len(durations)
            min_duration = min(durations)
            max_duration = max(durations)
            
            print(f"\n⚡ PERFORMANCE ANALYSIS:")
            print(f"   📊 Average Duration: {avg_duration:.1f}s")
            print(f"   🚀 Fastest Bot: {min_duration:.1f}s")
            print(f"   🐌 Slowest Bot: {max_duration:.1f}s")
            print(f"   📈 Speed Improvement: {((max_duration - avg_duration) / max_duration * 100):.1f}% over slowest")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if honeypot_triggered_count > 0:
            print(f"   🎯 SUCCESS: {honeypot_triggered_count} bots triggered honeypots - detection system working!")
        else:
            print(f"   ⚠️ No honeypots triggered - check honeypot implementation")
            
        if successful_tests == total_tests:
            print(f"   ✅ All bots completed successfully - optimization working well!")
        elif successful_tests > total_tests * 0.8:
            print(f"   ⚠️ Most bots successful - minor issues to address")
        else:
            print(f"   ❌ Multiple failures detected - need investigation")
        
        fastest_bots = [name for name, result in self.test_results.items() 
                       if result.get('duration', float('inf')) < avg_duration if durations]
        
        if fastest_bots:
            print(f"   🚀 Fastest performing bots: {', '.join(fastest_bots[:3])}")
        
        print("=" * 80)

async def main():
    """Main async runner"""
    runner = ParallelBotRunner()
    await runner.run_parallel_tests()

if __name__ == "__main__":
    asyncio.run(main())
