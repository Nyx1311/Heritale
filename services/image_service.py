"""
Image Service - Fetches monument images from Wikipedia/Wikimedia Commons
"""

import requests
import urllib.parse

class ImageService:
    """Service to fetch monument images from Wikipedia"""
    
    def __init__(self):
        self.wikipedia_api = "https://en.wikipedia.org/w/api.php"
        self.default_image = "/static/images/default-monument.svg"
        self.headers = {
            'User-Agent': 'AI Heritage Storyteller/1.0 (Educational Project)'
        }
    
    def get_monument_image(self, monument_name, monument_state=None):
        """
        Fetch monument image URL from Wikipedia
        
        Args:
            monument_name: Name of the monument
            monument_state: State/location for better search results
            
        Returns:
            Image URL or default image path
        """
        try:
            # Search for the monument page
            search_query = f"{monument_name} {monument_state if monument_state else ''} India monument"
            page_title = self._search_wikipedia(search_query, monument_name)
            
            if page_title:
                # Get the main image from the page
                image_url = self._get_page_image(page_title)
                if image_url:
                    return image_url
            
            # Fallback: Try direct monument name
            image_url = self._get_page_image(monument_name)
            if image_url:
                return image_url
            
            return self.default_image
            
        except Exception as e:
            print(f"Error fetching image for {monument_name}: {e}")
            return self.default_image
    
    def _search_wikipedia(self, query, monument_name):
        """Search Wikipedia for the monument"""
        try:
            params = {
                'action': 'query',
                'list': 'search',
                'srsearch': query,
                'format': 'json',
                'srlimit': 3
            }
            
            response = requests.get(self.wikipedia_api, params=params, headers=self.headers, timeout=5)
            data = response.json()
            
            if 'query' in data and 'search' in data['query']:
                results = data['query']['search']
                
                # Try to find exact or close match
                for result in results:
                    title = result['title']
                    # Check if monument name is in the title
                    if monument_name.lower() in title.lower():
                        return title
                
                # Return first result if no exact match
                if results:
                    return results[0]['title']
            
            return None
            
        except Exception as e:
            print(f"Wikipedia search error: {e}")
            return None
    
    def _get_page_image(self, page_title):
        """Get the main image from a Wikipedia page"""
        try:
            params = {
                'action': 'query',
                'titles': page_title,
                'prop': 'pageimages',
                'format': 'json',
                'pithumbsize': 800,  # Get high-quality image
                'pilicense': 'any'
            }
            
            response = requests.get(self.wikipedia_api, params=params, headers=self.headers, timeout=5)
            data = response.json()
            
            if 'query' in data and 'pages' in data['query']:
                pages = data['query']['pages']
                for page_id, page_data in pages.items():
                    if 'thumbnail' in page_data:
                        return page_data['thumbnail']['source']
                    elif 'original' in page_data:
                        return page_data['original']['source']
            
            return None
            
        except Exception as e:
            print(f"Error getting page image: {e}")
            return None
    
    def get_monument_images_gallery(self, monument_name, monument_state=None, limit=6):
        """
        Fetch multiple images for a monument from Wikipedia
        
        Args:
            monument_name: Name of the monument
            monument_state: State/location for better search results
            limit: Maximum number of images to fetch
            
        Returns:
            List of image URLs
        """
        try:
            # Search for the monument page
            search_query = f"{monument_name} {monument_state if monument_state else ''} India monument"
            page_title = self._search_wikipedia(search_query, monument_name)
            
            if page_title:
                # Get multiple images from the page
                images = self._get_page_images(page_title, limit)
                if images:
                    return images
            
            # Fallback: Try direct monument name
            images = self._get_page_images(monument_name, limit)
            if images:
                return images
            
            return [self.default_image]
            
        except Exception as e:
            print(f"Error fetching images for {monument_name}: {e}")
            return [self.default_image]
    
    def _get_page_images(self, page_title, limit=6):
        """Get multiple images from a Wikipedia page"""
        try:
            params = {
                'action': 'query',
                'titles': page_title,
                'prop': 'images',
                'format': 'json',
                'imlimit': limit * 2  # Get extra to filter out icons/flags
            }
            
            response = requests.get(self.wikipedia_api, params=params, headers=self.headers, timeout=5)
            data = response.json()
            
            image_urls = []
            
            if 'query' in data and 'pages' in data['query']:
                pages = data['query']['pages']
                for page_id, page_data in pages.items():
                    if 'images' in page_data:
                        for img in page_data['images']:
                            img_title = img['title']
                            # Filter out common non-photo files
                            if any(x in img_title.lower() for x in ['.svg', '.png', 'icon', 'flag', 'logo', 'map']):
                                continue
                            
                            # Get actual image URL
                            img_url = self._get_image_url(img_title)
                            if img_url:
                                image_urls.append(img_url)
                                
                            if len(image_urls) >= limit:
                                break
            
            return image_urls if image_urls else None
            
        except Exception as e:
            print(f"Error getting page images: {e}")
            return None
    
    def _get_image_url(self, image_title):
        """Get the actual URL for an image file"""
        try:
            params = {
                'action': 'query',
                'titles': image_title,
                'prop': 'imageinfo',
                'iiprop': 'url',
                'format': 'json',
                'iiurlwidth': 800  # Get thumbnail size
            }
            
            response = requests.get(self.wikipedia_api, params=params, headers=self.headers, timeout=5)
            data = response.json()
            
            if 'query' in data and 'pages' in data['query']:
                pages = data['query']['pages']
                for page_id, page_data in pages.items():
                    if 'imageinfo' in page_data and len(page_data['imageinfo']) > 0:
                        img_info = page_data['imageinfo'][0]
                        # Prefer thumbnail, fallback to full size
                        if 'thumburl' in img_info:
                            return img_info['thumburl']
                        elif 'url' in img_info:
                            return img_info['url']
            
            return None
            
        except Exception as e:
            print(f"Error getting image URL: {e}")
            return None
    
    def get_multiple_images(self, monuments):
        """
        Fetch images for multiple monuments
        
        Args:
            monuments: List of monument dictionaries with 'name' and 'state'
            
        Returns:
            Dictionary mapping monument_id to image_url
        """
        images = {}
        for monument in monuments:
            monument_id = monument.get('id')
            monument_name = monument.get('name')
            monument_state = monument.get('state')
            
            if monument_id and monument_name:
                image_url = self.get_monument_image(monument_name, monument_state)
                images[monument_id] = image_url
        
        return images


# Global instance
image_service = ImageService()
