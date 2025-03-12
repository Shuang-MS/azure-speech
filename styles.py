def load_css():
    """Return the CSS styles for the application."""
    return """
<style>
    .grid-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-gap: 20px;
        margin: 30px 0;
    }
    .grid-item {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        transition: transform 0.3s, box-shadow 0.3s;
        cursor: pointer;
        height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .grid-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .icon {
        font-size: 3rem;
        margin-bottom: 10px;
    }
    .title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .description {
        font-size: 0.9rem;
        color: #555;
    }
    .centered-title {
        text-align: center;
        margin-bottom: 20px;
    }
</style>
"""
