<script lang="ts" >
    import {onMount} from 'svelte'; // function to activate on component mount to the DOM
    import {BROWSER} from 'esm-env'; // sveltekit environment variable, used to check if user is in the browser or not
    import '../app.css'; // global CSS file
    export const ssr = false; // fixes a build error since sveltekit is meant to be server-side rendered, not statically generated/served
    
	interface Article { // format of the data received from the backend
		id: number,
        headline: string,
        author: string,
        content: string,
        imageUrl: string,
        articleUrl: string
	}
	
	// nav bar and footer related states
	let currentDate: string = 'Loading Date...';
	let currentYear: string = new Date().getFullYear().toString();
	let isSidebarOpen: boolean = false;
	let isSticky: boolean = false;
 
	// article related vars
    let articles: Article[] = [];
    let isLoadingArticles: boolean = true;
    let articlesError: string | null = null;
	
    // nav bar related vars
	let mainNavElement: HTMLElement | null = null; // nav bar reference'
    let hamburgerElement: HTMLElement | null = null;
	let navHeight: number = 0;
	let stickyPoint: number = 0; // calculated on mount
	
	// column calculations -- change as formatting is changed -- $ indicates performed @ onMount()
	$: columnCount = 3;
    $: articlesPerColumn = Math.ceil(articles.length / columnCount);
    $: col1Articles = articles.slice(0, articlesPerColumn);
    $: col2Articles = articles.slice(articlesPerColumn, articlesPerColumn * 2);
    $: col3Articles = articles.slice(articlesPerColumn * 2, articles.length);
    
    // --- visual state change functions ---
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
    // --- end of visual state change functions ---
    
    
    // changed to only a state change handler, rather than updating calculations
	// I beleive this is more efficent given calculations are done on mount
	function handleScroll() {
        if (!mainNavElement) return; // nav bar existence check
        if (window.scrollY > stickyPoint) {
            if (!isSticky) {
                isSticky = true
	            hamburgerElement.offsetLeft ? : 10px; ########################################################
            }
        } else {
            if (isSticky) isSticky = false;
        }
    }
    
    // populates articles dict via fetch
	async function fetchArticles() {
        isLoadingArticles = true;
        articlesError = null;
        let fake_articles : Boolean = false; // true if testing
        try {
            const [response] = await Promise.all([fetch((fake_articles ? '/api/test_articles': '/api/search'))]); // Promise.all() will be used to eventually fetch multiple NYT pages
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`); // error handling
            }
            articles = await response.json(); // parse response as JSON
            console.log("Fetched articles:", articles); // log articles to console for debugging
        } catch (e: any) {
            console.error("Failed to fetch articles:", e);
            articlesError = e.message || "Unknown error loading articles";
            articles = [];
        } finally {
            isLoadingArticles = false;
        }
    }
 
	onMount(() => {
        if (!BROWSER) return; // check for non-browser environment i.e. code outside of browser
        updateDate();
        fetchArticles();
        // build sticky nav -- TODO: Update for better mobile viewing
        if (mainNavElement) {
            // get initial values after render
            stickyPoint = mainNavElement.offsetTop;
            navHeight = mainNavElement.offsetHeight;
            if (navHeight > 0) {
                window.addEventListener('scroll', handleScroll);
                console.log(`Sticky nav initialized. Height: ${navHeight}px, Sticky Point: ${stickyPoint}px`);
            } else {
                console.warn("Sticky navigation disabled: Nav element height is 0.");
            }

            // clean up the scroll listener after component is destroyed
            return () => {
                if (mainNavElement && navHeight > 0) {
                    window.removeEventListener('scroll', handleScroll);
                }
            };
        }
    })
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
			bind:this={hamburgerElement}
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
	<div class="overlay" class:active={isSidebarOpen} aria-label="Close navigation menu"></div>
	
	
</header>

<!-- Body -->
<!-- Updated in-layout version of articles -->
<div class="main-content-area">
		<main id="main-content">
				{#if isLoadingArticles}
						<p>Loading Articles...</p>
				{:else if articlesError}
						<p style ="color: red;">Error Loading Articles: {articlesError}</p>
				{:else if articles.length === 0}
						<p>No articles were found.</p>
				{:else}
						<div class="content-grid">
								<section class="content-column" id="column-left">
										{#each col1Articles as article (article.id)}
												<article>
														<h2 class="headline">{article.headline}</h2>
														{#if article.imageUrl}
																<img src={article.imageUrl} alt={article.headline} class="article-image">
														{/if}
														<p class="author">{article.author}</p>
														<p class="content">{article.content}</p>
												</article>
										{/each}
								</section>
								<section class="content-column" id="column-left">
										{#each col2Articles as article (article.id)}
												<article>
														<h2 class="headline">{article.headline}</h2>
														{#if article.imageUrl}
																<img src={article.imageUrl} alt={article.headline} class="article-image">
														{/if}
														<p class="author">{article.author}</p>
														<p class="content">{article.content}</p>
												</article>
										{/each}
								</section>
								<section class="content-column" id="column-left">
										{#each col3Articles as article (article.id)}
												<article>
														<h2 class="headline">{article.headline}</h2>
														{#if article.imageUrl}
																<img src={article.imageUrl} alt={article.headline} class="article-image">
														{/if}
														<p class="author">{article.author}</p>
														<p class="content">{article.content}</p>
												</article>
										{/each}
								</section>
						</div>
				{/if}
		</main>
</div>

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