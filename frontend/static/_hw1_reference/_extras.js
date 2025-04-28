document.addEventListener('DOMContentLoaded', () => { // runs scripts following full DOM load

    // ------------------------ Update Date -------------------------- //
    const dateElement = document.getElementById('current-date');
    if (dateElement) {
        const today = new Date();
        const options = {weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'};
        dateElement.textContent = today.toLocaleDateString('en-US', options);
    }
    // ---------------------------------------------------------------- //


    // --------------------- Update Footer Year ----------------------- //
    const yearElement = document.getElementById('current-year');
    if (yearElement) {
        const currentYear = new Date().getFullYear();
        yearElement.textContent = currentYear.toString();
    }
    // ---------------------------------------------------------------- //


    // -------------------- Toggle Sidebar (mobile) ------------------- //
    const menuToggle = document.getElementById('nav-toggle'); // hamburger menu (mobile)
    const sidebar = document.getElementById('mobile-sidebar'); // sidebar
    const closeBtn = document.getElementById('close-mobile-sidebar'); // sidebar close button
    const overlay = document.getElementById('overlay'); // dimmer

    if (menuToggle && sidebar && closeBtn && overlay) { // element existence check

        const openSidebar = () => {
            sidebar.classList.add('open'); // update state for sidebar
            overlay.classList.add('active'); // update state for overlay
            // Accessibility
            menuToggle.setAttribute('aria-expanded', 'true'); // ARIA update
            sidebar.setAttribute('aria-hidden', 'false'); // ARIA update
        };

        const closeSidebar = () => {
            sidebar.classList.remove('open'); // update state for sidebar
            overlay.classList.remove('active'); // update state for overlay
            // Accessibility
            menuToggle.setAttribute('aria-expanded', 'false'); // ARIA update
            sidebar.setAttribute('aria-hidden', 'true'); // ARIA update
        };

        // event listeners
        menuToggle.addEventListener('click', openSidebar); // listener for open sidebar event
        // listeners for close sidebar event
        closeBtn.addEventListener('click', closeSidebar);
        overlay.addEventListener('click', closeSidebar);

    } else {
        // error message for missing elements
        console.warn("Error: Sidebar functionality disabled check sidebar elements.");
    }
    // ------------------------------------------------------------------ //


    // -------------------------- Sticky Navbar ------------------------- //
    const mainNav = document.getElementById('main-nav-bar');
    const mainContent = document.querySelector('main'); // padding if needed

    if (mainNav && mainContent) { // element existence check
        // variables
        const stickyPoint = mainNav.offsetTop; // main box offset
        const navHeight = mainNav.offsetHeight; // nav box height

        /* Scroll Handler:
                Initiates a change of position for the homepage navbar from static to fixed.
                Adds and removes sticky class from mainNav based on scroll distance from top.
                Adds and removes sticky-nav-active class from document ''.
                Updates document padding to reflect persistent navbar.
        */
        const handleScroll = () => {
            if (window.scrollY > stickyPoint) { // init position check
                // fixes position to top of window
                mainNav.classList.add('sticky');
                // updates state for use elsewhere
                document.body.classList.add('sticky-nav-active');
                // padding for proper visual effect, fixes jumping of content on change of nav
                document.body.style.paddingTop = `${navHeight}px`;

            } else {
                // reset position
                mainNav.classList.remove('sticky');
                // update state
                document.body.classList.remove('sticky-nav-active');
                // reset padding
                document.body.style.paddingTop = '0px';
            }
        };

        window.addEventListener('scroll', handleScroll); // triggers handleScroll() on mouse scroll event

    } else {
        console.warn("Error: Sticky navigation disabled, check nav bar elements."); // error message for missing nav elements
    }
    // ------------------------------------------------------------------ //

    // TODO: Market Widget, Search

});