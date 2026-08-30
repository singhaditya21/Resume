const portfolio = [
    { id: "01", institution: "HDFC Bank", title: "Six journeys, four objectives", subtitle: "Reusable acquisition and servicing journeys across cards, loans, KYC, insurance and funding.", type: "Delivered", region: "India", file: "01HdfcSixJourneys.pdf" },
    { id: "02", institution: "HDFC Bank", title: "Two journeys, opposite risk", subtitle: "A comparison of digital journeys whose controls, economics and failure modes point in different directions.", type: "Delivered", region: "India", file: "02HdfcTwoJourneys.pdf" },
    { id: "03", institution: "HDFC Bank", title: "Cross-entity by design", subtitle: "How shared identity, consent and orchestration create reuse without erasing entity boundaries.", type: "Architecture", region: "India", file: "03HdfcCrossEntity.pdf" },
    { id: "04", institution: "State Bank of India", title: "Operating CRM at 300,000 users", subtitle: "A scale reference for platform operations, governance and adoption across a very large banking workforce.", type: "Analysis", region: "India", file: "04SbiScaleReference.pdf" },
    { id: "05", institution: "State Bank of India", title: "Reading an enterprise AI RFP", subtitle: "A practical method for finding the operating model hidden inside a large AI ambition.", type: "Strategy", region: "India", file: "05SbiEnterpriseAiRfp.pdf" },
    { id: "06", institution: "State Bank of India", title: "Seventy-five use cases, three years", subtitle: "Turning a use-case inventory into sequenced delivery, governance, capacity and value realization.", type: "Strategy", region: "India", file: "06SbiUseCaseProgramme.pdf" },
    { id: "07", institution: "Axis Max Life", title: "Displacing the incumbent", subtitle: "The decision logic required to replace a deeply embedded enterprise platform.", type: "Strategy", region: "India", file: "07AxisMaxLifeDisplacement.pdf" },
    { id: "08", institution: "Axis Max Life", title: "Configurability as architecture", subtitle: "Why configurable rules and controls can matter more than feature breadth in regulated operations.", type: "Architecture", region: "India", file: "08AxisMaxLifeConfigurability.pdf" },
    { id: "09", institution: "Axis Max Life", title: "Five blockers and a deal", subtitle: "A structured path from technical objections to an executable commercial decision.", type: "Strategy", region: "India", file: "09AxisMaxLifeBlockers.pdf" },
    { id: "10", institution: "Punjab National Bank", title: "Two clocks, one engine", subtitle: "Designing customer and operational journeys that run at different speeds on shared foundations.", type: "Architecture", region: "India", file: "10PnbTwoClocks.pdf" },
    { id: "11", institution: "Punjab National Bank", title: "The RM's day, rebuilt", subtitle: "Reframing relationship management around decisions, next actions and accountable workflows.", type: "Experience", region: "India", file: "11PnbRmDayRebuilt.pdf" },
    { id: "12", institution: "Kotak Mahindra Life", title: "Risk-based policy revival", subtitle: "A decisioning approach that changes the treatment path according to customer and policy risk.", type: "Strategy", region: "India", file: "12KotakPolicyRevival.pdf" },
    { id: "13", institution: "Kotak", title: "Case visibility, five systems", subtitle: "A service architecture for creating one accountable case view across fragmented systems.", type: "Architecture", region: "India", file: "13KotakCaseVisibility.pdf" },
    { id: "14", institution: "Abu Dhabi Islamic Bank", title: "Eight programmes, three years", subtitle: "A platform portfolio spanning sales, service, onboarding, credit, warning, planning and campaigns.", type: "Delivered", region: "UAE", file: "14AdibEightProgrammes.pdf" },
    { id: "15", institution: "Abu Dhabi Islamic Bank", title: "Parallel approvals, including Sharia", subtitle: "Approval design for multiple governance paths without losing traceability or throughput.", type: "Architecture", region: "UAE", file: "15AdibParallelApprovals.pdf" },
    { id: "16", institution: "Abu Dhabi Islamic Bank", title: "Early warning without the model", subtitle: "A governed early-warning operating system that begins with evidence, workflow and ownership.", type: "Strategy", region: "UAE", file: "16AdibEarlyWarning.pdf" },
    { id: "17", institution: "Arab Bank", title: "One corporate spine, six countries", subtitle: "A reusable corporate-banking architecture designed to travel across market and entity boundaries.", type: "Delivered", region: "Middle East", file: "17ArabBankCorporateSpine.pdf" },
    { id: "18", institution: "Arab Bank", title: "From dashboards to decisions", subtitle: "Connecting relationship profitability and customer insight to governed frontline action.", type: "Analytics", region: "Middle East", file: "18ArabBankDashboards.pdf" },
    { id: "19", institution: "Cross-account pattern", title: "Group exposure is the hard problem", subtitle: "Why corporate hierarchy and exposure aggregation determine the quality of enterprise risk views.", type: "Analysis", region: "Cross-market", file: "19CorporateGroupExposure.pdf" },
    { id: "20", institution: "Maybank", title: "Nine architectures, two finalists", subtitle: "A seven-criterion decision model for choosing among compliant multi-market tenancy options.", type: "Architecture", region: "ASEAN", file: "20MaybankTenancyDecision.pdf" },
    { id: "21", institution: "Maybank", title: "One architecture, three regulators", subtitle: "A control model that preserves shared capability while respecting jurisdictional boundaries.", type: "Architecture", region: "ASEAN", file: "21MaybankThreeRegulators.pdf" },
    { id: "22", institution: "Maybank", title: "What a technical panel asks", subtitle: "The architecture, security and operating questions that separate a pitch from an approvable design.", type: "Method", region: "ASEAN", file: "22MaybankTechnicalPanel.pdf" },
    { id: "23", institution: "Bank Danamon", title: "Six thousand call types to 526", subtitle: "A service-design simplification that turns uncontrolled variety into an operable taxonomy.", type: "Analysis", region: "Indonesia", file: "23DanamonCallTypes.pdf" },
    { id: "24", institution: "ASEAN portfolio", title: "Three banks, three entry points", subtitle: "How different constraints change the most credible starting point for transformation.", type: "Strategy", region: "ASEAN", file: "24AseanEntryPoints.pdf" },
    { id: "25", institution: "US credit unions", title: "The deployment factory", subtitle: "Productizing repeated delivery into shared definitions, integration patterns, configuration and migration tools.", type: "Product", region: "United States", file: "25UsDeploymentFactory.pdf" },
    { id: "26", institution: "US credit unions", title: "The integration tax", subtitle: "The recurring cost of fragmented cores, processors and member-data definitions—and how to reduce it.", type: "Architecture", region: "United States", file: "26UsIntegrationTax.pdf" },
    { id: "27", institution: "Dupaco Community Credit Union", title: "Six 360s and an action centre", subtitle: "Role-specific member views organized around accountable work instead of passive information.", type: "Delivered", region: "United States", file: "27DupacoSix360s.pdf" },
    { id: "28", institution: "WESTconsin Credit Union", title: "Card servicing, three processors", subtitle: "A unified servicing experience across fragmented card and transaction platforms.", type: "Delivered", region: "United States", file: "28WestconsinCardServicing.pdf" },
    { id: "29", institution: "Magnifi Financial", title: "Member banding and value", subtitle: "Translating member context into governed segmentation, prioritization and next action.", type: "Delivered", region: "United States", file: "29MagnifiMemberBanding.pdf" },
    { id: "30", institution: "Cross-account pattern", title: "Notes from 38 programmes", subtitle: "The recurring decisions, failure modes and design principles visible across a long delivery record.", type: "Synthesis", region: "Cross-market", file: "30NotesFrom38Programmes.pdf" }
];

