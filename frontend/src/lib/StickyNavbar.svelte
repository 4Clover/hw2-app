<script lang="ts">
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
</script>

<button class="nav-toggle"
        id="nav-toggle"
        aria-label="Open navigation menu"
        aria-expanded="false"
        aria-controls="mobile-sidebar">
		☰
</button>
<!-- Navigation links -->
<ul>
		<li><a href="#">U.S.</a></li>
		<li><a href="#">World</a></li>
		<li><a href="#">Business</a></li>
		<li><a href="#">Arts</a></li>
		<li><a href="#">Lifestyle</a></li>
		<li><a href="#">Opinion</a></li>
		<li class="main-nav-bar-divider">|</li>
		<li><a href="#">Audio</a></li>
		<li><a href="#">Games</a></li>
		<li><a href="#">Cooking</a></li>
		<li><a href="#">Wirecutter</a></li>
		<li><a href="#">The Athletic</a></li>
</ul>