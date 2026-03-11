---
name: tailwindcss
description: Tailwind CSS v4 utility-first styling patterns including responsive design, dark mode, and custom configuration. Use when styling with Tailwind, adding utility classes, configuring Tailwind, setting up dark mode, or customizing the theme.
user-invocable: true
---

# Tailwind CSS v4 Development Guidelines

## When to Use

- Styling components with Tailwind utilities
- Adding responsive design breakpoints
- Implementing dark mode
- Configuring Tailwind v4 theme (@theme inline)
- Using utility classes for layout, typography, colors
- Creating custom CSS with @layer
- Working with Tailwind-specific patterns (cn(), cva())

Best practices for using Tailwind CSS v4 utility classes effectively.

**Note**: This project uses Tailwind CSS v4 with CSS-first configuration. No `tailwind.config.js` file is used - theme is defined via `@theme inline` in `src/client/index.css`.

## Core Principles

1. **Utility-First**: Use utility classes instead of custom CSS
2. **Mobile-First**: Design for mobile, then scale up with responsive modifiers
3. **Component Extraction**: Extract repeated patterns into components
4. **Consistent Spacing**: Use Tailwind's spacing scale
5. **Custom Configuration**: Extend the default theme for brand consistency

## Basic Utilities

See [basic-utilities.md](reference/basic-utilities.md) for layout (flexbox, grid, positioning), spacing, typography, and color utility patterns.

---

## Responsive Design

### Breakpoints

```tsx
// Mobile-first responsive classes
<div className="w-full md:w-1/2 lg:w-1/3">
  {/* Full width on mobile, half on medium screens, third on large */}
</div>

<h1 className="text-2xl md:text-4xl lg:text-6xl">
  {/* Responsive text sizes */}
</h1>

<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
  {/* Responsive grid */}
</div>
```

### Container

```tsx
<div className="container mx-auto px-4">
  {/* Centered container with horizontal padding */}
</div>

<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  {/* Responsive container padding */}
</div>
```

## Component Patterns

See [component-patterns.md](examples/component-patterns.md) for button, card, and form input styling examples.

---

## State Variants

### Hover, Focus, Active

```tsx
<button className="bg-blue-500 hover:bg-blue-600 active:bg-blue-700 focus:ring-2 focus:ring-blue-500">
  Interactive Button
</button>

<a href="#" className="text-blue-600 hover:text-blue-800 hover:underline">
  Link
</a>
```

### Group Hover

```tsx
<div className="group">
    <img src="/image.jpg" className="transition-opacity group-hover:opacity-75" />
    <p className="group-hover:text-blue-600">Hover the container</p>
</div>
```

### Disabled

```tsx
<button className="disabled:cursor-not-allowed disabled:opacity-50" disabled>
    Disabled Button
</button>
```

## Dark Mode

This project uses **class-based** dark mode configured in `src/client/index.css`:

```css
@custom-variant dark (&:is(.dark *));
```

Colors use **oklch** values via CSS variables:

```css
:root {
    --background: oklch(1 0 0);
    --foreground: oklch(0.145 0 0);
}

.dark {
    --background: oklch(0.145 0 0);
    --foreground: oklch(0.985 0 0);
}
```

```tsx
// Use semantic token classes (not raw colors)
<div className="bg-background text-foreground">
    <h1 className="text-foreground">Title</h1>
    <p className="text-muted-foreground">Description</p>
</div>
```

## Custom Styles

### Arbitrary Values

```tsx
<div className="top-[117px]">           {/* Custom top value */}
<div className="bg-[#1da1f2]">          {/* Custom color */}
<div className="grid-cols-[200px_1fr]"> {/* Custom grid template */}
```

### @apply Directive

```css
/* components/button.css */
.btn-primary {
    @apply rounded-md bg-blue-600 px-4 py-2 font-medium text-white;
    @apply hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:outline-none;
    @apply disabled:cursor-not-allowed disabled:opacity-50;
}
```

## Configuration

### CSS-First Configuration (This Project)

This project uses Tailwind CSS v4 with **CSS-first configuration** - no `tailwind.config.js`. All theme config lives in `src/client/index.css`:

```css
@import "tailwindcss";
@import "tw-animate-css";

@custom-variant dark (&:is(.dark *));

@theme inline {
    --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
    --color-background: var(--background);
    --color-foreground: var(--foreground);
    --color-primary: var(--primary);
    --color-primary-foreground: var(--primary-foreground);
    --color-muted: var(--muted);
    --color-muted-foreground: var(--muted-foreground);
    --color-destructive: var(--destructive);
    --color-border: var(--border);
    --color-input: var(--input);
    --color-ring: var(--ring);
    --radius-sm: calc(var(--radius) - 4px);
    --radius-md: calc(var(--radius) - 2px);
    --radius-lg: var(--radius);
    --radius-xl: calc(var(--radius) + 4px);
}
```

Colors are defined as **oklch** CSS variables:

```css
:root {
    --radius: 0.625rem;
    --background: oklch(1 0 0);
    --foreground: oklch(0.145 0 0);
    --primary: oklch(0.205 0 0);
    --primary-foreground: oklch(0.985 0 0);
    /* ... */
}
```

The Vite plugin handles Tailwind integration:

```typescript
// vite.config.ts
import tailwindcss from "@tailwindcss/vite";
// ...
plugins: [tailwindcss() /* ... */];
```

## Plugins

### Official Plugins

```bash
npm install @tailwindcss/forms
npm install @tailwindcss/typography
npm install @tailwindcss/aspect-ratio
npm install @tailwindcss/container-queries
```

```tsx
// @tailwindcss/forms
<input type="text" className="form-input rounded-md" />

// @tailwindcss/typography
<article className="prose lg:prose-xl">
  <h1>Article Title</h1>
  <p>Content...</p>
</article>
```

## Performance

### Build Integration

This project uses the `@tailwindcss/vite` plugin for optimal build performance. Tailwind v4 automatically detects and scans all template files - no `content` configuration needed.

### Build Performance

Tailwind v4 delivers 3.5x faster full builds (~100ms) compared to v3 using modern CSS features like `@property` and `color-mix()`.

## Common Patterns

### Centered Content

```tsx
<div className="flex min-h-screen items-center justify-center">
    <div>Centered content</div>
</div>
```

### Sticky Header

```tsx
<header className="sticky top-0 z-50 border-b bg-white">
    <nav>Navigation</nav>
</header>
```

### Grid Layout

```tsx
<div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
    {posts.map((post) => (
        <PostCard key={post.id} post={post} />
    ))}
</div>
```

### Truncate Text

```tsx
<p className="truncate">This text will be truncated with ellipsis if too long</p>
<p className="line-clamp-3">This text will show max 3 lines with ellipsis</p>
```

## Best Practices

1. **Use Consistent Spacing**: Stick to Tailwind's spacing scale
2. **Responsive by Default**: Always consider mobile-first design
3. **Extract Components**: Avoid repeating long class lists
4. **Use Theme Colors**: Define custom colors in config, not arbitrary values
5. **Leverage @apply Sparingly**: Prefer utility classes in JSX
6. **Enable Dark Mode**: Plan for dark mode from the start
7. **Use Plugins**: Leverage official plugins for common needs
8. **Optimize Production**: Ensure purge is configured correctly

## Additional Resources

For detailed information, see:

- [Utility Patterns](resources/utility-patterns.md)
- [Component Library](resources/component-library.md)
- [Configuration Guide](resources/configuration.md)
