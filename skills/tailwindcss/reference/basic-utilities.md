# Basic Utilities

## Layout

```tsx
// Flexbox
<div className="flex items-center justify-between gap-4">
  <div className="flex-1">Content</div>
  <div className="flex-shrink-0">Sidebar</div>
</div>

// Grid
<div className="grid grid-cols-3 gap-4">
  <div>1</div>
  <div>2</div>
  <div>3</div>
</div>

// Positioning
<div className="relative">
  <div className="absolute top-0 right-0">Badge</div>
</div>
```

## Spacing

```tsx
// Padding and Margin
<div className="p-4 m-2">           {/* padding: 1rem, margin: 0.5rem */}
<div className="px-6 py-4">        {/* padding-x: 1.5rem, padding-y: 1rem */}
<div className="mt-8 mb-4">        {/* margin-top: 2rem, margin-bottom: 1rem */}

// Space between children
<div className="space-y-4">        {/* margin-bottom on all but last child */}
  <div>Item 1</div>
  <div>Item 2</div>
</div>
```

## Typography

```tsx
<h1 className="text-4xl font-bold text-gray-900">Heading</h1>
<p className="text-base font-normal text-gray-600 leading-relaxed">
  Paragraph text with comfortable line height.
</p>
<span className="text-sm font-medium text-blue-600">Label</span>
```

## Colors

```tsx
// Text colors
<p className="text-gray-900 dark:text-gray-100">Text</p>

// Background colors
<div className="bg-blue-500 hover:bg-blue-600">Button</div>

// Border colors
<div className="border border-gray-300">Box</div>
```
