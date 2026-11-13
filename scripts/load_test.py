#!/usr/bin/env python3
"""
BBMS Concurrency Load Test Runner

# BBMS-NF-004 (TC-Perf-02): Support 200 concurrent users.
Standard library only (threading, urllib.request, time).
"""

import sys
import time
import json
import threading
import urllib.request
import urllib.error

DEFAULT_URL = 'http://127.0.0.1:8000/api/health'
NUM_CONCURRENT_USERS = 200
REQUESTS_PER_USER = 2


def worker(target_url, results, thread_id):
    thread_latencies = []
    successes = 0
    failures = 0

    for _ in range(REQUESTS_PER_USER):
        start = time.perf_counter()
        try:
            req = urllib.request.Request(target_url, headers={'User-Agent': f'BBMS-LoadTester-Thread/{thread_id}'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                status_code = resp.status
                if status_code in (200, 201):
                    successes += 1
                else:
                    failures += 1
        except Exception as e:
            failures += 1
        finally:
            elapsed = time.perf_counter() - start
            thread_latencies.append(elapsed)

    results.append({
        'thread_id': thread_id,
        'latencies': thread_latencies,
        'successes': successes,
        'failures': failures,
    })


def run_load_test(target_url=DEFAULT_URL, concurrency=NUM_CONCURRENT_USERS):
    print(f"================================================================")
    print(f"BBMS Concurrency Benchmark (BBMS-NF-004)")
    print(f"Target:      {target_url}")
    print(f"Concurrency: {concurrency} threads")
    print(f"Requests/user: {REQUESTS_PER_USER} (Total expected: {concurrency * REQUESTS_PER_USER})")
    print(f"================================================================")

    threads = []
    results = []

    overall_start = time.perf_counter()

    for i in range(concurrency):
        t = threading.Thread(target=worker, args=(target_url, results, i + 1))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    total_time = time.perf_counter() - overall_start

    all_latencies = []
    total_successes = 0
    total_failures = 0

    for r in results:
        all_latencies.extend(r['latencies'])
        total_successes += r['successes']
        total_failures += r['failures']

    all_latencies.sort()
    total_requests = len(all_latencies)
    avg_latency = sum(all_latencies) / total_requests if total_requests else 0
    min_latency = all_latencies[0] if all_latencies else 0
    max_latency = all_latencies[-1] if all_latencies else 0
    p50_latency = all_latencies[int(total_requests * 0.50)] if total_requests else 0
    p95_latency = all_latencies[int(total_requests * 0.95)] if total_requests else 0
    p99_latency = all_latencies[int(total_requests * 0.99)] if total_requests else 0
    throughput = total_requests / total_time if total_time else 0

    print("\nBENCHMARK RESULTS:")
    print(f"  Total Duration:     {total_time:.3f} s")
    print(f"  Completed Requests: {total_requests}")
    print(f"  Successful (2xx):   {total_successes}")
    print(f"  Failed:             {total_failures}")
    print(f"  Throughput:         {throughput:.2f} req/s")
    print(f"  Latency Min:        {min_latency * 1000:.1f} ms")
    print(f"  Latency Mean:       {avg_latency * 1000:.1f} ms")
    print(f"  Latency Median:     {p50_latency * 1000:.1f} ms")
    print(f"  Latency 95th %ile:  {p95_latency * 1000:.1f} ms")
    print(f"  Latency 99th %ile:  {p99_latency * 1000:.1f} ms")
    print(f"================================================================")

    return {
        'concurrency': concurrency,
        'total_requests': total_requests,
        'total_successes': total_successes,
        'total_failures': total_failures,
        'total_time_seconds': total_time,
        'throughput_rps': throughput,
        'avg_ms': avg_latency * 1000,
        'p95_ms': p95_latency * 1000,
    }


if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    run_load_test(url)
