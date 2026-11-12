# Format Audit and Extraction Decisions

## Stable design elements retained

- Fixed 1280 x 720, 16:9 canvas with viewport scaling.
- Dark navy radial-gradient background.
- Aptos/Inter/Segoe UI font stack.
- White text with muted blue-gray body copy.
- Blue, cyan, purple, pink, green, amber, and red semantic accents.
- Upper-left deck identifier and upper-right section/progress treatment.
- Rounded gradient panels with fine borders and soft shadows.
- Large title hierarchy and blue title emphasis.
- CSS-only slide reveal animations.
- Keyboard navigation, fullscreen mode, and print-to-PDF rules.

## Problems removed from the source implementation

- Repeated top-bar markup on every slide.
- Hard-coded slide count.
- Slide-specific version overrides accumulated at the end of the stylesheet.
- Multi-megabyte embedded base64 images.
- Project-specific links, names, dates, and labels.
- Layout logic mixed directly with content.

## New agent-facing abstractions

- A data-driven slide array.
- Automatic top bars and progress bars.
- Ten reusable layouts.
- External asset paths during editing.
- A single-file build step for sharing.
- Overflow diagnostics available with `D` or `?debug=1`.
