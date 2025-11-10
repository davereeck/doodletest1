"""
HTML Cleanup Script for Swiftdoodles Repository
Removes Weebly dependencies, Store menu items, and adds mobile menu support
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

def create_mobile_menu_files(output_dir):
    """Create mobile-menu.css and mobile-menu.js files"""
    files_dir = Path(output_dir) / "files"
    files_dir.mkdir(exist_ok=True)
    
    # Create mobile-menu.css
    css_content = """/* Mobile Menu Styles - Override Weebly CSS */
@media screen and (max-width: 767px) {
    /* Hide desktop menu on mobile */
    #navigation {
        display: none !important;
    }
    
    /* Show hamburger menu on mobile */
    .nav-trigger {
        display: block !important;
        cursor: pointer;
        padding: 15px;
        z-index: 1000;
        position: relative;
    }
    
    .nav-trigger .mobile {
        display: block !important;
        width: 25px;
        height: 3px;
        background-color: #fbd634 !important;
        margin: 5px 0;
        transition: 0.3s;
    }
    
    /* Mobile menu wrapper - FORCE visibility */
    .navmobile-wrapper {
        display: block !important;
        position: fixed !important;
        top: 0 !important;
        right: -100% !important;
        width: 250px !important;
        height: 100% !important;
        background-color: rgba(0, 0, 0, 0.95) !important;
        z-index: 999 !important;
        overflow-y: auto !important;
        transition: right 0.3s ease !important;
        padding-top: 60px !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    .navmobile-wrapper.open {
        right: 0 !important;
    }
    
    /* Mobile menu items - FORCE visibility and colors */
    #navmobile {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    #navmobile ul {
        list-style: none !important;
        padding: 0 !important;
        margin: 0 !important;
        display: block !important;
        visibility: visible !important;
    }
    
    #navmobile .wsite-menu-item-wrap {
        display: block !important;
        visibility: visible !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    #navmobile .wsite-menu-item {
        display: block !important;
        visibility: visible !important;
        padding: 15px 20px !important;
        color: #ffffff !important;
        text-decoration: none !important;
        font-size: 16px !important;
        transition: background-color 0.3s !important;
        opacity: 1 !important;
        font-family: "Raleway", Arial, sans-serif !important;
    }
    
    #navmobile .wsite-menu-item:hover,
    #navmobile #active .wsite-menu-item {
        background-color: rgba(251, 214, 52, 0.2) !important;
        color: #fbd634 !important;
    }
    
    /* Overlay when menu is open */
    body.menu-open::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        z-index: 998;
    }
}

