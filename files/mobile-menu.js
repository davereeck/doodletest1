// Mobile menu toggle functionality
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