const menuToggle = document.querySelector(".menu-toggle");
const siteNav = document.querySelector(".site-nav");
const menuLinks = [...document.querySelectorAll(".site-nav a")];
const navLinks = menuLinks.filter((link) => link.getAttribute("href")?.startsWith("#"));
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

function closeMenu() {
    if (!menuToggle || !siteNav) return;
    siteNav.classList.remove("is-open");
    menuToggle.setAttribute("aria-expanded", "false");
}

menuToggle?.addEventListener("click", () => {
    const isOpen = siteNav?.classList.toggle("is-open") ?? false;
    menuToggle.setAttribute("aria-expanded", String(isOpen));
});

menuLinks.forEach((link) => link.addEventListener("click", closeMenu));
document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && siteNav?.classList.contains("is-open")) {
        closeMenu();
        menuToggle?.focus();
    }
});
window.addEventListener("resize", () => {
    if (window.innerWidth > 1240) closeMenu();
});

document.addEventListener("click", (event) => {
    const link = event.target.closest('a[href^="#"]');
    if (!link) return;
    const hash = link.getAttribute("href");
    if (!hash || hash.length < 2) return;
    const target = document.getElementById(hash.slice(1));
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: reducedMotion.matches ? "auto" : "smooth", block: "start" });
    history.replaceState(null, "", hash);
});

