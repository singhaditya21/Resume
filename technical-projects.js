(() => {
    const search = document.querySelector("[data-tech-search]");
    const capability = document.querySelector("[data-tech-capability]");
    const status = document.querySelector("[data-tech-status]");
    const family = document.querySelector("[data-tech-family]");
    const count = document.querySelector("[data-tech-count]");
    const grid = document.querySelector("[data-tech-grid]");
    const empty = document.querySelector("[data-tech-empty]");
    const sort = document.querySelector("[data-tech-sort]");
    const clear = document.querySelector("[data-tech-clear]");
    const disclosure = document.querySelector("[data-complete-library]");
    const cards = [...document.querySelectorAll("[data-project-card]")];

    if (!grid || cards.length === 0) return;

    const controls = [search, capability, status, family, sort, clear].filter(Boolean);
    const gridId = grid.id || "technical-project-grid";
    grid.id = gridId;
    grid.setAttribute("aria-label", "Complete technical project library");
    controls.forEach((control) => control.setAttribute("aria-controls", gridId));
    cards.forEach((card, index) => {
        card.dataset.portfolioOrder = String(index);
    });

    if (count) {
        count.setAttribute("role", "status");
        count.setAttribute("aria-live", "polite");
        count.setAttribute("aria-atomic", "true");
    }

    const initialParams = new URLSearchParams(window.location.search);
    if (search) search.value = initialParams.get("q") || "";
    if (capability) capability.value = optionValue(capability, initialParams.get("capability"));
    if (status) status.value = optionValue(status, initialParams.get("status"));
    if (family) family.value = optionValue(family, initialParams.get("family"));
    if (sort) sort.value = initialParams.get("sort") === "az" ? "az" : "featured";

    if (disclosure && (window.location.hash === "#complete-library" || [...initialParams.keys()].length > 0)) {
        disclosure.open = true;
    }

    function optionValue(select, requested) {
        if (!select || !requested) return "all";
        return [...select.options].some((option) => option.value === requested) ? requested : "all";
    }

    function normalized(value) {
        return value.trim().toLocaleLowerCase();
    }

    function updateUrl() {
        const url = new URL(window.location.href);
        const values = {
            q: search?.value.trim() || "",
            capability: capability?.value || "all",
            status: status?.value || "all",
            family: family?.value || "all",
            sort: sort?.value || "featured",
        };

        Object.entries(values).forEach(([key, value]) => {
            const isDefault = !value || value === "all" || (key === "sort" && value === "featured");
            if (isDefault) url.searchParams.delete(key);
            else url.searchParams.set(key, value);
        });
        window.history.replaceState(null, "", `${url.pathname}${url.search}${url.hash}`);
    }

    function render({ updateHistory = true } = {}) {
        const query = normalized(search?.value || "");
        let visible = 0;

        const orderedCards = [...cards].sort((left, right) => {
            if (sort?.value === "az") {
                return (left.dataset.name || "").localeCompare(right.dataset.name || "");
            }
            return Number(left.dataset.portfolioOrder) - Number(right.dataset.portfolioOrder);
        });
        orderedCards.forEach((card) => grid.append(card));

        cards.forEach((card) => {
            const matches = [
                !query || normalized(card.dataset.search || card.textContent || "").includes(query),
                !capability || capability.value === "all" || card.dataset.capability === capability.value,
                !status || status.value === "all" || card.dataset.status === status.value,
                !family || family.value === "all" || card.dataset.family === family.value,
            ].every(Boolean);
            card.hidden = !matches;
            if (matches) visible += 1;
        });

        if (count) count.textContent = `${visible} ${visible === 1 ? "project" : "projects"}`;
        if (empty) empty.hidden = visible !== 0;
        if (clear) {
            clear.disabled = !query
                && (!capability || capability.value === "all")
                && (!status || status.value === "all")
                && (!family || family.value === "all")
                && (!sort || sort.value === "featured");
        }
        if (updateHistory) updateUrl();
    }

    search?.addEventListener("input", () => render());
    [capability, status, family, sort].forEach((control) => control?.addEventListener("change", () => render()));
    clear?.addEventListener("click", () => {
        if (search) search.value = "";
        if (capability) capability.value = "all";
        if (status) status.value = "all";
        if (family) family.value = "all";
        if (sort) sort.value = "featured";
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
        if (search) search.value = params.get("q") || "";
        if (capability) capability.value = optionValue(capability, params.get("capability"));
        if (status) status.value = optionValue(status, params.get("status"));
        if (family) family.value = optionValue(family, params.get("family"));
        if (sort) sort.value = params.get("sort") === "az" ? "az" : "featured";
        render({ updateHistory: false });
    });

    render({ updateHistory: false });
})();
