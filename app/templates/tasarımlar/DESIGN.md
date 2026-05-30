---
name: Cyber Gate Redux
colors:
  surface: '#131313'
  surface-dim: '#131313'
  surface-bright: '#3a3939'
  surface-container-lowest: '#0e0e0e'
  surface-container-low: '#1c1b1b'
  surface-container: '#201f1f'
  surface-container-high: '#2a2a2a'
  surface-container-highest: '#353534'
  on-surface: '#e5e2e1'
  on-surface-variant: '#e8bdb6'
  inverse-surface: '#e5e2e1'
  inverse-on-surface: '#313030'
  outline: '#ae8882'
  outline-variant: '#5e3f3a'
  surface-tint: '#ffb4a8'
  primary: '#ffb4a8'
  on-primary: '#690000'
  primary-container: '#cc0000'
  on-primary-container: '#ffdad4'
  inverse-primary: '#c00000'
  secondary: '#c8c6c5'
  on-secondary: '#313030'
  secondary-container: '#474746'
  on-secondary-container: '#b7b5b4'
  tertiary: '#c6c6c7'
  on-tertiary: '#2f3131'
  tertiary-container: '#636565'
  on-tertiary-container: '#e2e3e3'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdad4'
  primary-fixed-dim: '#ffb4a8'
  on-primary-fixed: '#410000'
  on-primary-fixed-variant: '#930000'
  secondary-fixed: '#e5e2e1'
  secondary-fixed-dim: '#c8c6c5'
  on-secondary-fixed: '#1c1b1b'
  on-secondary-fixed-variant: '#474746'
  tertiary-fixed: '#e2e2e2'
  tertiary-fixed-dim: '#c6c6c7'
  on-tertiary-fixed: '#1a1c1c'
  on-tertiary-fixed-variant: '#454747'
  background: '#131313'
  on-background: '#e5e2e1'
  surface-variant: '#353534'
typography:
  display-lg:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-md:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 8px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 64px
  container-max: 1280px
---

## Brand & Style
The design system embodies a high-performance "Cyber Gate" aesthetic—a fusion of advanced technology and security. It targets a technical audience that values precision, speed, and reliability. 

The visual style is **Glassmorphism mixed with Dark Tech Minimalism**. It utilizes deep charcoal backgrounds to create a sense of infinite depth, contrasted by a singular, aggressive red accent. The emotional response is one of authority and cutting-edge sophistication. Transparency, backdrop blurs, and sharp lines are the primary vehicles for this narrative.

## Colors
This design system operates exclusively in a **Dark Mode** environment. The palette is anchored by the "Cyber Red" (#CC0000) extracted from the reference, used sparingly but high-impactfully for critical actions and brand identity.

- **Primary:** The signature red, used for primary buttons, active states, and focus indicators.
- **Surface & Background:** Deep charcoals and near-blacks provide the "void" for glass elements to sit within.
- **Glass Effects:** Semi-transparent layers use a white stroke at 10% opacity to define edges against the dark background.
- **Functional:** Success states use a muted emerald, while warnings scale into orange-reds to maintain harmony with the primary red.

## Typography
The typography strategy leverages **Geist** for its clinical, developer-friendly precision and **JetBrains Mono** for technical metadata and labels.

- **Headlines:** Use tight letter-spacing and bold weights to command attention.
- **Body:** Prioritizes legibility with generous line heights and standard weights.
- **Monospaced Accents:** Used for status codes, IDs, and button labels to reinforce the "Cyber Gate" tech theme.
- **Color Application:** Primary headers are white; secondary text is a medium gray. Red is reserved for "Alert" typography or high-priority interactive labels only.

## Layout & Spacing
The layout follows a **12-column Fluid Grid** for desktop and a **4-column grid** for mobile. 

- **Rhythm:** An 8px base unit governs all padding and margins (8, 16, 24, 32, 48, 64).
- **Density:** The system favors high-density layouts for data-heavy views but utilizes large 64px vertical gaps between major content sections to allow the glassmorphic background blurs to "breathe."
- **Constraints:** Content is centered in a max-width container of 1280px, with margins expanding dynamically on ultra-wide displays.

## Elevation & Depth
Hierarchy is established through **Backdrop Blurs** and **Tonal Layering** rather than traditional drop shadows.

- **Level 0:** The base background (#0A0A0A).
- **Level 1 (Glass):** Surfaces use `backdrop-filter: blur(12px)` with a `rgba(255, 255, 255, 0.05)` fill and a 1px solid border (`rgba(255, 255, 255, 0.1)`).
- **Level 2 (Active):** Elevated cards or modals add a subtle red "inner glow" or a very faint red drop shadow (`rgba(204, 0, 0, 0.2)`) to indicate focus.
- **Interaction:** Hovering over a glass surface increases the background opacity slightly (from 5% to 8%).

## Shapes
The shape language is **Soft (0.25rem / 4px)**. This minimal rounding maintains a technical, "engineered" look while avoiding the harshness of completely sharp corners. 

- **Standard Elements:** 4px radius (inputs, buttons, cards).
- **Large Elements:** 8px radius (modals, main containers).
- **Interaction:** Buttons do not change shape on click, but they may expand their border-width or change stroke color to the primary red.

## Components
- **Buttons:** 
    - *Primary:* Solid Cyber Red (#CC0000) with white text. No shadow.
    - *Secondary:* Glass surface with a white border and red text.
- **Inputs:** Dark charcoal fill (#1A1A1A) with a 1px gray border that turns red on focus.
- **Chips:** Monospaced text inside a pill shape with a 1px red stroke for active states.
- **Lists:** Separated by thin 1px lines (`rgba(255, 255, 255, 0.05)`). Hover state utilizes a subtle red tint in the background.
- **Cards:** The primary container for the glassmorphic effect. Must always have a backdrop blur to distinguish from the background.
- **Status Indicators:** Small glowing dots. The "Active" or "Critical" dot uses the primary red with a CSS pulse animation.