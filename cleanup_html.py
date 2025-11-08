"""
HTML Cleanup Script for Swiftdoodles Repository
Removes Weebly dependencies and Store menu items from HTML files
Run with: python cleanup_html.py
"""

import os
import re
from pathlib import Path

# List of HTML files to process
HTML_FILES = [
    "index.html",
    "about.html",
    "blue-yonder.html",
    "bugaroo.html",
    "bugpods.html",
    "cellular.html",
    "city-lights.html",
    "crowned.html",
    "extricate.html",
    "formations.html",
    "gallery.html",
    "homage-to-miro.html",
    "inner-workings.html",
    "insectoid.html",
    "jumbled.html",
    "milking-strawberries.html",
    "new-work.html",
    "night-sky.html",
    "out-the-window.html",
    "red-rain.html",
    "rolling.html",
    "sketchbook.html",
    "string-theory.html",
    "sunshine-thoughts.html",
    "the-secret-garden.html",
    "wop-10.html",
    "wop-9.html"
]

def clean_html_content(content):
    """Clean HTML content by removing dependencies and Store menu items"""
    
    # 1. Replace Weebly font links with Google Fonts
    # Remove all individual Weebly font links
    content = re.sub(r'<link[^>]*cdn2\.editmysite\.com/fonts[^>]*>\s*', '', content)
    
    # Add Google Fonts if not already present
    if 'fonts.googleapis.com' not in content:
        google_fonts = '\t<!-- Google Fonts - replacing Weebly fonts -->\n\t<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700&family=Lora:wght@400;700&family=Dosis:wght@400;500;600;700&display=swap" rel="stylesheet">\n\t\n'
        content = content.replace('<link id="wsite-base-style"', google_fonts + '<link id="wsite-base-style"')
    
    # 2. Remove Weebly CSS files
    content = re.sub(r'<link[^>]*cdn2\.editmysite\.com/css/sites\.css[^>]*>\s*', '', content)
    content = re.sub(r'<link[^>]*cdn2\.editmysite\.com/css/old/fancybox\.css[^>]*>\s*', '', content)
    content = re.sub(r'<link[^>]*cdn2\.editmysite\.com/css/social-icons\.css[^>]*>\s*', '', content)
    content = re.sub(r'<link[^>]*cdn2\.editmysite\.com/css/old/slideshow/slideshow\.css[^>]*>\s*', '', content)
    
    # 3. Replace jQuery with modern version from reliable CDN
    content = re.sub(
        r'<script src=[\'"]https?://cdn2\.editmysite\.com/js/jquery[^>]*></script>',
        '<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>',
        content
    )
    
    # 4. Remove Weebly JavaScript files
    content = re.sub(r'<script[^>]*cdn2\.editmysite\.com/js/lang/en/stl\.js[^>]*></script>\s*', '', content)
    content = re.sub(r'<script[^>]*cdn2\.editmysite\.com/js/site/main\.js[^>]*></script>', '', content)
    content = re.sub(r'<script[^>]*cdn2\.editmysite\.com/js/old/slideshow-jq\.js[^>]*></script>\s*', '', content)
    content = re.sub(r'<script[^>]*cdn2\.editmysite\.com/js/site/main-customer-accounts-site\.js[^>]*></script>\s*', '', content)
    content = re.sub(r'<script src=[\'"]files/templateArtifacts\.js[^>]*></script>\s*', '', content)
    
    # 5. Remove Weebly variable blocks
    content = re.sub(r'<script>\s*var STATIC_BASE[^<]*</script>\s*', '', content)
    content = re.sub(r'<script type="text/javascript">\s*function initCustomerAccountsModels\(\)[^<]*</script>\s*', '', content, flags=re.DOTALL)
    content = re.sub(r'<script type="text/javascript">\s*_W = _W[^<]*</script>', '', content)
    content = re.sub(r'<script type="text/javascript">_W\.configDomain[^<]*</script>', '', content)
    content = re.sub(r'<script>_W\.relinquish[^<]*</script>\s*', '', content)
    content = re.sub(r'<script type="text/javascript" src="http://cdn2\.editmysite\.com/js/lang/en/stl\.js[^>]*></script>', '', content)
    content = re.sub(r'<script>\s*_W\.themePlugins[^<]*</script>', '', content)
    content = re.sub(r'<script type="text/javascript">\s*_W\.recaptchaUrl[^<]*</script>\s*', '', content)
    
    # 6. Comment out theme plugin scripts at bottom
    content = re.sub(
        r'<script language="javascript" src="files/theme/plugins\.js"></script>',
        '<!-- <script language="javascript" src="files/theme/plugins.js"></script> -->',
        content
    )
    content = re.sub(
        r'<script language="javascript" src="files/theme/custom\.js"></script>',
        '<!-- <script language="javascript" src="files/theme/custom.js"></script> -->',
        content
    )
    content = re.sub(
        r'<script language="javascript" src="files/theme/mobile\.js"></script>',
        '<!-- <script language="javascript" src="files/theme/mobile.js"></script> -->',
        content
    )
    
    # 7. Remove customer accounts app
    content = re.sub(r'<div id="customer-accounts-app"></div>\s*', '', content)
    
    # 8. Remove Store menu item from JavaScript array
    content = re.sub(
        r',?\{"id":"129236209278723622","title":"Store","url":"store\.html"[^}]*\}',
        '',
        content
    )
    
    # 9. Remove Store menu from desktop navigation (with or without comments)
    store_menu_pattern = r'<!--[^>]*-->\s*<li id="pg129236209278723622"[^>]*>.*?</li>\s*<!--[^>]*-->'
    content = re.sub(store_menu_pattern, '<!-- Store menu item removed -->', content, flags=re.DOTALL)
    
    store_menu_pattern2 = r'<li id="pg129236209278723622"[^>]*>.*?</li>'
    content = re.sub(store_menu_pattern2, '<!-- Store menu item removed -->', content, flags=re.DOTALL)
    
    # 10. Add mobile menu toggle script if initFlyouts exists but no mobile script
    if 'function initFlyouts' in content and 'Mobile menu toggle' not in content:
        mobile_script = '''
<script>
// Mobile menu toggle functionality
document.addEventListener('DOMContentLoaded', function() {
	var hamburger = document.querySelector('.nav-trigger');
	var mobileNav = document.querySelector('.navmobile-wrapper');
	
	if (hamburger && mobileNav) {
		hamburger.addEventListener('click', function() {
			mobileNav.classList.toggle('open');
		});
	}
	
	// Initialize flyouts if the function exists
	if (typeof initFlyouts === 'function') {
		initFlyouts();
	}
});
</script>

</body>'''
        content = content.replace('</body>', mobile_script)
    
    # 11. Add minimal menu stub if initFlyouts is called but not defined
    if 'initFlyouts()' in content and 'function initPublishedFlyoutMenus' not in content:
        menu_stub = '''
	// Minimal menu functionality stub (if needed by main_style.css)
	function initPublishedFlyoutMenus(items, currentId, prefix, activeClass, isPreview, templates) {
		// Basic implementation - can be expanded if needed
		console.log('Menu initialized with', items.length, 'items');
	}
'''
        content = content.replace('function initFlyouts(){', 'function initFlyouts(){' + menu_stub)
    
    return content

