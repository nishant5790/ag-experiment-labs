import shutil
import subprocess

def kaggle_tool(query: str) -> str:
    """
    Search for datasets on Kaggle.
    Note: Requires the kaggle python package and ~/.kaggle/kaggle.json credentials.
    
    Args:
        query: The search query.
    """
    if not shutil.which("kaggle"):
        return (
            "Kaggle CLI is not installed. To use this tool:\n"
            "  1. pip install kaggle\n"
            "  2. Place your API token at ~/.kaggle/kaggle.json\n"
            "     (Get it from https://www.kaggle.com/settings -> API -> Create New Token)\n"
            "  3. chmod 600 ~/.kaggle/kaggle.json"
        )
    try:
        result = subprocess.run(
            ["kaggle", "datasets", "list", "-s", query],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            return f"Kaggle CLI error (is kaggle authenticated?): {result.stderr.strip()}"
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Kaggle CLI timed out. Please check your network connection."
    except Exception as e:
        return f"Error querying Kaggle: {str(e)}"
