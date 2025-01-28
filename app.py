import streamlit as st
import requests
from bs4 import BeautifulSoup
import html2text

def fetch_url_content(url):
    """
    Fetches and parses content from a given URL.
    Returns both HTML and plain text versions.
    """
    try:
        # Send request with a user agent to avoid potential blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Convert HTML to markdown/plain text
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        plain_text = h.handle(response.text)
        
        return soup.prettify(), plain_text
        
    except requests.RequestException as e:
        st.error(f"Error fetching URL: {str(e)}")
        return None, None

def main():
    # Set page configuration
    st.set_page_config(
        page_title="URL Content Renderer",
        page_icon="🌐",
        layout="wide"
    )
    
    # Add title and description
    st.title("URL Content Renderer")
    st.write("This app fetches and displays content from a given URL.")
    
    # URL input
    url = "https://paulspector.com/we-should-not-discourage-students-from-manual-work/"
    
    if url:
        # Add a spinner while loading
        with st.spinner('Fetching content...'):
            html_content, plain_text = fetch_url_content(url)
            
            if html_content and plain_text:
                # Create tabs for different view options
                tab1, tab2 = st.tabs(["Rendered Content", "Raw HTML"])
                
                with tab1:
                    st.markdown(plain_text)
                
                with tab2:
                    st.code(html_content, language='html')
                    
                # Add download buttons
                st.download_button(
                    label="Download as Text",
                    data=plain_text,
                    file_name="content.txt",
                    mime="text/plain"
                )
                
                st.download_button(
                    label="Download as HTML",
                    data=html_content,
                    file_name="content.html",
                    mime="text/html"
                )

if __name__ == "__main__":
    main()