<script lang="ts">
    const yearElement : HTMLElement | null = document.getElementById('current-year');
    if (yearElement) {
        const currentYear : number = new Date().getFullYear();
        yearElement.textContent = currentYear.toString();
    }
</script>

<span id="current-year"></span>