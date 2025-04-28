<script lang="ts">
	import { onMount } from 'svelte';
	import '../app.css'; // global CSS file
    export const ssr = false; // fixes a build error since sveltekit is meant to be server-side rendered, not statically generated/served
    
	let currentDate: string = 'Loading Date...';
	let currentYear: string = new Date().getFullYear().toString();
	let isSidebarOpen: boolean = false;
	let isSticky: boolean = false;

	let mainNavElement: HTMLElement | null = null; // nav bar reference
	let navHeight: number = 0;
	let stickyPoint: number = 0;

	function updateDate() {
		const today = new Date();
		const options: Intl.DateTimeFormatOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
		currentDate = today.toLocaleDateString('en-US', options);
	}

	function openSidebar() {
		isSidebarOpen = true; // possibly add overlay-related code here
	}

	function closeSidebar() {
		isSidebarOpen = false; // ''                                 ''
	}

	function handleScroll() {
		if (!mainNavElement) return; // nav bar existence check
		
		// recalculation of nav bar height on resize to ensure it's correct
		stickyPoint = mainNavElement.offsetTop;

		if (window.scrollY > stickyPoint) { // scroll check for if window is past the normal nav location
			if (!isSticky) { // if the nav is not sticky on scroll check
				isSticky = true;
				// Apply padding directly to body - Note: Less idiomatic Svelte, but mimics original JS.
				// A wrapper div around <slot /> might be a more Svelte-native way.
				document.body.style.paddingTop = `${navHeight}px`;
				document.body.classList.add('sticky-nav-active'); // Optional: if CSS uses this class
			}
		} else {
			if (isSticky) { // Check if state needs changing
				isSticky = false;
				document.body.style.paddingTop = '0px';
				document.body.classList.remove('sticky-nav-active'); // Optional: if CSS uses this class
			}
		}
	}

	onMount(() => {
		updateDate();

		// Sticky Nav Setup
		if (mainNavElement) {
			// get initial values after render
			stickyPoint = mainNavElement.offsetTop;
			navHeight = mainNavElement.offsetHeight;
			window.addEventListener('scroll', handleScroll);
		} else {
			console.warn("Error: Sticky navigation disabled, nav bar element not found.");
		}

		// clean up the scroll listener after component is destroyed
		return () => {
			window.removeEventListener('scroll', handleScroll);
			// if the component is removed while still sticky, reset states and padding
			if (isSticky) {
				document.body.style.paddingTop = '0px';
				document.body.classList.remove('sticky-nav-active');
			}
		};
	});

</script>

<!-- Header -->
<header>
	<!-- Top bar -->
	<div class="top-bar">
		<div class="top-bar-left">
			<span>Search</span>
		</div>
		<div class="top-bar-center">
			<span><a href="# ">U.S.</a></span>
			<span><a href="# ">International</a></span>
			<span><a href="# ">Canada</a></span>
			<span><a href="# ">Español</a></span>
			<span><a href="# ">中文</a></span>
		</div>
		<div id="top-bar-right">
			<button class="login-button">Log In</button>
		</div>
	</div>
	<!-- Title bar -->
	<div class="title-bar">
		<div class="title-bar-left">
			<span id="current-date">{currentDate}</span>
		</div>
		<div class="title-bar-center">
			<h1>The New York Limes</h1>
		</div>
		<div id="title-bar-right">
			<span class="market-widget">DOW +1000% ↑</span>
		</div>
	</div>
	<!-- Persistent nav bar -->
	<nav class="main-nav-bar" class:sticky={isSticky} bind:this={mainNavElement}>
		<!-- Mobile menu button -->
		<button
			class="nav-toggle"
			aria-label="Open navigation menu"
			aria-expanded={isSidebarOpen}
			aria-controls="mobile-sidebar"
			on:click={openSidebar}
		>
			☰
		</button>
		<!-- Navigation links -->
		<ul>
			<li><a href="# ">U.S.</a></li>
			<li><a href="# ">World</a></li>
			<li><a href="# ">Business</a></li>
			<li><a href="# ">Arts</a></li>
			<li><a href="# ">Lifestyle</a></li>
			<li><a href="# ">Opinion</a></li>
			<li class="main-nav-bar-divider">|</li>
			<li><a href="# ">Audio</a></li>
			<li><a href="# ">Games</a></li>
			<li><a href="# ">Cooking</a></li>
			<li><a href="# " >Wirecutter</a></li>
			<li><a href="# ">The Athletic</a></li>
		</ul>
	</nav>
	
	<!-- MOBILE NAV MENU -->
	<aside class="mobile-sidebar" class:open={isSidebarOpen} id="mobile-sidebar" aria-hidden={!isSidebarOpen}>
		<button class="close-mobile-sidebar" aria-label="Close navigation menu" on:click={closeSidebar}>x</button>
		<ul>
			<li><a href="# " on:click={closeSidebar}>U.S.</a></li>
			<li><a href="# " on:click={closeSidebar}>World</a></li>
			<li><a href="# " on:click={closeSidebar}>Business</a></li>
			<li><a href="# " on:click={closeSidebar}>Arts</a></li>
			<li><a href="# " on:click={closeSidebar}>Lifestyle</a></li>
			<li><a href="# " on:click={closeSidebar}>Opinion</a></li>
			<li class="mobile-divider"></li>
			<li><a href="# " on:click={closeSidebar}>Audio</a></li>
			<li><a href="# " on:click={closeSidebar}>Games</a></li>
			<li><a href="# " on:click={closeSidebar}>Cooking</a></li>
			<li><a href="# " on:click={closeSidebar}>Wirecutter</a></li>
			<li><a href="# " on:click={closeSidebar}>The Athletic</a></li>
			<li class="mobile-divider"></li>
			<li><a href="# " on:click={closeSidebar}>Search</a></li>
			<li><a href="# " on:click={closeSidebar}>Log In</a></li>
		</ul>
	</aside>
	<!-- DIMMER -->
	<div class="overlay" class:active={isSidebarOpen}></div>
	
	
</header>

<!-- This is where the content from +page.svelte will be inserted -->
<div class="main-content-area"><slot /></div>

<!-- Footer -->
<footer>
	<div class="footer-nav-bar">
		<ul>
			<li><a href="# ">© <span id="current-year">{currentYear}</span> New York Lime, LLC </a></li>
			<li><a href="# ">Terms of Service</a></li>
			<li><a href="# ">Help</a></li>
		</ul>
	</div>
</footer>