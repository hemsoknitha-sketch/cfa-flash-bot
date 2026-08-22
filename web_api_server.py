"""
Khmer National News API & Telemetry Web Server V1.0
Lightweight async HTTP API exposing Khmer national news, defense archives, and hardware telemetry.
Runs on port 8080.
"""

import os
import json
import logging
from aiohttp import web
from national_ingestion_registry import get_all_national_feeds
from defense_intelligence_engine import defense_engine

logger = logging.getLogger(__name__)

async def handle_latest_news(request):
    """GET /api/v1/latest_news"""
    try:
        from vector_store import news_dedup_store
        data = {
            "status": "success",
            "total_cached": len(news_dedup_store.seen_hashes),
            "national_desks_count": len(get_all_national_feeds()),
            "message": "CFA Flash Feed Premier National News API"
        }
        return web.json_response(data)
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

async def handle_defense_archives(request):
    """GET /api/v1/defense_archives"""
    try:
        archives = defense_engine.get_border_archives(limit=20)
        return web.json_response({"status": "success", "count": len(archives), "data": archives})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

async def handle_telemetry(request):
    """GET /api/v1/telemetry"""
    try:
        import psutil
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        data = {
            "status": "active",
            "server": "Google Cloud VM (Linux Cloud x86_64)",
            "ram_used_mb": round(ram.used / (1024 * 1024), 1),
            "ram_total_mb": round(ram.total / (1024 * 1024), 1),
            "ram_percent": ram.percent,
            "disk_used_gb": round(disk.used / (1024 * 1024 * 1024), 1),
            "disk_total_gb": round(disk.total / (1024 * 1024 * 1024), 1),
            "disk_percent": disk.percent,
            "cost_per_month": "$0.00 / 100% Free Forever"
        }
        return web.json_response(data)
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

def create_app():
    app = web.Application()
    app.router.add_get('/api/v1/latest_news', handle_latest_news)
    app.router.add_get('/api/v1/defense_archives', handle_defense_archives)
    app.router.add_get('/api/v1/telemetry', handle_telemetry)
    return app

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = create_app()
    web.run_app(app, host='0.0.0.0', port=8080)
