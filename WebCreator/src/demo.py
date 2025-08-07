"""
WebCreator Interactive Demo
A Gradio-based interface for testing the website generation agent.
"""

import os
import sys
import logging
from pathlib import Path
import gradio as gr
from typing import Dict, Any, Tuple

# Add the src directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent))

from core.generator import WebCreatorGenerator, WebsiteRequest
from core.content_ai import ContentAI
from core.layout_engine import LayoutEngine
from core.style_engine import StyleEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebCreatorDemo:
    """Interactive demo interface for WebCreator."""
    
    def __init__(self):
        """Initialize the demo."""
        self.generator = WebCreatorGenerator()
        self.examples = self._get_example_prompts()
        
    def generate_website_demo(self, 
                             description: str,
                             website_type: str,
                             theme: str,
                             color_scheme: str,
                             target_audience: str,
                             content_tone: str) -> Tuple[str, str, str, str]:
        """
        Generate a website based on user inputs.
        
        Returns:
            Tuple of (html_content, css_content, js_content, metadata)
        """
        try:
            # Create website request
            request = WebsiteRequest(
                description=description,
                website_type=website_type,
                theme=theme,
                color_scheme=color_scheme,
                target_audience=target_audience,
                content_tone=content_tone,
                features=['contact_form', 'animations'],
                responsive=True,
                accessibility=True,
                performance_optimized=True
            )
            
            # Generate website
            website = self.generator.generate_website(request)
            
            # Prepare metadata
            metadata = f"""
Generation completed successfully!

**Statistics:**
- Generation time: {website.generation_time:.2f} seconds
- Website type: {website.structure.get('template_type', 'Unknown')}
- Sections: {len(website.structure.get('sections', []))}
- Features: {len(website.structure.get('features', []))}

**Metadata:**
- Title: {website.metadata.get('title', 'N/A')}
- Description: {website.metadata.get('description', 'N/A')}
- Keywords: {', '.join(website.metadata.get('keywords', []))}
- Generated at: {website.metadata.get('generated_at', 'N/A')}
            """
            
            return website.html_content, website.css_content, website.js_content, metadata
            
        except Exception as e:
            error_msg = f"Error generating website: {str(e)}"
            logger.error(error_msg)
            return error_msg, "", "", f"Generation failed: {str(e)}"
    
    def _get_example_prompts(self) -> list:
        """Get example prompts for demonstration."""
        return [
            [
                "Create a modern portfolio website for a photographer with a dark theme, image gallery, contact form, and about section",
                "portfolio",
                "dark",
                "auto",
                "photographers and artists",
                "creative"
            ],
            [
                "Build a professional business website for a consulting company with services section, testimonials, and modern design",
                "business",
                "corporate",
                "auto",
                "business professionals",
                "professional"
            ],
            [
                "Generate a landing page for a new software product with features showcase, pricing, and call-to-action",
                "landing",
                "modern",
                "auto",
                "tech entrepreneurs",
                "persuasive"
            ],
            [
                "Create a personal blog website with clean design, about section, and contact form",
                "blog",
                "minimal",
                "auto",
                "general audience",
                "friendly"
            ],
            [
                "Design a restaurant website with menu showcase, location info, and reservation system",
                "business",
                "creative",
                "auto",
                "food lovers",
                "warm"
            ]
        ]
    
    def create_interface(self) -> gr.Interface:
        """Create the Gradio interface."""
        
        with gr.Blocks(title="WebCreator - AI Website Generator", theme=gr.themes.Soft()) as demo:
            gr.Markdown("""
            # 🎨 WebCreator - AI Website Generator
            
            **Automatically generate amazing websites with AI!**
            
            Simply describe your website requirements and watch as WebCreator generates a complete, 
            responsive website with modern design, clean code, and professional content.
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 📝 Website Requirements")
                    
                    description = gr.Textbox(
                        label="Website Description",
                        placeholder="Describe your website requirements...",
                        lines=4,
                        value="Create a modern portfolio website for a photographer"
                    )
                    
                    with gr.Row():
                        website_type = gr.Dropdown(
                            label="Website Type",
                            choices=["general", "portfolio", "business", "landing", "blog", "ecommerce"],
                            value="portfolio"
                        )
                        
                        theme = gr.Dropdown(
                            label="Theme",
                            choices=["modern", "dark", "minimal", "corporate", "creative"],
                            value="modern"
                        )
                    
                    with gr.Row():
                        color_scheme = gr.Dropdown(
                            label="Color Scheme",
                            choices=["auto", "blue", "green", "purple", "orange", "red"],
                            value="auto"
                        )
                        
                        target_audience = gr.Textbox(
                            label="Target Audience",
                            placeholder="e.g., photographers, business professionals",
                            value="photographers and artists"
                        )
                    
                    content_tone = gr.Dropdown(
                        label="Content Tone",
                        choices=["professional", "friendly", "creative", "persuasive", "warm"],
                        value="creative"
                    )
                    
                    generate_btn = gr.Button("🚀 Generate Website", variant="primary", size="lg")
                
                with gr.Column(scale=2):
                    gr.Markdown("### 🎯 Generated Website")
                    
                    with gr.Tabs():
                        with gr.TabItem("Preview"):
                            html_output = gr.HTML(label="Website Preview")
                        
                        with gr.TabItem("HTML"):
                            html_code = gr.Code(label="HTML Code", language="html")
                        
                        with gr.TabItem("CSS"):
                            css_code = gr.Code(label="CSS Code", language="css")
                        
                        with gr.TabItem("JavaScript"):
                            js_code = gr.Code(label="JavaScript Code", language="javascript")
                        
                        with gr.TabItem("Info"):
                            metadata_output = gr.Markdown(label="Generation Info")
            
            # Examples section
            gr.Markdown("### 💡 Example Prompts")
            gr.Examples(
                examples=self.examples,
                inputs=[description, website_type, theme, color_scheme, target_audience, content_tone],
                label="Try these examples:"
            )
            
            # Generate button event
            generate_btn.click(
                fn=self.generate_website_demo,
                inputs=[description, website_type, theme, color_scheme, target_audience, content_tone],
                outputs=[html_code, css_code, js_code, metadata_output]
            ).then(
                fn=lambda html: html,  # Pass through HTML for preview
                inputs=[html_code],
                outputs=[html_output]
            )
            
            # Footer
            gr.Markdown("""
            ---
            
            **WebCreator** - Part of the WebAgent ecosystem by Alibaba NLP
            
            🔧 Features:
            - AI-powered content generation
            - Responsive design
            - Modern themes
            - Accessibility compliant
            - Performance optimized
            - One-click export
            """)
        
        return demo
    
    def launch(self, **kwargs):
        """Launch the demo interface."""
        demo = self.create_interface()
        demo.launch(**kwargs)


def main():
    """Main function to run the demo."""
    print("🎨 Starting WebCreator Demo...")
    
    demo = WebCreatorDemo()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )


if __name__ == "__main__":
    main()