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
