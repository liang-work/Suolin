import rich
import SolarNetworkAPI
from readFile import LoadJson

# Initialize API client and console
api = SolarNetworkAPI.SNAPI()
console = rich.console.Console()

def get_character_width(text: str) -> int:
    """
    Calculate the display width of a text string.
    Chinese characters count as 2 width units, others as 1.
    
    Args:
        text (str): Input text string
        
    Returns:
        int: Total display width of the text
    """
    width = 0
    for char in text:
        if ord(char) > 127:  # Non-ASCII characters (Chinese, etc.)
            width += 2
        else:  # ASCII characters
            width += 1
    return width

def get_post_row(post: dict, config: dict) -> int:
    """
    Calculate the number of rows needed to display a post.
    Considers title, description, content, publisher nick and name.
    
    Args:
        post (dict): Post data dictionary
        config (dict): Configuration with MaxWidth setting
        
    Returns:
        int: Total number of rows required
    """
    post_row = 0
    max_width = config['MaxWidth'] - 4  # Account for padding
    
    # Calculate rows for title if present
    if post.get('data', {}).get('title', '') != "":
        title_length = get_character_width(post.get('data', {}).get('title', ''))
        post_row += (title_length // max_width) + 1
    
    # Calculate rows for description if present
    if post.get('data', {}).get('description', '') != "":
        description_length = get_character_width(post.get('data', {}).get('description', ''))
        post_row += (description_length // max_width) + 1
    
    # Calculate rows for content if present
    if post.get('data', {}).get('content', '') != "":
        content_length = get_character_width(post.get('data', {}).get('content', ''))
        post_row += (content_length // max_width) + 1
    
    # Calculate rows for publisher information
    publisher_nick_length = get_character_width(post.get('data', {}).get('publisher', {}).get('nick', ''))
    publisher_name_length = get_character_width(post.get('data', {}).get('publisher', {}).get('name', ''))
    
    post_row += (publisher_nick_length // max_width) + 1  # Publisher nick
    post_row += (publisher_name_length // max_width) + 1  # Publisher name
    
    return post_row + 1  # Add 1 for spacing between posts

def get_show_post_count(post_rows: int, config: dict) -> int:
    """
    Calculate how many posts can be shown based on available rows.
    
    Args:
        post_rows (int): Total rows required for posts
        config (dict): Configuration with MaxHeight setting
        
    Returns:
        int: Number of posts that can be displayed
    """
    available_height = config['MaxHeight'] - 2  # Account for UI elements
    show_post_count = post_rows // available_height
    
    # Add extra page if there are remaining rows
    if post_rows % available_height != 0:
        show_post_count += 1
    
    return show_post_count

def home(token: str = "", config: dict = {}) -> None:
    """
    Display home page with recent activity posts.
    
    Args:
        token (str): Authentication token (optional)
        config (dict): Configuration dictionary (optional)
    """
    # Load default config if not provided
    if config == {}:
        config = LoadJson("config.json")
    
    # Fetch home activity data
    home_data: list[dict] = api.get_home_activity(Authorization=token, take=5)
    post_count: int = len(home_data)
    post_show_count: int = 0
    
    # Calculate total display rows needed
    for post in home_data:
        post_row = get_post_row(post, config)
        post_show_count = post_show_count + get_show_post_count(post_row, config)