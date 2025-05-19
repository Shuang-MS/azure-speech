def load_css():
    """Return the CSS styles for the application."""
    return """
<style>  
    .main .block-container {{  
        max-width: 1200px;  
        padding-top: 2rem;  
    }}  
    .feature-card {{  
        background: #ffffff;  
        border-radius: 15px;  
        padding: 2rem;  
        margin: 1rem;  
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);  
        transition: transform 0.2s, box-shadow 0.2s;  
        height: 300px;  
        display: flex;  
        flex-direction: column;  
        justify-content: space-between;  
    }}  
    .feature-card:hover {{  
        transform: translateY(-5px);  
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);  
        cursor: pointer;  
    }}  
    /* New container constraints */  
    .main {{  
        display: flex;  
        justify-content: center;  
    }}  
    @media (min-width: 1200px) {{  
        .main .block-container {{  
            width: 1200px;  
            max-width: 1200px !important;  
            padding-left: 2rem;  
            padding-right: 2rem;  
        }}  
    }}  
</style>  
"""

def get_iframe_fullscreen_style():
    """
    Returns CSS styling for embedding an iframe that takes up the full screen.
    Removes all margins, paddings, scrollbars and hides default Streamlit UI elements.
    """
    return """
    /* Hide all default UI elements */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Remove all margins, paddings, and scrollbars */
    html, body, [class*="css"] {
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    
    /* Make iframe container take full viewport height */
    .iframe-container {
        position: relative;
        width: 100vw;
        height: 100vh; /* Use full viewport height */
        overflow: hidden;
        margin: 0;
        padding: 0;
    }
    
    .responsive-iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border: none;
    }
    
    /* Remove all padding and margins from Streamlit containers */
    .stApp {
        padding: 0 !important;
        margin: 0 !important;
        overflow: hidden !important;
    }
    
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    /* Hide the tiny header too */
    h3 {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding: 0 !important;
        line-height: 0 !important;
        font-size: 0.7rem !important;
    }
    
    /* Target the specific div that wraps Streamlit content */
    .stApp > div:first-child {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    section[data-testid="stSidebar"] {
        width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    """

def get_credential_page_style():
    return """
    <style>
        /* Make file uploader use full width */
        [data-testid='stFileUploader'],
        [data-testid='stFileUploader'] section,
        [data-testid='stFileUploaderDropzone'] {
            width: 100%;
        }
        
        /* Remove padding */
        [data-testid='stFileUploader'] section {
            padding: 0;
        }
        
        /* Hide help text */
        [data-testid='stFileUploader'] section > input + div {
            display: none;
        }
        
        /* Adjust spacing for file details */
        [data-testid='stFileUploader'] section + div {
            padding-top: 0;
        }
        [data-testid="stFileUploaderDropzone"] {
            background-color: #001E38;
            border: 1px solid #FFFFFF33;
        }
        
        [data-testid="stFileUploaderDropzone"] button {
            visibility: hidden;
            width: 100%;
            justify-content: center;
        }

        div[data-testid="stFileUploader"] section:hover {
            border-color: #E694FF;
            color: #E694FF;
        }
        
        [data-testid="stFileUploaderDropzone"] button::after {
            content: "Browse";
            visibility: visible;
            position: absolute;
        }

    </style>
    """

def get_file_uploader_style():
    return f"""
    <style>
        div[data-testid="stFileUploaderDropzoneInstructions"]>div>small {{
            visibility:hidden;
        }}
    </style>
    """