def process_files(input_dir, output_dir):
    """Process all HTML files"""
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    processed_count = 0
    skipped_count = 0
    
    print(f"Processing HTML files from: {input_dir}")
    print(f"Output directory: {output_dir}")
    print("-" * 60)
    
    for filename in HTML_FILES:
        input_file = Path(input_dir) / filename
        output_file = output_path / filename
        
        if not input_file.exists():
            print(f"⚠️  SKIP: {filename} (file not found)")
            skipped_count += 1
            continue
        
        try:
            # Read original file
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Clean the content
            cleaned_content = clean_html_content(content)
            
            # Write cleaned file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"✅ SUCCESS: {filename}")
            processed_count += 1
            
        except Exception as e:
            print(f"❌ ERROR: {filename} - {str(e)}")
            skipped_count += 1
    
    print("-" * 60)
    print(f"\nProcessing complete!")
    print(f"✅ Processed: {processed_count} files")
    print(f"⚠️  Skipped: {skipped_count} files")
    print(f"\nCleaned files saved to: {output_path.absolute()}")

def main():
    """Main function"""
    print("=" * 60)
    print("HTML Cleanup Script for Swiftdoodles Repository")
    print("=" * 60)
    print()
    
    # Get current directory
    current_dir = os.getcwd()
    
    print("Current directory:", current_dir)
    print()
    print("This script will:")
    print("  1. Look for HTML files in the current directory")
    print("  2. Remove all Weebly/editmysite.com dependencies")
    print("  3. Remove Store menu items")
    print("  4. Save cleaned files to 'cleaned_html' folder")
    print()
    
    response = input("Continue? (y/n): ").strip().lower()
    
    if response != 'y':
        print("Cancelled.")
        return
    
    print()
    
    # Process files from current directory, output to cleaned_html
    process_files(current_dir, os.path.join(current_dir, "cleaned_html"))
    
    print("\n✨ Done! Check the 'cleaned_html' folder for your cleaned files.")
    print("You can now copy these files back to your repository.")

if __name__ == "__main__":
    main()