/* Desktop: hide mobile menu and hamburger */
@media screen and (min-width: 768px) {
    .navmobile-wrapper {
        display: none !important;
    }
    
    .nav-trigger {
        display: none !important;
    }
    
    #navigation {
        display: block !important;
    }
}
"""
    
    css_file = files_dir / "mobile-menu.css"
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(css_content)
    print(f"✅ Created: {css_file}")
    
    # Create mobile-menu.js
    js_content = """// Mobile menu toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    var hamburger = document.querySelector('.nav-trigger');
    var mobileNav = document.querySelector('.navmobile-wrapper');
    var body = document.body;
    
    if (hamburger && mobileNav) {
        // Toggle menu when hamburger is clicked
        hamburger.addEventListener('click', function(e) {
            e.stopPropagation();
            mobileNav.classList.toggle('open');
            body.classList.toggle('menu-open');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (mobileNav.classList.contains('open') && 
                !mobileNav.contains(e.target) && 
                !hamburger.contains(e.target)) {
                mobileNav.classList.remove('open');
                body.classList.remove('menu-open');
            }
        });
        
        // Close menu when clicking a menu item
        var menuLinks = mobileNav.querySelectorAll('.wsite-menu-item');
        menuLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                mobileNav.classList.remove('open');
                body.classList.remove('menu-open');
            });
        });
    }
    
    // Initialize flyouts if the function exists
    if (typeof initFlyouts === 'function') {
        initFlyouts();
    }
});
"""
    
    js_file = files_dir / "mobile-menu.js"
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"✅ Created: {js_file}")

def clean_html_content(content):
    """Clean HTML content by removing dependencies and Store menu items"""
    
    # Track if mobile menu CSS is already present
    has_mobile_css = 'files/mobile-menu.css' in content
    has_mobile_js = 'files/mobile-menu.js' in content
    
    # 1. Replace Weebly font links with Google Fonts (only if not already present)
    if 'fonts.googleapis.com' not in content:
        # Remove all individual Weebly font links
        content = re.sub(r'<link[^>]*cdn2\.editmysite\.com/fonts[^>]*>\s*', '', content)
        
        # Add Google Fonts
        google_fonts = '\t<!-- Google Fonts - replacing Weebly fonts -->\n\t<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700&family=Lora:wght@400;700&family=Dosis:wght@400;500;600;700&display=swap" rel="stylesheet">\n\t\n'
        
        # Find a good place to insert (after viewport meta or before first link)
        if '<meta name="viewport"' in content:
            content = content.replace('<meta name="viewport"', f'{google_fonts}<meta name="viewport"')
        elif '<link' in content:
            content = content.replace('<link', f'{google_fonts}<link', 1)
    
    # 2. Remove Weebly CSS files
    content = re.sub(r'<link[^>]*cdn2\.editmysite\.com/css/sites\.css[^>]*>\s*', '', content)
    content = re.sub(r'<link[^>]*cdn2\.editmysite\.com/css/old/fancybox\.css[^>]*>\s*', '', content)
    content = re.sub(r'<link[^>]*cdn2\.editmysite\.com/css/social-icons\.css[^>]*>\s*', '', content)
    content = re.sub(r'<link[^>]*cdn2\.editmysite\.com/css/old/slideshow/slideshow\.css[^>]*>\s*', '', content)
    
    # 3. Add mobile menu CSS if not already present
    if not has_mobile_css and 'files/main_style.css' in content:
        # Add after main_style.css
        content = content.replace(
            'files/main_style.css?1762544893" title="wsite-theme-css" />',
            'files/main_style.css?1762544893" title="wsite-theme-css" />\n<link rel="stylesheet" type="text/css" href="files/mobile-menu.css" />'
        )
    
    # 4. Replace jQuery with modern version from reliable CDN
    content = re.sub(
        r'<script src=[\'"]https?://cdn2\.editmysite\.com/js/jquery[^>]*></script>',
        '<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>',
        content
    )
    
    # 5. Remove Weebly JavaScript files
    content = re.sub(r'<script[^>]*cdn2\.editmysite\.com/js/lang/en/stl\.js[^>]*></script>\s*', '', content)
    content = re.sub(r'<script[^>]*cdn2\.editmysite\.com/js/site/main\.js[^>]*></script>', '', content)
    content = re.sub(r'<script[^>]*cdn2\.editmysite\.com/js/old/slideshow-jq\.js[^>]*></script>\s*', '', content)
    content = re.sub(r'<script[^>]*cdn2\.editmysite\.com/js/site/main-customer-accounts-site\.js[^>]*></script>\s*', '', content)
    content = re.sub(r'<script src=[\'"]files/templateArtifacts\.js[^>]*></script>\s*', '', content)
    
    # 6. Remove Weebly variable blocks
    content = re.sub(r'<script>\s*var STATIC_BASE[^<]*</script>\s*', '', content)
    content = re.sub(r'<script type="text/javascript">\s*function initCustomerAccountsModels\(\)[^<]*</script>\s*', '', content, flags=re.DOTALL)
    content = re.sub(r'<script type="text/javascript">\s*_W = _W[^<]*</script>', '', content)
    content = re.sub(r'<script type="text/javascript">_W\.configDomain[^<]*</script>', '', content)
    content = re.sub(r'<script>_W\.relinquish[^<]*</script>\s*', '', content)
    content = re.sub(r'<script type="text/javascript" src="http://cdn2\.editmysite\.com/js/lang/en/stl\.js[^>]*></script>', '', content)
    content = re.sub(r'<script>\s*_W\.themePlugins[^<]*</script>', '', content)
    content = re.sub(r'<script type="text/javascript">\s*_W\.recaptchaUrl[^<]*</script>\s*', '', content)
    
    # 7. Comment out theme plugin scripts at bottom (if not already commented)
    if 'files/theme/plugins.js' in content and '<!-- <script language="javascript" src="files/theme/plugins.js"' not in content:
        content = re.sub(
            r'<script language="javascript" src="files/theme/plugins\.js"></script>',
            '<!-- <script language="javascript" src="files/theme/plugins.js"></script> -->',
            content
        )
    if 'files/theme/custom.js' in content and '<!-- <script language="javascript" src="files/theme/custom.js"' not in content:
        content = re.sub(
            r'<script language="javascript" src="files/theme/custom\.js"></script>',
            '<!-- <script language="javascript" src="files/theme/custom.js"></script> -->',
            content
        )
    if 'files/theme/mobile.js' in content and '<!-- <script language="javascript" src="files/theme/mobile.js"' not in content:
        content = re.sub(
            r'<script language="javascript" src="files/theme/mobile\.js"></script>',
            '<!-- <script language="javascript" src="files/theme/mobile.js"></script> -->',
            content
        )
    
    # 8. Remove customer accounts app (if not already commented)
    if '<div id="customer-accounts-app"></div>' in content and '<!-- <div id="customer-accounts-app"' not in content:
        content = re.sub(r'<div id="customer-accounts-app"></div>\s*', '<!-- <div id="customer-accounts-app"></div> -->\n', content)
    
    # 9. Add mobile menu JavaScript if not already present
    if not has_mobile_js and '</body>' in content:
        mobile_js = '\n<script src="files/mobile-menu.js"></script>\n\n</body>'
        content = content.replace('</body>', mobile_js)
    
    # 10. Remove Store menu item from JavaScript array
    content = re.sub(
        r',?\{"id":"129236209278723622","title":"Store","url":"store\.html"[^}]*\}',
        '',
        content
    )
    
    # 11. Remove Store menu from desktop navigation (with or without comments)
    store_menu_pattern = r'<!--[^>]*-->\s*<li id="pg129236209278723622"[^>]*>.*?</li>\s*<!--[^>]*-->'
    content = re.sub(store_menu_pattern, '<!-- Store menu item removed -->', content, flags=re.DOTALL)
    
    store_menu_pattern2 = r'<li id="pg129236209278723622"[^>]*>.*?</li>'
    content = re.sub(store_menu_pattern2, '<!-- Store menu item removed -->', content, flags=re.DOTALL)
    
    return content

def process_files(input_dir, output_dir):
    """Process all HTML files"""
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Create mobile menu files first
    print("Creating mobile menu files...")
    create_mobile_menu_files(output_dir)
    print("-" * 60)
    
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
    print(f"\n📱 Mobile menu files created:")
    print(f"   - {output_path / 'files' / 'mobile-menu.css'}")
    print(f"   - {output_path / 'files' / 'mobile-menu.js'}")

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
    print("  4. Add mobile menu CSS and JavaScript")
    print("  5. Create mobile-menu.css and mobile-menu.js in files/")
    print("  6. Save cleaned files to 'cleaned_html' folder")
    print()
    
    response = input("Continue? (y/n): ").strip().lower()
    
    if response != 'y':
        print("Cancelled.")
        return
    
    print()
    
    # Process files from current directory, output to cleaned_html
    process_files(current_dir, os.path.join(current_dir, "cleaned_html"))
    
    print("\n✨ Done! Check the 'cleaned_html' folder for your cleaned files.")
    print("📁 Copy the 'files' folder and all HTML files back to your repository.")
    print("🧪 Test the mobile menu by resizing your browser or using a mobile device.")

if __name__ == "__main__":
    main()