const fs = require('fs');
const path = require('path');

// Read the script.js file to load it into the jsdom environment
const scriptCode = fs.readFileSync(path.resolve(__dirname, '../script.js'), 'utf8');

describe('Mobile Menu Toggle', () => {
    let menuBtn;
    let navLinks;

    beforeAll(() => {
        // Mock IntersectionObserver
        class IntersectionObserver {
            constructor() {}
            observe() {}
            unobserve() {}
            disconnect() {}
        }
        global.IntersectionObserver = IntersectionObserver;

        // Set up a minimal DOM
        document.body.innerHTML = `
            <nav>
                <div class="menu-btn">Menu</div>
                <div class="nav-links" style="display: none;">
                    <a href="#section1">Section 1</a>
                    <a href="#section2">Section 2</a>
                </div>
            </nav>
            <div id="section1"></div>
            <div id="section2"></div>
        `;

        // Execute the script once
        eval(scriptCode);

        // Dispatch DOMContentLoaded to trigger script's event listener bindings
        const event = new Event('DOMContentLoaded');
        document.dispatchEvent(event);
    });

    beforeEach(() => {
        // Reset state before each test
        menuBtn = document.querySelector('.menu-btn');
        navLinks = document.querySelector('.nav-links');
        navLinks.style.display = 'none'; // reset menu state
    });

    test('should open mobile menu and set inline styles correctly', () => {
        // Initial state
        expect(navLinks.style.display).toBe('none');

        // Click to open
        menuBtn.click();

        // Check new inline styles
        expect(navLinks.style.display).toBe('flex');
        expect(navLinks.style.flexDirection).toBe('column');
        expect(navLinks.style.position).toBe('absolute');
        expect(navLinks.style.top).toBe('100%');
        expect(navLinks.style.left).toBe('0px');
        expect(navLinks.style.width).toBe('100%');
        expect(navLinks.style.background).toBe('white');
        expect(navLinks.style.padding).toBe('1rem');
        expect(navLinks.style.boxShadow).toBe('0 10px 15px -3px rgba(0, 0, 0, 0.1)'); // Updated to match actual JSDOM output
    });

    test('should close mobile menu when clicked again', () => {
        // Open first
        menuBtn.click();
        expect(navLinks.style.display).toBe('flex');

        // Click to close
        menuBtn.click();
        expect(navLinks.style.display).toBe('none');
    });

    test('should close mobile menu when an anchor link is clicked and window width <= 768px', () => {
        // Open menu
        menuBtn.click();
        expect(navLinks.style.display).toBe('flex');

        // Simulate mobile window width
        global.innerWidth = 500;

        // Mock scrollIntoView since it's not implemented in jsdom by default
        Element.prototype.scrollIntoView = jest.fn();

        const anchor = document.querySelector('a[href="#section1"]');

        // Mock click event to preventDefault
        anchor.click();

        // Menu should be closed
        expect(navLinks.style.display).toBe('none');
        expect(Element.prototype.scrollIntoView).toHaveBeenCalledWith({
            behavior: 'smooth',
            block: 'start'
        });
    });

    test('should NOT close menu when anchor link is clicked and window width > 768px', () => {
        // Open menu
        menuBtn.click();
        expect(navLinks.style.display).toBe('flex');

        // Simulate desktop window width
        global.innerWidth = 1024;

        // Mock scrollIntoView
        Element.prototype.scrollIntoView = jest.fn();

        const anchor = document.querySelector('a[href="#section1"]');
        anchor.click();

        // Menu should STILL be open
        expect(navLinks.style.display).toBe('flex');
    });
});
