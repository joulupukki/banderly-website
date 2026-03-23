# App Icon Integration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the Banderly app icon to the marketing page in three placements: sticky nav, hero, and a download/coming-soon section.

**Architecture:** Single-file changes to the existing Astro page plus one new static asset. No new dependencies. Uses existing CSS variable system and IntersectionObserver pattern.

**Tech Stack:** Astro, HTML, CSS, vanilla JS

---

### Task 1: Copy app icon asset to public/

**Files:**
- Create: `public/app-icon.png`

- [ ] **Step 1: Copy the PNG to public/**

```bash
cp ~/Documents/Banderly-App-Icon.png public/app-icon.png
```

- [ ] **Step 2: Verify the file exists**

```bash
ls -la public/app-icon.png
```
Expected: file exists, ~100KB+ PNG

- [ ] **Step 3: Commit**

```bash
git add public/app-icon.png
git commit -m "Add app icon asset to public directory"
```

---

### Task 2: Add sticky navigation bar

**Files:**
- Modify: `src/pages/index.astro` (CSS: after line ~420 footer styles, HTML: after line 499 `<div class="page-content">`, JS: extend script block)

- [ ] **Step 1: Add nav CSS styles**

Add after the `.footer` styles block (~line 420):

```css
/* ─── Sticky Nav ─── */
.sticky-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.75rem 1.5rem;
  background: rgba(10, 10, 15, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-subtle);
  opacity: 0;
  transform: translateY(-100%);
  transition: opacity 0.3s ease, transform 0.3s ease;
  pointer-events: none;
}

.sticky-nav.visible {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}

.sticky-nav-icon {
  width: 28px;
  height: 28px;
  border-radius: 7px;
  flex-shrink: 0;
}

.sticky-nav-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}
```

- [ ] **Step 2: Add nav HTML**

Insert right after `<div class="page-content">` (line 499):

```html
<!-- Sticky Nav -->
<nav class="sticky-nav">
  <img src="/app-icon.png" alt="Banderly app icon" class="sticky-nav-icon" width="28" height="28" />
  <span class="sticky-nav-name">Banderly</span>
</nav>
```

- [ ] **Step 3: Add nav scroll observer in script block**

Add after the existing observer code (~line 696):

```javascript
// Show/hide sticky nav based on hero visibility
const nav = document.querySelector('.sticky-nav');
const hero = document.querySelector('.hero');
const navObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      nav.classList.remove('visible');
    } else {
      nav.classList.add('visible');
    }
  });
}, { threshold: 0 });
navObserver.observe(hero);
```

- [ ] **Step 4: Verify in browser**

```bash
npm run dev
```

Scroll past hero — nav should fade in. Scroll back up — nav should hide.

- [ ] **Step 5: Commit**

```bash
git add src/pages/index.astro
git commit -m "Add sticky navigation bar with app icon"
```

---

### Task 3: Add app icon to hero section

**Files:**
- Modify: `src/pages/index.astro` (CSS: add hero-icon styles, HTML: insert img between badge and h1)

- [ ] **Step 1: Add hero icon CSS**

Add after `.hero-badge` styles (~line 138):

```css
.hero-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  margin-bottom: 1.75rem;
  box-shadow: 0 8px 32px rgba(29, 78, 216, 0.3), 0 0 60px rgba(29, 78, 216, 0.1);
  animation: fadeInUp 0.8s ease-out 0.05s both;
}
```

Add mobile override inside `@media (max-width: 768px)`:

```css
.hero-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
}
```

- [ ] **Step 2: Add hero icon HTML**

Insert between the `<span class="hero-badge">` and `<h1 class="hero-logo">` (line 503-504):

```html
<img src="/app-icon.png" alt="Banderly app icon" class="hero-icon" width="80" height="80" />
```

- [ ] **Step 3: Verify in browser**

Icon should appear centered between badge and "Banderly" text, with cobalt glow shadow. Should be 64px on mobile.

- [ ] **Step 4: Commit**

```bash
git add src/pages/index.astro
git commit -m "Add app icon to hero section"
```

---

### Task 4: Replace closing CTA with download section

**Files:**
- Modify: `src/pages/index.astro` (CSS: add download section styles, HTML: replace closing section inner content)

- [ ] **Step 1: Add download section CSS**

Add after `.closing-badge` styles (~line 409):

```css
.closing-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  margin: 0 auto 1.5rem;
  box-shadow: 0 4px 20px rgba(29, 78, 216, 0.25);
  position: relative;
}

.store-badges {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  position: relative;
}

.store-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.4rem;
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-secondary);
  font-size: 0.8rem;
  font-weight: 500;
  letter-spacing: 0.01em;
  transition: border-color 0.3s ease, color 0.3s ease;
  text-decoration: none;
}

.store-badge:hover {
  border-color: var(--border-glow);
  color: var(--text-emphasis);
}

.store-badge svg {
  width: 18px;
  height: 18px;
}
```

- [ ] **Step 2: Replace closing section HTML**

Replace the inner content of the `.closing` section (lines 672-674) with:

```html
<img src="/app-icon.png" alt="Banderly app icon" class="closing-icon reveal" width="64" height="64" />
<h2 class="closing-title reveal">Coming soon to iOS & Android</h2>
<p class="closing-sub reveal">We're putting the finishing touches on Banderly. A better way to manage your band is almost here.</p>
<div class="store-badges reveal reveal-delay-1">
  <span class="store-badge">
    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.8-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/></svg>
    App Store
  </span>
  <span class="store-badge">
    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M3.18 23.49c.38.21.83.24 1.23.06l12.49-6.26-2.77-2.77L3.18 23.49zm-.62-1.19V1.7c0-.35.18-.67.47-.86L14.38 14.5 3.03 22.86c-.28-.11-.47-.38-.47-.56zM20.55 10.55l-3.22-1.79-3.02 3.02 3.24 3.24 3-1.5c.62-.31.62-1.21 0-2.97zM14.13 9.52L4.96.36l-.33-.17c.01 0 .02-.01.03-.01.4-.18.86-.15 1.23.06l10.85 5.44-2.61 3.84z"/></svg>
    Google Play
  </span>
</div>
```

- [ ] **Step 3: Verify in browser**

Closing section should show icon, "Coming soon to iOS & Android" heading, subtitle, and two placeholder store badges.

- [ ] **Step 4: Commit**

```bash
git add src/pages/index.astro
git commit -m "Replace closing CTA with download/coming-soon section"
```

---

### Task 5: Final verification and cleanup

- [ ] **Step 1: Full page review**

Run `npm run dev` and verify all three icon placements:
1. Hero: icon between badge and "Banderly" text, cobalt glow
2. Nav: appears on scroll with icon + wordmark, hides when scrolling to top
3. Download: icon + heading + store badges at bottom

- [ ] **Step 2: Mobile responsive check**

Check at 375px width:
- Hero icon scales to 64px
- Nav icon stays 28px
- Store badges stack or stay side-by-side gracefully

- [ ] **Step 3: Build check**

```bash
npm run build
```
Expected: clean build, no errors
