"""
Khmer National News API & Telemetry Web Server V8.0 GOLD STANDARD
Lightweight async HTTP API exposing Khmer national news, defense archives, legal vault, and hardware telemetry.
Serves static Web Mini App directly at root (/) and /mini_app with full CORS support.
Runs on port 8080.
"""

import os
import json
import logging
from aiohttp import web
from national_ingestion_registry import get_all_national_feeds
from defense_intelligence_engine import defense_engine
from khmer_legal_engine import KhmerLegalEngine
from news_credibility_engine import NewsCredibilityEngine

logger = logging.getLogger(__name__)

legal_engine = KhmerLegalEngine()
credibility_engine = NewsCredibilityEngine()

# Middleware for Cross-Origin Resource Sharing (CORS)
@web.middleware
async def cors_middleware(request, handler):
    if request.method == "OPTIONS":
        response = web.Response(status=200)
    else:
        try:
            response = await handler(request)
        except Exception as ex:
            response = web.json_response({"status": "error", "message": str(ex)}, status=500)

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    return response

async def handle_latest_news(request):
    """GET /api/v1/latest_news - Summary metadata"""
    try:
        from vector_store import VectorDeduplicator
        dedup = VectorDeduplicator()
        data = {
            "status": "success",
            "total_cached": len(dedup.seen_hashes),
            "national_desks_count": len(get_all_national_feeds()),
            "message": "CFA Flash Feed Premier National News API"
        }
        return web.json_response(data)
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

async def handle_news_feed(request):
    """GET /api/v1/news_feed?limit=20 - List of latest published articles"""
    try:
        limit = int(request.query.get("limit", 20))
        archives = defense_engine.get_border_archives(limit=limit)
        return web.json_response({"status": "success", "count": len(archives), "data": archives})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

async def handle_defense_archives(request):
    """GET /api/v1/defense_archives"""
    try:
        archives = defense_engine.get_border_archives(limit=30)
        return web.json_response({"status": "success", "count": len(archives), "data": archives})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

async def handle_laws_search(request):
    """GET /api/v1/laws?q=... - Search 249+ Cambodian national laws"""
    try:
        query = request.query.get("q", "").strip()
        limit = int(request.query.get("limit", 10))
        if not query:
            results = legal_engine.laws[:limit]
        else:
            results = legal_engine.search_relevant_laws(query, limit=limit)
        return web.json_response({
            "status": "success",
            "query": query,
            "count": len(results),
            "total_vault": len(legal_engine.laws),
            "data": results
        })
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

async def handle_fact_check(request):
    """POST /api/v1/fact_check - Calculates Credibility Score & AI Audit"""
    try:
        body = await request.json()
        title = body.get("title", "")
        content = body.get("content", body.get("text", ""))
        source = body.get("source", "សារព័ត៌មានឌីជីថល")

        result = credibility_engine.evaluate_credibility(title=title, content=content, source_name=source)
        return web.json_response({"status": "success", "data": result})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

async def handle_feeds(request):
    """GET /api/v1/feeds - 37 National Ministries & Provincial Desks"""
    try:
        feeds = get_all_national_feeds()
        return web.json_response({"status": "success", "count": len(feeds), "data": feeds})
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

async def handle_telemetry(request):
    """GET /api/v1/telemetry - Live System & Server Telemetry"""
    try:
        import psutil
        import platform
        import time

        ram = psutil.virtual_memory()
        disk_path = '/' if os.name != 'nt' else 'C:\\'
        disk = psutil.disk_usage(disk_path)
        cpu_pct = psutil.cpu_percent(interval=0.1)

        data = {
            "status": "active",
            "os_name": f"{platform.system()} {platform.release()}",
            "hostname": platform.node(),
            "cpu_percent": cpu_pct,
            "ram_used_mb": round(ram.used / (1024 * 1024), 1),
            "ram_total_mb": round(ram.total / (1024 * 1024), 1),
            "ram_percent": ram.percent,
            "disk_used_gb": round(disk.used / (1024 * 1024 * 1024), 1),
            "disk_total_gb": round(disk.total / (1024 * 1024 * 1024), 1),
            "disk_percent": disk.percent,
            "cost_per_month": "$0.00 / 100% Free Forever 24/7 365",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return web.json_response(data)
    except Exception as e:
        return web.json_response({"status": "error", "message": str(e)}, status=500)

def create_app():
    app = web.Application(middlewares=[cors_middleware])
    
    # API Routes
    app.router.add_get('/api/v1/latest_news', handle_latest_news)
    app.router.add_get('/api/v1/news_feed', handle_news_feed)
    app.router.add_get('/api/v1/defense_archives', handle_defense_archives)
    app.router.add_get('/api/v1/laws', handle_laws_search)
    app.router.add_post('/api/v1/fact_check', handle_fact_check)
    app.router.add_get('/api/v1/feeds', handle_feeds)
    app.router.add_get('/api/v1/telemetry', handle_telemetry)

    # Static Web Mini App Root Route
    mini_app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mini_app")
    if os.path.exists(mini_app_dir):
        app.router.add_static('/static', mini_app_dir, name='static', show_index=True)

        async def index_handler(request):
            index_path = os.path.join(mini_app_dir, "index.html")
            if os.path.exists(index_path):
                return web.FileResponse(index_path)
            return web.Response(text="CFA Flash Feed Web Mini App - Ready", content_type="text/plain")

        app.router.add_get('/', index_handler)
        app.router.add_get('/mini_app', index_handler)

    return app

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = create_app()
    logger.info("⚡ [CFA WEB API & MINI APP SERVER READY] Running on http://localhost:8080")
    web.run_app(app, host='0.0.0.0', port=8080)
