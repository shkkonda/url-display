import streamlit as st
import streamlit.components.v1 as components
import requests

def check_url_accessibility(url):
    """
    Check if the URL is accessible and returns proper headers
    """
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Website Renderer",
        page_icon="🌐",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Add title
    st.title("Website Renderer")
    
    # URL to render
    url = "https://paulspector.com/we-should-not-discourage-students-from-manual-work/"
    
    if url:
        # Check if URL is accessible
        if check_url_accessibility(url):
            # Create a container for the iframe
            container = st.container()
            
            with container:
                # Add some styling to ensure the iframe takes up most of the space
                st.markdown("""
                    <style>
                        iframe {
                            width: 100%;
                            height: 800px;
                            border: none;
                            border-radius: 8px;
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        }
                    </style>
                """, unsafe_allow_html=True)
                
                # Render the webpage in an iframe
                components.iframe(url, height=800, scrolling=True)
                
                # Add a direct link to the website
                st.markdown(f"<br>View the original website: [{url}]({url})", unsafe_allow_html=True)
        else:
            st.error("Unable to access the URL. Please check if the website is accessible and allows embedding.")
            
        # Add footer with additional information
        st.markdown("---")
        st.markdown("""
            <small>Note: Some websites may block embedding due to security policies. 
            In such cases, you'll need to visit the original website directly.</small>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()