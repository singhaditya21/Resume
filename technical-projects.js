(() => {
    const search = document.querySelector("[data-tech-search]");
    const count = document.querySelector("[data-tech-count]");
    const grid = document.querySelector("[data-tech-grid]");
    const empty = document.querySelector("[data-tech-empty]");
    const sort = document.querySelector("[data-tech-sort]");
    const clear = document.querySelector("[data-tech-clear]");
    const cards = [...document.querySelectorAll("[data-project-card]")];
    const filters = [...document.querySelectorAll("[data-tech-filter]")];

    if (!grid || cards.length === 0) return;

    const gridId = grid.id || "technical-project-grid";
    grid.id = gridId;
    grid.setAttribute("aria-label", "Technical projects");
    search?.setAttribute("aria-controls", gridId);
    sort?.setAttribute("aria-controls", gridId);
    clear?.setAttribute("aria-controls", gridId);
    filters.forEach((button) => button.setAttribute("aria-controls", gridId));
    cards.forEach((card, index) => {
        card.dataset.featuredOrder = String(index);
    });

    if (count) {
        count.setAttribute("role", "status");
        count.setAttribute("aria-live", "polite");
        count.setAttribute("aria-atomic", "true");
    }

    const availableCategories = new Set(filters.map((button) => button.dataset.techFilter));
    const initialParams = new URLSearchParams(window.location.search);
    const requestedCategory = initialParams.get("category") || "all";
    let activeCategory = availableCategories.has(requestedCategory) ? requestedCategory : "all";

    if (search) search.value = initialParams.get("q") || "";
    if (sort) sort.value = initialParams.get("sort") === "az" ? "az" : "featured";

    function normalized(value) {
        return value.trim().toLocaleLowerCase();
    }

    function updateUrl() {
        const url = new URL(window.location.href);
        const query = search?.value.trim() || "";

        if (query) url.searchParams.set("q", query);
        else url.searchParams.delete("q");

        if (activeCategory !== "all") url.searchParams.set("category", activeCategory);
        else url.searchParams.delete("category");

        if (sort?.value === "az") url.searchParams.set("sort", "az");
        else url.searchParams.delete("sort");

        window.history.replaceState(null, "", `${url.pathname}${url.search}${url.hash}`);
    }

    function render({ updateHistory = true } = {}) {
        const query = normalized(search?.value || "");
        let visible = 0;

        const orderedCards = [...cards].sort((left, right) => {
            if (sort?.value === "az") {
                return (left.dataset.name || "").localeCompare(right.dataset.name || "");
            }
            return Number(left.dataset.featuredOrder) - Number(right.dataset.featuredOrder);
        });
        orderedCards.forEach((card) => grid.append(card));

        cards.forEach((card) => {
            const categoryMatches = activeCategory === "all" || card.dataset.category === activeCategory;
            const searchMatches = !query || normalized(card.dataset.search || card.textContent || "").includes(query);
            const show = categoryMatches && searchMatches;
            card.hidden = !show;
            if (show) visible += 1;
        });

        filters.forEach((button) => {
            const active = button.dataset.techFilter === activeCategory;
            button.classList.toggle("is-active", active);
            button.setAttribute("aria-pressed", String(active));
        });

        if (count) count.textContent = `${visible} ${visible === 1 ? "project" : "projects"}`;
        if (empty) empty.hidden = visible !== 0;
        if (clear) clear.disabled = !query && activeCategory === "all" && sort?.value !== "az";
        if (updateHistory) updateUrl();
    }

    filters.forEach((button) => {
        button.addEventListener("click", () => {
            activeCategory = button.dataset.techFilter || "all";
            render();
        });
    });

    search?.addEventListener("input", () => render());
    sort?.addEventListener("change", () => render());
    clear?.addEventListener("click", () => {
        if (search) search.value = "";
        if (sort) sort.value = "featured";
        activeCategory = "all";
        render();
        search?.focus();
    });
    search?.addEventListener("keydown", (event) => {
        if (event.key !== "Escape" || !search.value) return;
        search.value = "";
        render();
    });

    window.addEventListener("popstate", () => {
        const params = new URLSearchParams(window.location.search);
        const category = params.get("category") || "all";
        activeCategory = availableCategories.has(category) ? category : "all";
        if (search) search.value = params.get("q") || "";
        if (sort) sort.value = params.get("sort") === "az" ? "az" : "featured";
        render({ updateHistory: false });
    });

    render({ updateHistory: false });
})();
