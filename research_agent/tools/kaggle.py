import subprocess

def kaggle_tool(query: str) -> str:
    """
    Search for datasets on Kaggle.
    Note: Requires the kaggle python package and ~/.kaggle/kaggle.json credentials.
    
    Args:
        query: The search query.
    """
    try:
        # We use a subprocess call to the kaggle CLI if available
        result = subprocess.run(
            ["kaggle", "datasets", "list", "-s", query],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return f"Kaggle CLI error (is kaggle authenticated?): {result.stderr}"
        return result.stdout
    except Exception as e:
        return f"Error querying Kaggle: {str(e)} - Note that Kaggle CLI must be installed."
