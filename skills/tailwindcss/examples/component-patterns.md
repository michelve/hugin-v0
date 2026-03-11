# Component Patterns

## Button

```tsx
<button className="px-4 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
  Click me
</button>

// Variants
<button className="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50">
  Secondary
</button>
```

## Card

```tsx
<div className="overflow-hidden rounded-lg bg-white shadow-md">
    <img src="/image.jpg" alt="" className="h-48 w-full object-cover" />
    <div className="p-6">
        <h2 className="mb-2 text-xl font-semibold">Card Title</h2>
        <p className="text-gray-600">Card content goes here.</p>
    </div>
</div>
```

## Form Input

```tsx
<div className="space-y-2">
    <label htmlFor="email" className="block text-sm font-medium text-gray-700">
        Email
    </label>
    <input
        type="email"
        id="email"
        className="w-full rounded-md border border-gray-300 px-3 py-2 focus:border-transparent focus:ring-2 focus:ring-blue-500 focus:outline-none"
        placeholder="you@example.com"
    />
    <p className="text-sm text-gray-500">We'll never share your email.</p>
</div>
```
