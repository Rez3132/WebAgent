#!/usr/bin/env python3
"""
WebCreator Usage Examples
Demonstrates how to use the WebCreator agent to generate different types of amazing websites.
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from core.generator import WebCreatorGenerator, WebsiteRequest


def example_photographer_portfolio():
    """Generate a photographer portfolio website."""
    print("🎨 Generating Photographer Portfolio Website...")
    
    generator = WebCreatorGenerator()
    
    request = WebsiteRequest(
        description="Create a stunning portfolio website for a professional photographer specializing in wedding and portrait photography. Include an elegant image gallery, about section highlighting 10+ years of experience, client testimonials, and a contact form for booking inquiries.",
        website_type="portfolio",
        theme="dark",
        color_scheme="auto",
        target_audience="couples and families looking for professional photography",
        content_tone="creative",
        features=["image_gallery", "contact_form", "testimonials"]
    )
    
    website = generator.generate_website(request)
    export_path = generator.export_website(website, "generated_websites/photographer_portfolio")
    
    print(f"✅ Photographer portfolio generated in {website.generation_time:.2f}s")
    print(f"📁 Exported to: {export_path}")
    return export_path


def example_tech_startup_landing():
    """Generate a tech startup landing page."""
    print("🚀 Generating Tech Startup Landing Page...")
    
    generator = WebCreatorGenerator()
    
    request = WebsiteRequest(
        description="Build a high-converting landing page for an AI-powered productivity app called 'TaskMaster Pro'. Focus on the key benefits: 50% time savings, intelligent task prioritization, and seamless team collaboration. Include feature highlights, customer testimonials, pricing tiers, and a strong call-to-action for a free trial.",
        website_type="landing",
        theme="modern",
        color_scheme="auto",
        target_audience="busy professionals and teams",
        content_tone="persuasive",
        features=["testimonials", "pricing", "free_trial_cta"]
    )
    
    website = generator.generate_website(request)
    export_path = generator.export_website(website, "generated_websites/startup_landing")
    
    print(f"✅ Startup landing page generated in {website.generation_time:.2f}s")
    print(f"📁 Exported to: {export_path}")
    return export_path


def example_restaurant_website():
    """Generate a restaurant website."""
    print("🍽️ Generating Restaurant Website...")
    
    generator = WebCreatorGenerator()
    
    request = WebsiteRequest(
        description="Create an appetizing website for 'Bella Vista', an upscale Italian restaurant. Showcase our authentic cuisine, cozy atmosphere, and 20+ years of family tradition. Include menu highlights, chef's story, reservation system, location details, and customer reviews. Emphasize fresh ingredients and traditional recipes.",
        website_type="business",
        theme="creative",
        color_scheme="auto",
        target_audience="food enthusiasts and families",
        content_tone="warm",
        features=["menu_showcase", "reservations", "testimonials", "contact_form"]
    )
    
    website = generator.generate_website(request)
    export_path = generator.export_website(website, "generated_websites/restaurant")
    
    print(f"✅ Restaurant website generated in {website.generation_time:.2f}s")
    print(f"📁 Exported to: {export_path}")
    return export_path


def example_personal_blog():
    """Generate a personal blog website."""
    print("📝 Generating Personal Blog Website...")
    
    generator = WebCreatorGenerator()
    
    request = WebsiteRequest(
        description="Design a clean and minimal personal blog for a travel and lifestyle writer. Focus on readability and showcase recent articles about sustainable travel, cultural experiences, and travel photography tips. Include an about section, article categories, and a newsletter signup.",
        website_type="blog",
        theme="minimal",
        color_scheme="auto",
        target_audience="travel enthusiasts and conscious travelers",
        content_tone="friendly",
        features=["article_showcase", "categories", "newsletter_signup"]
    )
    
    website = generator.generate_website(request)
    export_path = generator.export_website(website, "generated_websites/travel_blog")
    
    print(f"✅ Personal blog generated in {website.generation_time:.2f}s")
    print(f"📁 Exported to: {export_path}")
    return export_path


def example_consulting_firm():
    """Generate a consulting firm website."""
    print("💼 Generating Consulting Firm Website...")
    
    generator = WebCreatorGenerator()
    
    request = WebsiteRequest(
        description="Build a professional website for 'Strategic Solutions Consulting', a management consulting firm specializing in digital transformation. Highlight our expertise in helping Fortune 500 companies modernize their operations. Include service offerings, case studies, team profiles, thought leadership, and a consultation booking system.",
        website_type="business",
        theme="corporate",
        color_scheme="auto",
        target_audience="enterprise executives and decision makers",
        content_tone="professional",
        features=["case_studies", "team_profiles", "consultation_booking", "testimonials"]
    )
    
    website = generator.generate_website(request)
    export_path = generator.export_website(website, "generated_websites/consulting_firm")
    
    print(f"✅ Consulting firm website generated in {website.generation_time:.2f}s")
    print(f"📁 Exported to: {export_path}")
    return export_path


def showcase_themes():
    """Demonstrate different themes with the same content."""
    print("🎨 Showcasing Different Themes...")
    
    generator = WebCreatorGenerator()
    base_description = "Create a portfolio website for a graphic designer"
    
    themes = ["modern", "dark", "minimal", "corporate", "creative"]
    generated_sites = []
    
    for theme in themes:
        print(f"  Generating {theme} theme...")
        
        request = WebsiteRequest(
            description=base_description,
            website_type="portfolio",
            theme=theme,
            target_audience="design-conscious clients",
            content_tone="creative"
        )
        
        website = generator.generate_website(request)
        export_path = generator.export_website(website, f"generated_websites/themes/{theme}_portfolio")
        generated_sites.append(export_path)
        
        print(f"    ✅ {theme} theme generated")
    
    print(f"✅ All {len(themes)} themes generated successfully")
    return generated_sites


def main():
    """Run all examples."""
    print("🚀 WebCreator Examples - Generating Amazing Websites\n")
    
    try:
        # Create output directory
        os.makedirs("generated_websites", exist_ok=True)
        
        # Generate different types of websites
        examples = [
            example_photographer_portfolio,
            example_tech_startup_landing,
            example_restaurant_website,
            example_personal_blog,
            example_consulting_firm
        ]
        
        generated_sites = []
        
        for example_func in examples:
            site_path = example_func()
            generated_sites.append(site_path)
            print()
        
        # Showcase different themes
        theme_sites = showcase_themes()
        generated_sites.extend(theme_sites)
        
        print(f"\n🎉 All examples completed successfully!")
        print(f"📊 Generated {len(generated_sites)} websites")
        print(f"📁 All websites saved in: generated_websites/")
        print("\n🌐 To view the websites:")
        print("  1. Navigate to any generated_websites folder")
        print("  2. Open index.html in your web browser")
        print("  3. Enjoy your AI-generated website!")
        
        # Show generation statistics
        print(f"\n📈 Generation Statistics:")
        stats = generator.get_stats()
        print(f"  • Websites generated: {stats['websites_generated']}")
        print(f"  • Total generation time: {stats['total_generation_time']:.2f}s")
        print(f"  • Average time per website: {stats['average_generation_time']:.2f}s")
        
    except Exception as e:
        print(f"❌ Example failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()