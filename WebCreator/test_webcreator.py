#!/usr/bin/env python3
"""
Test script for WebCreator
Tests the basic functionality of the website generation agent.
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from core.generator import WebCreatorGenerator, WebsiteRequest


def test_basic_generation():
    """Test basic website generation."""
    print("🧪 Testing WebCreator basic generation...")
    
    # Initialize generator
    generator = WebCreatorGenerator()
    
    # Create a test request
    request = WebsiteRequest(
        description="Create a modern portfolio website for a photographer with dark theme and gallery",
        website_type="portfolio",
        theme="dark",
        target_audience="photographers",
        content_tone="creative",
        features=["contact_form", "image_gallery"]
    )
    
    # Generate website
    print("⚡ Generating website...")
    website = generator.generate_website(request)
    
    # Verify results
    assert website.html_content, "HTML content should not be empty"
    assert website.css_content, "CSS content should not be empty"
    assert website.js_content, "JavaScript content should not be empty"
    assert website.metadata, "Metadata should not be empty"
    
    print(f"✅ Generation successful! ({website.generation_time:.2f}s)")
    print(f"📊 HTML length: {len(website.html_content)} chars")
    print(f"📊 CSS length: {len(website.css_content)} chars")
    print(f"📊 JS length: {len(website.js_content)} chars")
    
    return website


def test_export_functionality():
    """Test website export functionality."""
    print("📦 Testing export functionality...")
    
    generator = WebCreatorGenerator()
    
    # Generate a simple website
    request = WebsiteRequest(
        description="Simple business website",
        website_type="business",
        theme="modern"
    )
    
    website = generator.generate_website(request)
    
    # Export to test directory
    export_path = generator.export_website(website, "/tmp/test_website")
    
    # Verify exported files
    assert Path(export_path, "index.html").exists(), "HTML file should exist"
    assert Path(export_path, "styles.css").exists(), "CSS file should exist"
    assert Path(export_path, "script.js").exists(), "JS file should exist"
    assert Path(export_path, "metadata.json").exists(), "Metadata file should exist"
    
    print(f"✅ Export successful to: {export_path}")
    
    return export_path


def test_different_website_types():
    """Test generation of different website types."""
    print("🎭 Testing different website types...")
    
    generator = WebCreatorGenerator()
    
    website_types = ["portfolio", "business", "landing", "blog"]
    
    for website_type in website_types:
        print(f"  Testing {website_type} website...")
        
        request = WebsiteRequest(
            description=f"Create a {website_type} website",
            website_type=website_type,
            theme="modern"
        )
        
        website = generator.generate_website(request)
        
        assert website.html_content, f"{website_type} HTML should not be empty"
        assert website.structure.get('template_type') == website_type, f"Template type should be {website_type}"
        
        print(f"    ✅ {website_type} generated successfully")
    
    print("✅ All website types tested successfully")


def test_themes():
    """Test different themes."""
    print("🎨 Testing different themes...")
    
    generator = WebCreatorGenerator()
    
    themes = ["modern", "dark", "minimal", "corporate", "creative"]
    
    for theme in themes:
        print(f"  Testing {theme} theme...")
        
        request = WebsiteRequest(
            description="Test website for theme testing",
            theme=theme
        )
        
        website = generator.generate_website(request)
        
        assert website.css_content, f"{theme} CSS should not be empty"
        # Check if theme colors are applied (basic check)
        assert "var(--color-primary)" in website.css_content, "CSS should contain theme variables"
        
        print(f"    ✅ {theme} theme generated successfully")
    
    print("✅ All themes tested successfully")


def main():
    """Run all tests."""
    print("🚀 Starting WebCreator Tests\n")
    
    try:
        # Run tests
        website = test_basic_generation()
        print()
        
        export_path = test_export_functionality()
        print()
        
        test_different_website_types()
        print()
        
        test_themes()
        print()
        
        print("🎉 All tests passed successfully!")
        print(f"\n📁 Sample website exported to: {export_path}")
        print("🌐 You can open index.html in a browser to view the generated website.")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()