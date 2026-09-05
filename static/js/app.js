// app.js
document.addEventListener('DOMContentLoaded', () => {
    const themeStorageKey = 'teacherapp-theme';
    const sidebar = document.getElementById('app-sidebar');
    const logoToggle = document.getElementById('logo-toggle');
    const navTexts = document.querySelectorAll('.nav-text');
    const themeButtons = document.querySelectorAll('#theme-toggle-desktop, #theme-toggle-mobile');

    function applyTheme(theme) {
        const isDark = theme === 'dark';
        document.documentElement.classList.toggle('dark', isDark);
        document.documentElement.style.colorScheme = theme;
        localStorage.setItem(themeStorageKey, theme);

        themeButtons.forEach((button) => {
            const moon = button.querySelector('[data-theme-icon="moon"]');
            const sun = button.querySelector('[data-theme-icon="sun"]');
            if (moon && sun) {
                moon.classList.toggle('hidden', isDark);
                sun.classList.toggle('hidden', !isDark);
            }
            button.setAttribute('aria-label', isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro');
        });
    }

    function getInitialTheme() {
        const stored = localStorage.getItem(themeStorageKey);
        if (stored === 'dark' || stored === 'light') return stored;
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    applyTheme(getInitialTheme());

    let isExpanded = window.innerWidth >= 1024;

    function renderSidebar() {
        if (!sidebar) return;
        
        // Transiciones fijas para evitar cortes raros al mutar estilos online
        sidebar.style.transition = 'width 300ms ease-in-out';
        navTexts.forEach(el => el.style.transition = 'opacity 300ms ease-in-out');

        if (isExpanded) {
            sidebar.style.width = '16rem'; // w-64
            sidebar.classList.add('shadow-2xl');
            logoToggle.classList.add('expanded');
            
            navTexts.forEach(el => {
                el.style.opacity = '1';
                el.style.visibility = 'visible';
            });
        } else {
            sidebar.style.width = '5rem'; // w-20
            sidebar.classList.remove('shadow-2xl');
            logoToggle.classList.remove('expanded');
            
            navTexts.forEach(el => {
                el.style.opacity = '0';
                setTimeout(() => { if (!isExpanded) el.style.visibility = 'hidden'; }, 300);
            });
        }
    }

    if (logoToggle) {
        logoToggle.addEventListener('click', () => {
            isExpanded = !isExpanded;
            renderSidebar();
        });
    }

    themeButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const nextTheme = document.documentElement.classList.contains('dark') ? 'light' : 'dark';
            applyTheme(nextTheme);
        });
    });

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (event) => {
        if (!localStorage.getItem(themeStorageKey)) {
            applyTheme(event.matches ? 'dark' : 'light');
        }
    });

    // Auto colapsar en móviles al tocar cualquier lado oscuro de fuera
    document.addEventListener('click', (e) => {
        if (window.innerWidth < 1024 && isExpanded && sidebar) {
            if (!sidebar.contains(e.target)) {
                isExpanded = false;
                renderSidebar();
            }
        }
    });

    // Restaurar control a tailwind al rotar el celular o crecer pantalla
    window.addEventListener('resize', () => {
        const desktop = window.innerWidth >= 1024;
        if (desktop && !isExpanded && sidebar.style.width === '5rem') {
            isExpanded = true;
            // Limpia los inlines styles para que lg:w-64 del html fluya
            sidebar.style.width = '';
            navTexts.forEach(el => { el.style.opacity = ''; el.style.visibility = ''; });
        } else if (!desktop && isExpanded) {
            isExpanded = false;
            renderSidebar();
        }
    });

    // MOBILE MENU OVERLAY LOGIC
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenuClose = document.getElementById('mobile-menu-close');
    const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');

    if (mobileMenuBtn && mobileMenuOverlay) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenuOverlay.classList.remove('hidden');
            // Timeout para permitir que el navegador registre la eliminación de 'hidden' antes de animar
            setTimeout(() => {
                mobileMenuOverlay.classList.remove('opacity-0', 'pointer-events-none', '-translate-y-8', 'invisible');
                mobileMenuOverlay.classList.add('opacity-100', 'pointer-events-auto', 'translate-y-0', 'visible');
            }, 10);
            document.body.style.overflow = 'hidden'; 
        });
    }

    function closeMobileMenu() {
        if (!mobileMenuOverlay) return;
        mobileMenuOverlay.classList.add('opacity-0', 'pointer-events-none', '-translate-y-8', 'invisible');
        mobileMenuOverlay.classList.remove('opacity-100', 'pointer-events-auto', 'translate-y-0', 'visible');
        document.body.style.overflow = ''; 
        // Esperar a que termine la animación antes de poner hidden
        setTimeout(() => {
            if (mobileMenuOverlay.classList.contains('opacity-0')) {
                mobileMenuOverlay.classList.add('hidden');
            }
        }, 300);
    }

    if (mobileMenuClose) {
        mobileMenuClose.addEventListener('click', closeMobileMenu);
    }

    // Cerrar al tocar un link
    mobileNavLinks.forEach(link => {
        link.addEventListener('click', closeMobileMenu);
    });
});
