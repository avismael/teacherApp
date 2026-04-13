// app.js
document.addEventListener('DOMContentLoaded', () => {
    // Menu mobile toggle logic
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenuClose = document.getElementById('mobile-menu-close');
    const mobileMenuDrawer = document.getElementById('mobile-menu-drawer');
    const mobileMenuBackdrop = document.getElementById('mobile-menu-backdrop');

    function openMobileMenu() {
        if (!mobileMenuDrawer || !mobileMenuBackdrop) return;
        
        mobileMenuBackdrop.classList.remove('hidden');
        // Small delay to allow CSS transitions to trigger
        requestAnimationFrame(() => {
            mobileMenuBackdrop.classList.remove('opacity-0');
            mobileMenuBackdrop.classList.add('opacity-100');
            mobileMenuDrawer.classList.remove('-translate-x-full');
            mobileMenuDrawer.classList.add('translate-x-0');
        });
        document.body.classList.add('overflow-hidden');
    }

    function closeMobileMenu() {
        if (!mobileMenuDrawer || !mobileMenuBackdrop) return;

        mobileMenuBackdrop.classList.remove('opacity-100');
        mobileMenuBackdrop.classList.add('opacity-0');
        mobileMenuDrawer.classList.remove('translate-x-0');
        mobileMenuDrawer.classList.add('-translate-x-full');
        
        // Wait for transition to finish before hiding
        setTimeout(() => {
            if (mobileMenuDrawer.classList.contains('-translate-x-full')) {
                mobileMenuBackdrop.classList.add('hidden');
            }
        }, 300);
        document.body.classList.remove('overflow-hidden');
    }

    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', openMobileMenu);
    }

    if (mobileMenuClose) {
        mobileMenuClose.addEventListener('click', closeMobileMenu);
    }

    if (mobileMenuBackdrop) {
        mobileMenuBackdrop.addEventListener('click', closeMobileMenu);
    }

    // Handle Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && mobileMenuDrawer && !mobileMenuDrawer.classList.contains('-translate-x-full')) {
            closeMobileMenu();
        }
    });

    // Close menu when window is resized to desktop width
    window.addEventListener('resize', () => {
        if (window.innerWidth >= 768 && mobileMenuDrawer && !mobileMenuDrawer.classList.contains('-translate-x-full')) {
            closeMobileMenu();
        }
    });
});
