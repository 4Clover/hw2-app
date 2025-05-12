<script lang="ts" >
    import {onMount, onDestroy} from 'svelte'; // function to activate on component mount to the DOM
    import {BROWSER} from 'esm-env'; // sveltekit environment variable, used to check if user is in the browser or not
    import '../app.css'; // global CSS file
    export const ssr = false; // fixes a build error since sveltekit is meant to be server-side rendered, not statically generated/served
    
    interface Article { // format of the data received from the backend
        id: number,
        headline: string,
        author: string,
        content: string,
        imageUrl: string | null,
        articleUrl: string
    }

    const THROTTLE_DELAY = 1000; // milliseconds (1 second) - adjust as needed
    
    // nav bar and footer related states
    let currentDate: string = 'Loading Date...';
    let currentYear: string = new Date().getFullYear().toString();
    let isSidebarOpen: boolean = false;
    let isSticky: boolean = false;

    // article related vars
    let articles: Article[] = [];
    let articlesError: string | null = null;
    let fake_articles : boolean = false; // true if testing
    // infinite scroll
    let isLoadingInitArticles: boolean = true;
    let isLoadingMoreArticles: boolean = false;
    let currentPage: number = 0;
    let hasMoreArticles: boolean = true;
    let infinitePointElement: HTMLDivElement | null = null;
    let observer: IntersectionObserver | null = null;
    let observerInitialized: boolean = false;
    let isThrottled: boolean = false;
    let throttleTimeoutId: ReturnType<typeof setTimeout> | null = null;
    
    // nav bar related vars
    let mainNavElement: HTMLElement | null = null; // nav bar reference
    let navHeight: number = 0;
    let stickyPoint: number = 0; // calculated on mount

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
    function handleStickyNavScroll() {
        if (!mainNavElement || !BROWSER) return;
        if (window.scrollY > stickyPoint) {
            if (!isSticky) isSticky = true;
        } else {
            if (isSticky) isSticky = false;
        }
    }


    async function fetchArticlesPage(pageToFetch: number) {
        // loading state based on page number
        if (pageToFetch === 0) {
            isLoadingInitArticles = true;
        } else {
            if (isLoadingMoreArticles) {
                console.warn(`Fetch attempt for page ${pageToFetch} blocked by concurrent loading.`);
                return;
            }
            isLoadingMoreArticles = true; // loading state for pages
        }
        articlesError = null;
		
        // basic search
        const query = 'sacramento';
        const begin = '20230401';
        const filter = 'timesTags.location.includes=california';
        const baseUrl = fake_articles ? '/api/test_articles' : '/api/search';
        const apiUrl = fake_articles
            ? baseUrl
            : `${baseUrl}?query=${encodeURIComponent(query)}&begin_date=${begin}&filter=${encodeURIComponent(filter)}&page=${pageToFetch}`;

        try {
            // http check
            console.log(`Fetching page: ${pageToFetch} from ${apiUrl}`);
            const response = await fetch(apiUrl);
            if (!response.ok) {
                let errorBody = `HTTP error! status: ${response.status}`;
                try {
                    const errorJson = await response.json();
                    if (errorJson?.error) errorBody += ` - ${errorJson.error}`;
                    else if (errorJson?.message) errorBody += ` - ${errorJson.message}`;
                } catch { /* ignore */ }
                throw new Error(errorBody);
            }
            const newArticlesData = await response.json();
			
            
            // lots of error checking -------------
            if (!Array.isArray(newArticlesData)) {
                if (typeof newArticlesData === 'object' && newArticlesData?.error) {
                    throw new Error(`API Error: ${newArticlesData.error}`);
                }
                console.error("Unexpected API response format:", newArticlesData);
                throw new Error("Unexpected data format received from API.");
            }
            const newArticles: Article[] = newArticlesData;
            console.log(`Fetched ${newArticles.length} articles for page ${pageToFetch}.`);

            if (newArticles.length === 0 && pageToFetch > 0) {
                hasMoreArticles = false;
                console.log("No more articles found.");
            } else if (newArticles.length > 0) {
                const currentIds = new Set(articles.map(a => a.id));
                const uniqueNewArticles = newArticles.filter(a => a?.id && !currentIds.has(a.id));
                articles = [...articles, ...uniqueNewArticles];

                if (!fake_articles && newArticles.length < 10 && pageToFetch > 0) {
                    hasMoreArticles = false;
                    console.log("Assuming no more articles based on count < 10.");
                }
            } else if (pageToFetch === 0 && newArticles.length === 0) {
                console.log("No articles found on initial fetch.");
            }

        } catch (e: any) {
            console.error(`Failed to fetch articles for page ${pageToFetch}:`, e);
            articlesError = e.message || `Unknown error loading articles (page ${pageToFetch})`;
        } finally {
            isLoadingInitArticles = false;
            isLoadingMoreArticles = false;
        } // stop!!
    }

    // --- Intersection Observer Callback ---
    function onIntersection(entries: IntersectionObserverEntry[]) {
        const entry = entries[0];
        if (entry.isIntersecting && hasMoreArticles && !isLoadingMoreArticles && !isLoadingInitArticles && !isThrottled) {
            console.log('Watcher visible AND not throttled, loading next page...');

            // --- throttle BEFORE fetch ---
            isThrottled = true;
            console.log(`Throttling activated. Cooldown: ${THROTTLE_DELAY}ms`);

            currentPage++;
            fetchArticlesPage(currentPage); // fetch the next page

            // --- timeout to release throttle ---
            if (throttleTimeoutId) clearTimeout(throttleTimeoutId);
            throttleTimeoutId = setTimeout(() => {
                isThrottled = false;
                console.log('Throttle released.');
            }, THROTTLE_DELAY);

        } else if (entry.isIntersecting) {
            console.log('Watcher visible but not loading:', { hasMoreArticles, isLoadingMoreArticles, isLoadingInitArticles, isThrottled });
        }
    }

    
    // load everything
    onMount(() => {
        if (!BROWSER) return;
        updateDate();
        fetchArticlesPage(currentPage);

        // sticky Nav Setup
        if (mainNavElement) {
            stickyPoint = mainNavElement.offsetTop;
            navHeight = mainNavElement.offsetHeight;
            if (navHeight > 0) {
                window.addEventListener('scroll', handleStickyNavScroll);
                console.log(`Sticky nav initialized. Height: ${navHeight}px, Sticky Point: ${stickyPoint}px`);
            } else {
                console.warn('Sticky navigation disabled: Nav element height is 0.');
            }
        }
    });

    $: if (BROWSER && !isLoadingInitArticles && infinitePointElement && !observerInitialized && hasMoreArticles) {
        console.log("Conditions met, setting up Intersection Observer...");
        observer = new IntersectionObserver(onIntersection, {
            rootMargin: '200px' // adjust rootMargin if needed
        });
        observer.observe(infinitePointElement);
        observerInitialized = true;
        console.log("Intersection Observer is set up reactively.");
    } else if (BROWSER && observerInitialized && !hasMoreArticles && observer) {
        console.log("No more articles expected, disconnecting observer.");
        observer.disconnect();
        observer = null;
        observerInitialized = false;
    }


    // --- cleanup ---
    onDestroy(() => {
        if (observer) {
            observer.disconnect();
            console.log("Intersection Observer disconnected on component destroy.");
        }
        if (throttleTimeoutId) {
            clearTimeout(throttleTimeoutId);
            console.log("Throttle timeout cleared on component destroy.");
        }
        if (mainNavElement && navHeight > 0 && BROWSER) {
            window.removeEventListener('scroll', handleStickyNavScroll);
            console.log("Sticky nav scroll listener removed.");
        }
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
						<h1>The New York Times</h1>
				</div>
				<div id="title-bar-right">
						<span class="market-widget">DOW +1000% ↑</span>
				</div>
		</div>
		<!-- Persistent nav bar -->
		<nav class="main-nav-bar" class:isSticky bind:this={mainNavElement}>
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
		<div class="overlay" class:active={isSidebarOpen} aria-label="Close navigation menu"></div>


</header>

<!-- Body -->
<div class="main-content-area">
		<main id="main-content">
				{#if isLoadingInitArticles}
						<!-- Show initial loading message -->
						<p>Loading Articles...</p>
				{:else if articlesError && articles.length === 0}
						<!-- Show error only if no articles were loaded -->
						<p style="color: red;">Error Loading Articles: {articlesError}</p>
				{:else if articles.length === 0 && !isLoadingInitArticles}
						<!-- Show no articles message only after initial load -->
						<p>No articles were found.</p>
				{:else}
						<!-- Display articles in the grid -->
						<div class="content-grid">
								{#each articles as article (article.id)}
										<article>
												<a href={article.articleUrl} target="_blank" rel="noopener noreferrer">
														<h2 class="headline">{article.headline}</h2>
												</a>
												{#if article.imageUrl}
														<img
																src={article.imageUrl.startsWith('http') ? article.imageUrl : `https://www.nytimes.com/${article.imageUrl}`}
																alt={article.headline}
																class="article-image"
														/>
												{/if}
												<p class="author">{article.author}</p>
												<p class="content">{article.content}</p>
										</article>
								{/each}
						</div>
						
						<!-- Loading indicator -->
						{#if isLoadingMoreArticles}
								<p style="text-align: center; padding: 20px;">Loading more articles...</p>
						{/if}
						
						<!-- "End of results" message -->
						{#if !hasMoreArticles && articles.length > 0}
								<p style="text-align: center; padding: 20px; color: #666;">You've reached the end of the articles.</p>
						{/if}
						
						<!-- Error message if shown alongside existing articles -->
						{#if articlesError && articles.length > 0}
								<p style="text-align: center; padding: 20px; color: red;">Error loading more articles: {articlesError}</p>
						{/if}
						
						<!-- Element for Watcher -->
						{#if hasMoreArticles}
								<div bind:this={infinitePointElement} style="height: 10px;"></div>
						{/if}
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