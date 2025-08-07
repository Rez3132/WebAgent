"""
WebCreator Layout Engine
Generates responsive website layouts and structures.
"""

import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class LayoutEngine:
    """Generates website layouts and structures based on content and requirements."""
    
    def __init__(self):
        """Initialize the layout engine."""
        self.grid_systems = {
            'modern': 'css-grid',
            'classic': 'flexbox',
            'responsive': 'css-grid'
        }
        
        logger.info("LayoutEngine initialized")
    
    def create_layout(self, website_plan: Dict[str, Any], content_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a layout structure based on the website plan and content.
        
        Args:
            website_plan: Website structure plan from analysis
            content_data: Generated content data
            
        Returns:
            Layout structure dictionary
        """
        website_type = website_plan.get('website_type', 'modern')
        sections = website_plan.get('sections', [])
        
        layout_structure = {
            'template_type': website_type,
            'grid_system': self.grid_systems.get(website_type, 'css-grid'),
            'sections': [],
            'navigation': self._create_navigation_layout(website_plan, content_data),
            'footer': self._create_footer_layout(content_data),
            'responsive_breakpoints': {
                'mobile': '768px',
                'tablet': '1024px',
                'desktop': '1280px'
            },
            'components': website_plan.get('components_needed', [])
        }
        
        # Create layout for each section
        if sections:
            for section in sections:
                section_layout = self._create_section_layout(
                    section, website_type, content_data.get('sections', {}).get(section)
                )
                layout_structure['sections'].append(section_layout)
        
        logger.info(f"Layout created with {len(layout_structure['sections'])} sections")
        return layout_structure
    
    def _create_navigation_layout(self, website_plan: Dict, content_data: Dict) -> Dict[str, Any]:
        """Create navigation layout structure."""
        nav_data = content_data.get('navigation', {})
        
        return {
            'type': 'header-nav',
            'layout': 'horizontal',
            'sticky': True,
            'mobile_hamburger': True,
            'brand': {
                'text': nav_data.get('brand', 'Brand'),
                'logo': None  # Can be added later
            },
            'items': nav_data.get('items', []),
            'cta_button': {
                'text': 'Get Started',
                'href': '#contact',
                'style': 'primary'
            }
        }
    
    def _create_footer_layout(self, content_data: Dict) -> Dict[str, Any]:
        """Create footer layout structure."""
        footer_data = content_data.get('footer', {})
        
        return {
            'type': 'multi-column',
            'columns': [
                {
                    'title': 'Quick Links',
                    'items': footer_data.get('links', [])
                },
                {
                    'title': 'Contact',
                    'items': [
                        {'name': 'Email', 'value': 'hello@example.com'},
                        {'name': 'Phone', 'value': '+1 (555) 123-4567'}
                    ]
                }
            ],
            'bottom': {
                'copyright': footer_data.get('copyright', '© 2024 All rights reserved.'),
                'social_links': []
            }
        }
    
    def _create_section_layout(self, section_name: str, website_type: str, content: Optional[Dict]) -> Dict[str, Any]:
        """Create layout for a specific section."""
        
        # Default section layout
        section_layout = {
            'name': section_name,
            'type': self._get_section_type(section_name),
            'container': 'container',
            'padding': 'py-16',
            'content': content or {}
        }
        
        # Customize layout based on section type
        if section_name == 'hero':
            section_layout.update(self._create_hero_layout(website_type, content))
        elif section_name == 'about':
            section_layout.update(self._create_about_layout(content))
        elif section_name == 'services':
            section_layout.update(self._create_services_layout(content))
        elif section_name == 'portfolio':
            section_layout.update(self._create_portfolio_layout(content))
        elif section_name == 'testimonials':
            section_layout.update(self._create_testimonials_layout(content))
        elif section_name == 'contact':
            section_layout.update(self._create_contact_layout(content))
        
        return section_layout
    
    def _get_section_type(self, section_name: str) -> str:
        """Determine the layout type for a section."""
        section_types = {
            'hero': 'hero-banner',
            'about': 'text-image',
            'services': 'card-grid',
            'portfolio': 'gallery-grid',
            'testimonials': 'testimonial-slider',
            'contact': 'contact-form'
        }
        return section_types.get(section_name, 'text-block')
    
    def _create_hero_layout(self, website_type: str, content: Optional[Dict]) -> Dict[str, Any]:
        """Create hero section layout."""
        hero_layouts = {
            'portfolio': {
                'layout': 'center-aligned',
                'background': 'gradient',
                'text_position': 'center',
                'cta_style': 'prominent',
                'height': 'vh-90'
            },
            'business': {
                'layout': 'split-layout',
                'background': 'solid',
                'text_position': 'left',
                'cta_style': 'button-group',
                'height': 'vh-80'
            },
            'landing': {
                'layout': 'center-aligned',
                'background': 'gradient',
                'text_position': 'center',
                'cta_style': 'large-button',
                'height': 'vh-100'
            }
        }
        
        layout = hero_layouts.get(website_type, {
            'layout': 'center-aligned',
            'background': 'gradient',
            'text_position': 'center',
            'cta_style': 'button',
            'height': 'vh-80'
        })
        
        layout.update({
            'elements': [
                {'type': 'headline', 'text': content.get('headline') if content else 'Welcome'},
                {'type': 'subheadline', 'text': content.get('subheadline') if content else 'Subtitle'},
                {'type': 'cta_button', 'text': content.get('cta_text') if content else 'Get Started'}
            ]
        })
        
        return layout
    
    def _create_about_layout(self, content: Optional[Dict]) -> Dict[str, Any]:
        """Create about section layout."""
        return {
            'layout': 'two-column',
            'text_column': 'left',
            'image_column': 'right',
            'elements': [
                {'type': 'title', 'text': content.get('title') if content else 'About Us'},
                {'type': 'content', 'text': content.get('content') if content else ''},
                {'type': 'bullet_points', 'items': content.get('points') if content else []}
            ],
            'image': {
                'src': 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=600',
                'alt': 'About us image'
            }
        }
    
    def _create_services_layout(self, content: Optional[Dict]) -> Dict[str, Any]:
        """Create services section layout."""
        return {
            'layout': 'card-grid',
            'columns': {
                'mobile': 1,
                'tablet': 2,
                'desktop': 3
            },
            'card_style': 'elevated',
            'elements': [
                {'type': 'section_title', 'text': content.get('title') if content else 'Our Services'},
                {'type': 'section_content', 'text': content.get('content') if content else ''},
                {'type': 'service_cards', 'services': content.get('services') if content else []}
            ]
        }
    
    def _create_portfolio_layout(self, content: Optional[Dict]) -> Dict[str, Any]:
        """Create portfolio section layout."""
        return {
            'layout': 'masonry-grid',
            'columns': {
                'mobile': 1,
                'tablet': 2,
                'desktop': 3
            },
            'hover_effects': True,
            'lightbox': True,
            'elements': [
                {'type': 'section_title', 'text': content.get('title') if content else 'Our Work'},
                {'type': 'section_content', 'text': content.get('content') if content else ''},
                {'type': 'project_grid', 'projects': content.get('projects') if content else []}
            ]
        }
    
    def _create_testimonials_layout(self, content: Optional[Dict]) -> Dict[str, Any]:
        """Create testimonials section layout."""
        return {
            'layout': 'carousel',
            'auto_play': True,
            'indicators': True,
            'navigation': True,
            'elements': [
                {'type': 'section_title', 'text': content.get('title') if content else 'Testimonials'},
                {'type': 'testimonial_slider', 'testimonials': content.get('testimonials') if content else []}
            ]
        }
    
    def _create_contact_layout(self, content: Optional[Dict]) -> Dict[str, Any]:
        """Create contact section layout."""
        return {
            'layout': 'split-layout',
            'form_column': 'left',
            'info_column': 'right',
            'elements': [
                {'type': 'section_title', 'text': content.get('title') if content else 'Contact Us'},
                {'type': 'contact_form', 'fields': content.get('form_fields') if content else []},
                {'type': 'contact_info', 'info': content.get('contact_info') if content else {}}
            ]
        }
    
    def get_responsive_classes(self, breakpoint: str) -> Dict[str, str]:
        """Get responsive CSS classes for a breakpoint."""
        classes = {
            'mobile': {
                'container': 'px-4',
                'grid': 'grid-cols-1',
                'text': 'text-sm',
                'spacing': 'gap-4'
            },
            'tablet': {
                'container': 'px-6',
                'grid': 'md:grid-cols-2',
                'text': 'md:text-base',
                'spacing': 'md:gap-6'
            },
            'desktop': {
                'container': 'px-8',
                'grid': 'lg:grid-cols-3',
                'text': 'lg:text-lg',
                'spacing': 'lg:gap-8'
            }
        }
        return classes.get(breakpoint, {})
    
    def optimize_layout_for_mobile(self, layout_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize layout structure for mobile devices."""
        # Ensure mobile-first responsive design
        for section in layout_structure.get('sections', []):
            if section.get('layout') == 'split-layout':
                section['mobile_layout'] = 'stacked'
            elif section.get('layout') == 'card-grid':
                section['mobile_columns'] = 1
        
        # Optimize navigation for mobile
        nav = layout_structure.get('navigation', {})
        nav['mobile_hamburger'] = True
        nav['mobile_overlay'] = True
        
        return layout_structure