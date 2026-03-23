# App Icon Integration — Design Spec

## Goal

Incorporate the Banderly app icon (music note / "B" letterform on cobalt gradient) into the marketing landing page to strengthen brand recognition, add visual interest to the hero, and prepare a download section for future App Store and Google Play links.

## Current State

- Single-page Astro site (`src/pages/index.astro`)
- Hero uses "Banderly" as styled gradient text — no logo image
- No navigation bar
- Closing CTA is a generic "coming soon" section
- App icon exists as `Banderly-App-Icon.png` (1024x1024) — no SVG yet
- No App Store or Google Play links available yet

## Design

### 1. Sticky Navigation Bar (new)

- Fixed at top of viewport
- Contains: app icon (28–32px, rounded corners) + "Banderly" wordmark
- **Hidden when hero is in view** — fades in once user scrolls past the hero (prevents competing with the hero icon)
- Subtle backdrop blur + semi-transparent background matching `--bg-deep`
- Border-bottom using `--border-subtle`
- Transition: fade-in over ~0.3s triggered by scroll observer on the hero section

### 2. Hero Enhancement (modify existing)

- Add the app icon **centered above** the existing "Banderly" gradient text
- Icon size: 72–80px with iOS-style rounded corners (`border-radius: 18–20px`)
- Subtle box-shadow glow using `--glow-cobalt` to match the site's atmospheric aesthetic
- Visual hierarchy becomes: Badge → Icon → Name → Tagline → Subtitle
- Uses the same `fadeInUp` animation with a staggered delay between badge and text
- Implemented as `<img src="/app-icon.png">` with CSS sizing

### 3. Download / Coming Soon Section (new, replaces closing CTA)

- Replaces the current closing section content
- Layout (centered):
  - App icon (56–64px, rounded corners, subtle shadow)
  - Heading: "Coming soon to iOS & Android"
  - Subtitle: brief teaser text
  - Two placeholder store badges side by side (styled as pill-shaped outlined buttons)
    - "App Store" and "Google Play" text
    - Muted colors (`--text-secondary`, subtle border)
    - When real links are available: swap in official badge images wrapped in `<a>` tags
- Uses the existing `.closing` section styling as a base

### Technical Approach

- **Asset**: Copy `~/Documents/Banderly-App-Icon.png` to `public/app-icon.png`
- **Image format**: Use the PNG directly via `<img>` tags at three sizes. Can swap for SVG later.
- **Nav scroll behavior**: Add an `IntersectionObserver` on the hero section. When hero exits the viewport, add a class to show the nav. Reuses the existing observer pattern already in the page.
- **Responsive**:
  - Mobile: icon sizes scale down slightly (hero icon ~56px, nav icon ~24px)
  - Nav remains fixed on mobile with same show/hide behavior
- **No new dependencies** — pure HTML/CSS/JS within the existing Astro page

### Files Changed

| File | Change |
|------|--------|
| `public/app-icon.png` | New — copy of app icon asset |
| `src/pages/index.astro` | Modified — add nav bar, hero icon, replace closing section |

### Future Upgrades (out of scope)

- Replace PNG with SVG for crisp rendering at all sizes
- Replace placeholder store badges with official App Store / Google Play badge images and links
- Add `og:image` meta tag using the app icon
