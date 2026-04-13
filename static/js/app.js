// app.js
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('app-sidebar');
    const logoToggle = document.getElementById('logo-toggle');
    const navTexts = document.querySelectorAll('.nav-text');

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
});
