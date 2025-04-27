<script lang="ts">
  import { onMount } from 'svelte';
  // custom components
  import MobileSidebar from "./lib/MobileSidebar.svelte";
  import StickyNavbar from "./lib/StickyNavbar.svelte";
  import Date from "./lib/Date.svelte";
  import FooterYear from "./lib/FooterYear.svelte";
  
  let apiKey: string = '';

  onMount(async () => {
    try {
      const res = await fetch('/api/key');
      const data = await res.json();
      apiKey = data.apiKey;
    } catch (error) {
      console.error('Failed to fetch API key:', error);
    }
  });
</script>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The New York Limes</title>
  <link rel="stylesheet" href="app.css">
  <meta name="description" content="Front Page"> <!-- SEO optimization stuff -->
</head>

<body>

<!-- Header: Main title, date, mobile menu toggle -->
<header>
  <!-- Top bar, search, language, login -->
  <div class="top-bar">
    
    <div class="top-bar-left">
      <span>Search</span>
    </div>
    
    <div class="top-bar-center">
      <span><a href=" ">U.S.</a></span>
      <span><a href=" ">International</a></span>
      <span><a href=" ">Canada</a></span>
      <span><a href=" ">Español</a></span>
      <span><a href=" ">中文</a></span>
    </div>
    
    <div id="top-bar-right">
      <button class="login-button">Log In</button>
    </div>
  
  </div>
  <!-- Title bar -->
  <div class="title-bar">
    <div class="title-bar-left">
      <Date />
    </div>
    
    <div class="title-bar-center">
      <h1>The New York Limes</h1>
    </div>
    
    <div id="title-bar-right">
      <!-- placeholder -->
      <span class="market-widget">DOW +1000% ↑</span>
    </div>
  
  </div>
  <!-- Persistent nav bar, sticky, STANDARD -->
  <nav class="main-nav-bar" id="main-nav-bar">
    <!-- Mobile menu button -->
    <StickyNavbar />
  </nav>
  
  <!-- MOBILE NAV MENU -->
  <aside class="mobile-sidebar" id="mobile-sidebar" aria-hidden="true">
    <MobileSidebar />
  </aside>
  
  <!--
  DIMMER:
  div to give JS a marker for applying a darkening of the screen when viewing the mobile menu.
  -->
  <div class="overlay" id="overlay"></div>

</header>

<!--
<main>:
  Contains: articles (<article>) and images (<img>) for the news feed grid
-->
<main id="main-content"> <!-- Articles -->
  <div class="content-grid">
    <section class="content-column" id="column-left">
      <article>
        <h2 class="headline">Breaking: Lime Shortage Sparks Citrus Panic</h2>
        <img src="images/1.png" alt="shortage depiction" class="article-image">
        <p class="author">Zesty Lemonsworth</p>
        <p class="content">Citizens storm supermarkets as lime shelves empty overnight. "Margarita night is in jeopardy!" one frantic shopper exclaims.</p>
      </article>
      <article>
        <h2 class="headline">Exclusive Interview: "Life as a Lime Farmer"</h2>
        <img src="images/2.png" alt="shortage depiction" class="article-image">
        <p class="author">Margarita Limeberg</p>
        <p class="content">Farmer Zest McJuicy reveals: "People don't appreciate the squeeze we face every day."
        </p>
      </article>
      <article>
        <h2 class="headline">Opinion: Is Lime the New Lemon?</h2>
        <img src="images/3.png" alt="shortage depiction" class="article-image">
        <p class="author">Citrus McPeel</p>
        <p class="content">Lemon lobbyists are furious as lime popularity squeezes citrus rivals out of the market.</p>
      </article>
      <article>
        <h2 class="headline">Study Reveals 9 Out of 10 Doctors Recommend More Limes</h2>
        <img src="images/5.png" alt="shortage depiction" class="article-image">
        <p class="author">Dr. Key Limeman</p>
        <p class="content">"Sourness improves your mood," scientists confirm. Skeptics say the study is too zesty to believe.</p>
      </article>
    </section>
    <section class="content-column" id="column-center">
      <article>
        <h2 class="headline">Sports Update: Limetown Limers Win the Citrus Cup</h2>
        <img src="images/6.png" alt="shortage depiction" class="article-image">
        <p class="author">Coach Ricky Rind</p>
        <p class="content">After an intense match, fans chant, "When life gives you limes, make championships."</p>
      </article>
      <article>
        <h2 class="headline">Technology Breakthrough: Smartphone Now Charges Using Limes</h2>
        <img src="images/7.png" alt="shortage depiction" class="article-image">
        <p class="author">Elon Zest</p>
        <p class="content">Tech company CEO proudly announces, "One lime equals ten percent battery life."</p>
      </article>
      <article>
        <h2 class="headline">Travel Guide: Top 5 Lime-Themed Destinations for Summer</h2>
        <img src="images/1.png" alt="shortage depiction" class="article-image"> <!-- Temporary image, need GPT to generate a new image for the story -->
        <p class="author">Clementine Sourwood</p>
        <p class="content">Visit Lime Island, Limetown, or the Limey Alps for a refreshingly sour vacation.</p>
      </article>
      <article>
        <h2 class="headline">Economics: LimeCoin Cryptocurrency Hits Record High</h2>
        <img src="images/8.png" alt="shortage depiction" class="article-image">
        <p class="author">Warren Zuffet</p>
        <p class="content">Investors advise: "Buy low, zest high."</p>
      </article>
    </section>
    <section class="content-column" id="column-right">
      <article>
        <h2 class="headline">Cooking Tips: How to Lime Your Way to Culinary Stardom</h2>
        <img src="images/9.png" alt="shortage depiction" class="article-image">
        <p class="author">Chef Zestina Peelini</p>
        <p class="content">"A lime a day keeps blandness away," celebrity chef advises.</p>
      </article>
      <article>
        <h2 class="headline">Crime Report: Lime Bandits Strike Again</h2>
        <img src="images/1.png" alt="shortage depiction" class="article-image"> <!-- Temporary image, need GPT to generate new image for story -->
        <p class="author">Detective Perry Limecroft</p>
        <p class="content">Thieves apprehended after stealing 1,000 limes from local grocer. Motive: Margarita obsession.</p>
      </article>
      <article>
        <h2 class="headline">Weather Forecast: Heavy Lime Showers Expected</h2>
        <img src="images/12.png" alt="shortage depiction" class="article-image">
        <p class="author">Sunny Citrina</p>
        <p class="content">Meteorologists warn residents to carry cocktail umbrellas at all times.</p>
      </article>
      <article>
        <h2 class="headline">Science: Lime Juice Found on Mars</h2>
        <img src="images/10.png" alt="shortage depiction" class="article-image">
        <p class="author">Neil Zestrong</p>
        <p class="content">NASA confirms, "The red planet is now officially zesty."</p>
      </article>
    </section>
  </div>
</main>


<footer>
  <div class="footer-nav-bar">
    <ul>
      <li><a href=" ">© <FooterYear /> New York Lime, LLC </a></li>
      <li><a href=" ">Terms of Service</a></li>
      <li><a href=" ">Help</a></li>
    </ul>
  </div>


</footer>

</body>

</html>