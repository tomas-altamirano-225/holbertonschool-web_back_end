#!/usr/bin/env python3
""" Log stats with Top 10 IPs """
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    # 1. Total Logs
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    # 2. Methods
    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # 3. Status Check
    status_check = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{status_check} status check")

    # 4. Top 10 IPs (Aggregation)
    print("IPs:")
    top_ips = nginx_collection.aggregate([
        { "$group": { "_id": "$ip", "count": { "$sum": 1 } } },
        { "$sort": { "count": -1 } },
        { "$limit": 10 }
    ])

    for ip_data in top_ips:
        print(f"\t{ip_data.get('_id')}: {ip_data.get('count')}")
