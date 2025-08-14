"""Resource management for documentation links."""

from typing import Dict, List


class ResourceManager:
    """Manages documentation and learning resources."""
    
    def __init__(self, resource_mappings: Dict[str, Dict[str, List[str]]]):
        self.resource_mappings = resource_mappings
    
    def get_resources(self, language: str, category: str) -> List[str]:
        """Get relevant resources for language and category."""
        resources = []
        
        if language in self.resource_mappings and category in self.resource_mappings[language]:
            resources.extend(self.resource_mappings[language][category][:3])
        
        # Fallback to Python resources if specific language not available
        if not resources and 'python' in self.resource_mappings and category in self.resource_mappings['python']:
            resources.extend(self.resource_mappings['python'][category][:2])
        
        return resources
    
    def extract_resource_name(self, url: str) -> str:
        """Extract meaningful name from URL."""
        try:
            name = url.split('/')[-1]
            if not name or name in ['', 'index.html']:
                name = url.split('/')[-2]
            
            name = name.replace('-', ' ').replace('_', ' ').replace('.html', '')
            name = ' '.join(word.capitalize() for word in name.split())
            
            # Add context based on domain
            if 'pep8.org' in url:
                name = "PEP 8 Style Guide"
            elif 'docs.python.org' in url:
                name = f"Python Documentation: {name}"
            elif 'developer.mozilla.org' in url:
                name = f"MDN: {name}"
            elif 'google.github.io' in url:
                name = f"Google Style Guide: {name}"
            elif 'eslint.org' in url:
                name = f"ESLint: {name}"
            
            return name or "Documentation"
        except:
            return "Related Documentation"
