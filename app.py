import streamlit as st
import streamlit.components.v1 as components
import requests
from playwright.sync_api import sync_playwright
import base64
from urllib.parse import urlparse
import os

class WebRenderer:
    def __init__(self):
        self.playwright = None
        self.browser = None
        
    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def capture_full_page(self, url):
        """Capture full page screenshot and return as base64"""
        page = self.browser.new_page()
        page.goto(url, wait_until='networkidle')
        page.wait_for_timeout(2000)  # Wait for any animations/loading
        screenshot = page.screenshot(full_page=True)
        page.close()
        return base64.b64encode(screenshot).decode()

    def get_page_content(self, url):
        """Get the full HTML content with styles inlined"""
        page = self.browser.new_page()
        page.goto(url, wait_until='networkidle')
        page.wait_for_timeout(2000)
        
        # Inject script to inline all styles
        page.evaluate("""() => {
            const styles = Array.from(document.styleSheets);
            styles.forEach(styleSheet => {
                try {
                    const rules = Array.from(styleSheet.cssRules);
                    rules.forEach(rule => {
                        if (rule.style) {
                            Array.from(document.querySelectorAll(rule.selectorText)).forEach(element => {
                                Object.assign(element.style, rule.style);
                            });
                        }
                    });
                } catch (e) {}
            });
        }""")
        
        content = page.content()
        page.close()
        return content

def check_iframe_allowed(url):
    """Check if iframe embedding is allowed"""
    try:
        response = requests.head(url)
        x_frame_options = response.headers.get('X-Frame-Options', '').upper()
        csp = response.headers.get('Content-Security-Policy', '')
        
        if x_frame_options in ['DENY', 'SAMEORIGIN']:
            return False
        if 'frame-ancestors' in csp and 'frame-ancestors *' not in csp:
            return False
        return True
    except:
        return False

def main():
    st.set_page_config(
        page_title="Advanced Website Renderer",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.title("Advanced Website Renderer")
    
    url = "https://paulspector.com/we-should-not-discourage-students-from-manual-work/"
    
    if url:
        domain = urlparse(url).netloc
        st.write(f"Rendering content from: {domain}")
        
        # Try iframe first
        if check_iframe_allowed(url):
            st.success("Direct embedding supported!")
            components.iframe(url, height=800, scrolling=True)
        else:
            st.info("Direct embedding not supported. Using advanced rendering...")
            
            # Use Playwright for advanced rendering
            with st.spinner("Rendering page content..."):
                with WebRenderer() as renderer:
                    # Create tabs for different viewing options
                    tab1, tab2 = st.tabs(["Interactive View", "Full Page Screenshot"])
                    
                    with tab1:
                        # Get and display the HTML content
                        content = renderer.get_page_content(url)
                        components.html(content, height=800, scrolling=True)
                    
                    with tab2:
                        # Get and display the screenshot
                        screenshot = renderer.capture_full_page(url)
                        st.image(f"data:image/png;base64,{screenshot}", 
                                use_column_width=True,
                                caption="Full page screenshot")
        
        # Add original link
        st.markdown(f"View original website: [{url}]({url})")

if __name__ == "__main__":
    main()
