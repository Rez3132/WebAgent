from flask import Flask, render_template, request, jsonify, session
import requests
import urllib.parse
import json
import logging
from datetime import datetime
import os
from typing import List, Dict, Optional
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-change-this')

class APIConfig:
    """Configuration class for different adult video APIs"""
    
    EPORNER_BASE_URL = "https://www.eporner.com/api/v2/video/search/"
    REDGIFS_BASE_URL = "https://api.redgifs.com/v2/search"
    
    # Rate limiting settings
    RATE_LIMIT_DELAY = 1  # seconds between requests
    MAX_RETRIES = 3
    TIMEOUT = 10

class EpornerAPI:
    """Eporner API integration"""
    
    @staticmethod
    def fetch_videos(query: str = "footjob+wife", category: Optional[str] = None, 
                    limit: int = 10, page: int = 1) -> List[Dict]:
        """
        Fetch videos from Eporner API
        
        Args:
            query: Search keywords
            category: Category filter
            limit: Number of videos to retrieve
            page: Page number for pagination
            
        Returns:
            List of video metadata dictionaries
        """
        params = {
            "per_page": min(limit, 50),  # Eporner max is 50
            "page": page,
            "thumbsize": "big",
            "order": "latest",
            "format": "json"
        }
        
        if query:
            params["query"] = query
        if category:
            params["category"] = category
        
        try:
            time.sleep(APIConfig.RATE_LIMIT_DELAY)
            response = requests.get(
                APIConfig.EPORNER_BASE_URL, 
                params=params, 
                timeout=APIConfig.TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            
            videos = data.get("videos", [])
            return [
                {
                    "source": "Eporner",
                    "title": video.get("title", "No title"),
                    "url": video.get("url", ""),
                    "thumbnail": video.get("default_thumb", {}).get("src", ""),
                    "duration": video.get("length_min", "N/A"),
                    "views": video.get("views", 0),
                    "rating": video.get("rate", 0),
                    "keywords": video.get("keywords", ""),
                    "added": video.get("added", ""),
                    "embed": video.get("embed", "")
                }
                for video in videos
            ]
        except requests.exceptions.RequestException as e:
            logger.error(f"Eporner API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in Eporner API: {e}")
            return []

class RedGifsAPI:
    """RedGifs API integration"""
    
    @staticmethod
    def get_auth_token() -> Optional[str]:
        """Get temporary auth token for RedGifs API"""
        try:
            response = requests.get("https://api.redgifs.com/v2/auth/temporary")
            if response.status_code == 200:
                return response.json().get("token")
        except Exception as e:
            logger.error(f"RedGifs auth error: {e}")
        return None
    
    @staticmethod
    def fetch_videos(query: str = "footjob wife", limit: int = 10, page: int = 1) -> List[Dict]:
        """
        Fetch videos from RedGifs API
        
        Args:
            query: Search keywords
            limit: Number of videos to retrieve
            page: Page number for pagination
            
        Returns:
            List of video metadata dictionaries
        """
        token = RedGifsAPI.get_auth_token()
        if not token:
            logger.error("Failed to get RedGifs auth token")
            return []
        
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "search_text": query,
            "order": "new",
            "count": min(limit, 80),  # RedGifs max per request
            "page": page - 1  # RedGifs uses 0-based pagination
        }
        
        try:
            time.sleep(APIConfig.RATE_LIMIT_DELAY)
            response = requests.get(
                APIConfig.REDGIFS_BASE_URL,
                headers=headers,
                params=params,
                timeout=APIConfig.TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            
            gifs = data.get("gifs", [])
            return [
                {
                    "source": "RedGifs",
                    "title": gif.get("tags", ["No title"])[0] if gif.get("tags") else "No title",
                    "url": f"https://redgifs.com/watch/{gif.get('id', '')}",
                    "thumbnail": gif.get("urls", {}).get("poster", ""),
                    "duration": f"{gif.get('duration', 0):.1f}s",
                    "views": gif.get("views", 0),
                    "rating": gif.get("likes", 0),
                    "keywords": ", ".join(gif.get("tags", [])),
                    "added": gif.get("createDate", ""),
                    "embed": gif.get("urls", {}).get("sd", "")
                }
                for gif in gifs
            ]
        except requests.exceptions.RequestException as e:
            logger.error(f"RedGifs API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in RedGifs API: {e}")
            return []

class PornHubStyleAPI:
    """Generic implementation for PornHub-style APIs (educational purposes)"""
    
    @staticmethod
    def fetch_videos(query: str = "footjob wife", limit: int = 10) -> List[Dict]:
        """
        Placeholder for PornHub-style API integration
        Note: This would require unofficial APIs or scraping which may violate ToS
        """
        logger.warning("PornHub-style API not implemented - would require unofficial methods")
        return [
            {
                "source": "PornHub-Style (Demo)",
                "title": f"Demo: {query} video {i+1}",
                "url": "#",
                "thumbnail": "https://via.placeholder.com/320x180?text=Demo+Video",
                "duration": f"{3+i}:{'%02d' % (15+i*7)}",
                "views": 1000 * (i + 1),
                "rating": 4.0 + (i * 0.1),
                "keywords": query.replace("+", ", "),
                "added": "2024-01-01",
                "embed": ""
            }
            for i in range(min(limit, 5))
        ]

class VideoSearcher:
    """Main video search orchestrator"""
    
    @staticmethod
    def search_all_apis(query: str = "footjob+wife", category: Optional[str] = None, 
                       limit_per_api: int = 10, apis: List[str] = None) -> Dict[str, List[Dict]]:
        """
        Search across multiple APIs
        
        Args:
            query: Search keywords
            category: Category filter (where supported)
            limit_per_api: Number of videos per API
            apis: List of APIs to search (default: all available)
            
        Returns:
            Dictionary with API names as keys and video lists as values
        """
        if apis is None:
            apis = ["eporner", "redgifs"]  # Exclude demo API by default
        
        results = {}
        
        if "eporner" in apis:
            logger.info(f"Searching Eporner for: {query}")
            results["eporner"] = EpornerAPI.fetch_videos(query, category, limit_per_api)
        
        if "redgifs" in apis:
            logger.info(f"Searching RedGifs for: {query}")
            # Convert query format for RedGifs
            redgifs_query = query.replace("+", " ")
            results["redgifs"] = RedGifsAPI.fetch_videos(redgifs_query, limit_per_api)
        
        if "pornhub_demo" in apis:
            logger.info(f"Using PornHub demo for: {query}")
            pornhub_query = query.replace("+", " ")
            results["pornhub_demo"] = PornHubStyleAPI.fetch_videos(pornhub_query, limit_per_api)
        
        return results
    
    @staticmethod
    def combine_and_sort_results(api_results: Dict[str, List[Dict]], 
                               sort_by: str = "views") -> List[Dict]:
        """
        Combine results from multiple APIs and sort them
        
        Args:
            api_results: Dictionary with API results
            sort_by: Sort field (views, rating, title, added)
            
        Returns:
            Combined and sorted list of videos
        """
        all_videos = []
        for api_name, videos in api_results.items():
            all_videos.extend(videos)
        
        # Sort by specified field
        if sort_by == "views":
            all_videos.sort(key=lambda x: x.get("views", 0), reverse=True)
        elif sort_by == "rating":
            all_videos.sort(key=lambda x: x.get("rating", 0), reverse=True)
        elif sort_by == "title":
            all_videos.sort(key=lambda x: x.get("title", "").lower())
        elif sort_by == "added":
            all_videos.sort(key=lambda x: x.get("added", ""), reverse=True)
        
        return all_videos

@app.route("/", methods=["GET", "POST"])
def index():
    """Main route for video search interface"""
    videos = []
    api_results = {}
    query = "footjob+wife"  # Default query
    category = None
    selected_apis = ["eporner", "redgifs"]
    sort_by = "views"
    
    if request.method == "POST":
        query = request.form.get("query") or "footjob+wife"
        category = request.form.get("category") or None
        selected_apis = request.form.getlist("apis") or ["eporner"]
        sort_by = request.form.get("sort_by") or "views"
        
        # Search APIs
        api_results = VideoSearcher.search_all_apis(
            query=query, 
            category=category, 
            limit_per_api=10,
            apis=selected_apis
        )
        
        # Combine and sort results
        videos = VideoSearcher.combine_and_sort_results(api_results, sort_by)
    else:
        # Initial load with default search
        api_results = VideoSearcher.search_all_apis(query=query, apis=selected_apis)
        videos = VideoSearcher.combine_and_sort_results(api_results, sort_by)
    
    # Store search stats
    total_results = len(videos)
    api_stats = {api: len(results) for api, results in api_results.items()}
    
    return render_template(
        "index.html", 
        videos=videos, 
        query=query, 
        category=category,
        selected_apis=selected_apis,
        sort_by=sort_by,
        total_results=total_results,
        api_stats=api_stats
    )

@app.route("/api/search", methods=["POST"])
def api_search():
    """JSON API endpoint for programmatic searches"""
    data = request.get_json()
    
    query = data.get("query", "footjob+wife")
    category = data.get("category")
    apis = data.get("apis", ["eporner", "redgifs"])
    limit_per_api = data.get("limit_per_api", 10)
    sort_by = data.get("sort_by", "views")
    
    try:
        api_results = VideoSearcher.search_all_apis(
            query=query,
            category=category,
            limit_per_api=limit_per_api,
            apis=apis
        )
        
        videos = VideoSearcher.combine_and_sort_results(api_results, sort_by)
        
        return jsonify({
            "success": True,
            "query": query,
            "total_results": len(videos),
            "api_stats": {api: len(results) for api, results in api_results.items()},
            "videos": videos
        })
    
    except Exception as e:
        logger.error(f"API search error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "available_apis": ["eporner", "redgifs", "pornhub_demo"]
    })

if __name__ == "__main__":
    # Ensure templates directory exists
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static/css", exist_ok=True)
    os.makedirs("static/js", exist_ok=True)
    
    # Run the app
    app.run(debug=True, host="0.0.0.0", port=5000)