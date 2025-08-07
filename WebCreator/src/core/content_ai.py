"""
WebCreator AI Content Generation Engine
Handles AI-powered analysis and content generation for websites.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
import re

# Try to import OpenAI, fallback to mock if not available
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI library not available. Using mock responses.")

logger = logging.getLogger(__name__)


class ContentAI:
    """AI-powered content generation and analysis for websites."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the ContentAI engine.
        
        Args:
            api_key: OpenAI API key (optional, will use mock if not provided)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.use_ai = OPENAI_AVAILABLE and bool(self.api_key)
        
        if self.use_ai:
            openai.api_key = self.api_key
            logger.info("ContentAI initialized with OpenAI integration")
        else:
            logger.info("ContentAI initialized with mock responses")
    
    def analyze_description(self, description: str) -> Dict[str, Any]:
        """
        Analyze a website description to extract structure and requirements.
        
        Args:
            description: Natural language description of the website
            
        Returns:
            Analysis dictionary with sections, features, and metadata
        """
        if self.use_ai:
            return self._ai_analyze_description(description)
        else:
            return self._mock_analyze_description(description)
    
    def generate_content(self, request, website_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate content for the website based on the request and plan.
        
        Args:
            request: WebsiteRequest object
            website_plan: Analyzed website plan
            
        Returns:
            Generated content dictionary
        """
        if self.use_ai:
            return self._ai_generate_content(request, website_plan)
        else:
            return self._mock_generate_content(request, website_plan)
    
    def _ai_analyze_description(self, description: str) -> Dict[str, Any]:
        """Use OpenAI to analyze the website description."""
        prompt = f"""
        Analyze this website description and extract the following information:
        
        Description: "{description}"
        
        Please respond with a JSON object containing:
        - sections: Array of section names (like "hero", "about", "services", "contact", etc.)
        - features: Array of needed features (like "contact_form", "image_gallery", "testimonials", etc.)
        - keywords: Array of relevant keywords that help determine website type
        - navigation: Object with main navigation items
        - pages: Array of page names needed
        - components: Array of UI components needed
        - content_blocks: Array of content blocks with their types and purposes
        
        Make the analysis comprehensive and practical for website generation.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a web design expert who analyzes website requirements and returns structured JSON responses."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            # Extract JSON from the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                logger.warning("Could not extract JSON from AI response, using fallback")
                return self._mock_analyze_description(description)
                
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            return self._mock_analyze_description(description)
    
    def _mock_analyze_description(self, description: str) -> Dict[str, Any]:
        """Mock analysis for when AI is not available."""
        description_lower = description.lower()
        
        # Determine sections based on keywords
        sections = ["hero"]
        
        if any(word in description_lower for word in ["about", "story", "company", "team"]):
            sections.append("about")
        
        if any(word in description_lower for word in ["service", "product", "offer", "feature"]):
            sections.append("services")
        
        if any(word in description_lower for word in ["portfolio", "gallery", "work", "project"]):
            sections.append("portfolio")
        
        if any(word in description_lower for word in ["testimonial", "review", "client"]):
            sections.append("testimonials")
        
        if any(word in description_lower for word in ["contact", "reach", "email", "phone"]):
            sections.append("contact")
        
        # Determine features
        features = []
        
        if "contact" in sections or any(word in description_lower for word in ["form", "contact", "email"]):
            features.append("contact_form")
        
        if any(word in description_lower for word in ["gallery", "image", "photo", "picture"]):
            features.append("image_gallery")
        
        if any(word in description_lower for word in ["animation", "smooth", "interactive"]):
            features.append("animations")
        
        # Extract keywords for type determination
        keywords = []
        if any(word in description_lower for word in ["portfolio", "artist", "designer", "photographer"]):
            keywords.extend(["portfolio", "showcase"])
        
        if any(word in description_lower for word in ["business", "company", "corporate", "service"]):
            keywords.extend(["business", "corporate"])
        
        if any(word in description_lower for word in ["blog", "news", "article", "content"]):
            keywords.extend(["blog", "content"])
        
        if any(word in description_lower for word in ["shop", "store", "product", "buy", "sell"]):
            keywords.extend(["ecommerce", "shop"])
        
        if any(word in description_lower for word in ["landing", "product", "launch", "marketing"]):
            keywords.extend(["landing", "marketing"])
        
        return {
            "sections": sections,
            "features": features,
            "keywords": keywords,
            "navigation": {
                "main": [section.capitalize() for section in sections if section != "hero"],
                "brand": "Brand Name"
            },
            "pages": ["home"],
            "components": ["header", "footer", "navigation"] + features,
            "content_blocks": [
                {"type": "hero", "purpose": "Main banner with key message"},
                {"type": "content", "purpose": "Main content sections"},
                {"type": "cta", "purpose": "Call-to-action elements"}
            ]
        }
    
    def _ai_generate_content(self, request, website_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Use OpenAI to generate website content."""
        prompt = f"""
        Generate content for a website with the following specifications:
        
        Description: "{request.description}"
        Website Type: {website_plan.get('website_type', 'general')}
        Sections: {website_plan.get('sections', [])}
        Theme: {request.theme}
        Tone: {request.content_tone}
        Target Audience: {request.target_audience}
        
        Please generate a JSON object with:
        - title: Main website title
        - description: Meta description for SEO
        - keywords: Array of SEO keywords
        - hero: Object with headline, subheadline, and cta_text
        - sections: Object with content for each section
        - navigation: Navigation menu items
        - footer: Footer content
        
        Make the content engaging, professional, and appropriate for the target audience.
        Keep text concise but compelling. Include placeholder content that makes sense.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional copywriter who creates compelling website content and returns structured JSON responses."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            # Extract JSON from the response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                logger.warning("Could not extract JSON from AI response, using fallback")
                return self._mock_generate_content(request, website_plan)
                
        except Exception as e:
            logger.error(f"Error in AI content generation: {str(e)}")
            return self._mock_generate_content(request, website_plan)
    
    def _mock_generate_content(self, request, website_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock content when AI is not available."""
        website_type = website_plan.get('website_type', 'general')
        sections = website_plan.get('sections', [])
        
        # Generate title based on description and type
        title = self._generate_mock_title(request.description, website_type)
        
        # Generate hero content
        hero_content = self._generate_hero_content(website_type, request.description)
        
        # Generate section content
        sections_content = {}
        for section in sections:
            sections_content[section] = self._generate_section_content(section, website_type)
        
        return {
            "title": title,
            "description": f"Professional {website_type} website showcasing quality services and expertise.",
            "keywords": self._generate_keywords(website_type, request.description),
            "hero": hero_content,
            "sections": sections_content,
            "navigation": {
                "brand": title,
                "nav_items": [{"name": section.capitalize(), "href": f"#{section}"} for section in sections if section != "hero"]
            },
            "footer": {
                "copyright": f"© 2024 {title}. All rights reserved.",
                "links": [
                    {"name": "Privacy Policy", "href": "#privacy"},
                    {"name": "Terms of Service", "href": "#terms"}
                ]
            }
        }
    
    def _generate_mock_title(self, description: str, website_type: str) -> str:
        """Generate a mock title based on description and type."""
        if "photographer" in description.lower():
            return "Elite Photography Studio"
        elif "restaurant" in description.lower():
            return "Artisan Kitchen"
        elif "business" in description.lower() or "company" in description.lower():
            return "Professional Solutions"
        elif "portfolio" in description.lower():
            return "Creative Portfolio"
        elif "blog" in description.lower():
            return "Insights & Ideas"
        elif "shop" in description.lower() or "store" in description.lower():
            return "Premium Store"
        else:
            return "Amazing Website"
    
    def _generate_hero_content(self, website_type: str, description: str) -> Dict[str, str]:
        """Generate hero section content."""
        hero_templates = {
            "portfolio": {
                "headline": "Creating Beautiful Visual Stories",
                "subheadline": "Professional photography and creative services that capture your most important moments with artistic excellence.",
                "cta_text": "View Portfolio"
            },
            "business": {
                "headline": "Professional Solutions for Your Success",
                "subheadline": "Expert services designed to help your business grow and thrive in today's competitive market.",
                "cta_text": "Get Started"
            },
            "landing": {
                "headline": "Transform Your Business Today",
                "subheadline": "Discover innovative solutions that drive results and accelerate your growth with our proven strategies.",
                "cta_text": "Learn More"
            },
            "blog": {
                "headline": "Insights That Matter",
                "subheadline": "Expert perspectives and actionable advice to help you stay ahead in your industry.",
                "cta_text": "Read Articles"
            },
            "ecommerce": {
                "headline": "Premium Quality Products",
                "subheadline": "Discover our carefully curated collection of exceptional products designed for discerning customers.",
                "cta_text": "Shop Now"
            }
        }
        
        return hero_templates.get(website_type, {
            "headline": "Welcome to Something Amazing",
            "subheadline": "Experience quality, innovation, and excellence in everything we do.",
            "cta_text": "Discover More"
        })
    
    def _generate_section_content(self, section: str, website_type: str) -> Dict[str, Any]:
        """Generate content for a specific section."""
        content_templates = {
            "about": {
                "title": "About Us",
                "content": "We are passionate professionals dedicated to delivering exceptional results. With years of experience and a commitment to excellence, we bring creativity and expertise to every project.",
                "points": [
                    "Professional expertise and experience",
                    "Commitment to quality and innovation",
                    "Customer-focused approach",
                    "Proven track record of success"
                ]
            },
            "services": {
                "title": "Our Services",
                "content": "We offer comprehensive solutions designed to meet your unique needs and exceed your expectations.",
                "services": [
                    {
                        "name": "Premium Service",
                        "description": "High-quality solutions tailored to your specific requirements.",
                        "features": ["Feature 1", "Feature 2", "Feature 3"]
                    },
                    {
                        "name": "Expert Consultation",
                        "description": "Professional guidance to help you make informed decisions.",
                        "features": ["Analysis", "Strategy", "Implementation"]
                    },
                    {
                        "name": "Ongoing Support",
                        "description": "Continuous assistance to ensure your continued success.",
                        "features": ["24/7 Support", "Regular Updates", "Maintenance"]
                    }
                ]
            },
            "portfolio": {
                "title": "Our Work",
                "content": "Explore our collection of successful projects and creative solutions.",
                "projects": [
                    {
                        "name": "Project Alpha",
                        "description": "Innovative solution delivering exceptional results.",
                        "image": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=500"
                    },
                    {
                        "name": "Project Beta",
                        "description": "Creative approach to complex challenges.",
                        "image": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=500"
                    },
                    {
                        "name": "Project Gamma",
                        "description": "Outstanding execution and attention to detail.",
                        "image": "https://images.unsplash.com/photo-1551434678-e076c223a692?w=500"
                    }
                ]
            },
            "testimonials": {
                "title": "What Our Clients Say",
                "content": "Don't just take our word for it - hear from our satisfied clients.",
                "testimonials": [
                    {
                        "text": "Exceptional service and outstanding results. Highly recommended!",
                        "author": "Sarah Johnson",
                        "position": "CEO, Tech Solutions"
                    },
                    {
                        "text": "Professional, reliable, and delivered beyond expectations.",
                        "author": "Michael Chen",
                        "position": "Marketing Director"
                    },
                    {
                        "text": "A game-changer for our business. Couldn't be happier!",
                        "author": "Emily Rodriguez",
                        "position": "Founder, Creative Agency"
                    }
                ]
            },
            "contact": {
                "title": "Get In Touch",
                "content": "Ready to get started? Contact us today to discuss your project and learn how we can help.",
                "contact_info": {
                    "email": "hello@example.com",
                    "phone": "+1 (555) 123-4567",
                    "address": "123 Business Street, City, State 12345"
                },
                "form_fields": [
                    {"name": "name", "label": "Your Name", "type": "text", "required": True},
                    {"name": "email", "label": "Email Address", "type": "email", "required": True},
                    {"name": "subject", "label": "Subject", "type": "text", "required": False},
                    {"name": "message", "label": "Message", "type": "textarea", "required": True}
                ]
            }
        }
        
        return content_templates.get(section, {
            "title": section.title(),
            "content": f"This is the {section} section with relevant content and information."
        })
    
    def _generate_keywords(self, website_type: str, description: str) -> List[str]:
        """Generate SEO keywords based on website type and description."""
        base_keywords = ["professional", "quality", "service", "expert"]
        
        type_keywords = {
            "portfolio": ["portfolio", "creative", "design", "showcase", "gallery"],
            "business": ["business", "solutions", "corporate", "consulting"],
            "landing": ["product", "service", "landing", "conversion"],
            "blog": ["blog", "articles", "insights", "content"],
            "ecommerce": ["shop", "store", "products", "buy", "online"]
        }
        
        keywords = base_keywords + type_keywords.get(website_type, [])
        
        # Extract additional keywords from description
        description_words = re.findall(r'\b\w+\b', description.lower())
        relevant_words = [word for word in description_words 
                         if len(word) > 3 and word not in ['website', 'site', 'page', 'with', 'that', 'this']]
        
        keywords.extend(relevant_words[:5])  # Add up to 5 relevant words
        
        return list(set(keywords))  # Remove duplicates