const progressBar = document.querySelector(".scroll-progress span");
function updateScrollState() {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const progress = scrollable > 0 ? Math.min(1, window.scrollY / scrollable) : 0;
    if (progressBar) progressBar.style.width = `${progress * 100}%`;

    let activeId = "";
    let activeTop = Number.NEGATIVE_INFINITY;
    for (const link of navLinks) {
        const id = link.getAttribute("href")?.slice(1);
        const section = id ? document.getElementById(id) : null;
        const top = section?.getBoundingClientRect().top;
        if (typeof top === "number" && top <= 160 && top > activeTop) {
            activeId = id;
            activeTop = top;
        }
    }
    navLinks.forEach((link) => {
        const isActive = link.getAttribute("href") === `#${activeId}`;
        link.classList.toggle("is-active", isActive);
        if (isActive) link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
    });
}
window.addEventListener("scroll", updateScrollState, { passive: true });
updateScrollState();

const workFilters = [...document.querySelectorAll("[data-work-filter]")];
const workCards = [...document.querySelectorAll("[data-work-category]")];
workFilters.forEach((button) => {
    button.addEventListener("click", () => {
        const selected = button.dataset.workFilter;
        workFilters.forEach((candidate) => {
            const active = candidate === button;
            candidate.classList.toggle("is-active", active);
            candidate.setAttribute("aria-pressed", String(active));
        });
        workCards.forEach((card) => {
            card.hidden = selected !== "all" && card.dataset.workCategory !== selected;
        });
    });
});

const portfolioGrid = document.querySelector("[data-portfolio-grid]");
const portfolioSearch = document.querySelector("[data-portfolio-search]");

function portfolioCard(item) {
    const link = document.createElement("a");
    link.className = "portfolio-card";
    link.href = `P%20Presentations/decksPdf/${encodeURIComponent(item.file)}`;
    link.target = "_blank";
    link.rel = "noopener";
    link.setAttribute("aria-label", `${item.institution}: ${item.title} (PDF)`);

    const top = document.createElement("span");
    top.className = "portfolio-card-top";
    const number = document.createElement("span");
    number.textContent = item.id;
    const region = document.createElement("span");
    region.textContent = item.region;
    top.append(number, region);

    const title = document.createElement("h3");
    title.textContent = item.title;
    const subtitle = document.createElement("p");
    subtitle.textContent = item.subtitle;
    const meta = document.createElement("span");
    meta.className = "portfolio-card-meta";
    meta.textContent = `${item.institution} · ${item.type} ↗`;
    link.append(top, title, subtitle, meta);
    return link;
}

function renderPortfolio(query = "") {
    if (!portfolioGrid) return;
    const normalized = query.trim().toLocaleLowerCase();
    const matches = portfolio.filter((item) =>
        [item.id, item.institution, item.title, item.subtitle, item.type, item.region]
            .join(" ")
            .toLocaleLowerCase()
            .includes(normalized)
    );
    portfolioGrid.replaceChildren(...matches.map(portfolioCard));
    if (matches.length === 0) {
        const empty = document.createElement("p");
        empty.className = "portfolio-empty";
        empty.textContent = "No portfolio notes match that search.";
        portfolioGrid.append(empty);
    }
}

portfolioSearch?.addEventListener("input", (event) => renderPortfolio(event.target.value));
renderPortfolio();

document.querySelectorAll("[data-deck-sampler]").forEach((sampler) => {
    const slideCount = Number(sampler.dataset.slideCount);
    const slideBase = sampler.dataset.slideBase;
    const image = sampler.querySelector("[data-slide-image]");
    const position = sampler.querySelector("[data-slide-position]");
    const previous = sampler.querySelector("[data-slide-prev]");
    const next = sampler.querySelector("[data-slide-next]");
    const stage = sampler.querySelector(".deck-stage");
    const title = sampler.querySelector("h3")?.textContent?.trim() || "Presentation";
    let currentSlide = 1;

    if (!slideCount || !slideBase || !image || !position || !previous || !next) return;

    function showSlide(requestedSlide) {
        currentSlide = ((requestedSlide - 1 + slideCount) % slideCount) + 1;
        image.src = `${slideBase}${currentSlide}.png`;
        image.alt = `${title} presentation, slide ${currentSlide}`;
        position.textContent = `${currentSlide} / ${slideCount}`;

        const followingSlide = (currentSlide % slideCount) + 1;
        const preload = new Image();
        preload.src = `${slideBase}${followingSlide}.png`;
    }

    previous.addEventListener("click", () => showSlide(currentSlide - 1));
    next.addEventListener("click", () => showSlide(currentSlide + 1));
    stage?.addEventListener("keydown", (event) => {
        if (event.key === "ArrowLeft") {
            event.preventDefault();
            showSlide(currentSlide - 1);
        }
        if (event.key === "ArrowRight") {
            event.preventDefault();
            showSlide(currentSlide + 1);
        }
    });
});

document.querySelectorAll("[data-year]").forEach((node) => {
    node.textContent = String(new Date().getFullYear());
});
