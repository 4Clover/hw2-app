<script lang="ts">
    const dateElement = document.getElementById('current-date');
    if (dateElement) {
        const today : Date = new Date();
        const dateFormat = new Intl.DateTimeFormat("en-US", {
            weekday: "long",
            year: "numeric",
            month: "long",
            day: "numeric"
        });
        dateElement.textContent = dateFormat.format(today);
    }
</script>

<span id="current-date">Loading Date...</span>