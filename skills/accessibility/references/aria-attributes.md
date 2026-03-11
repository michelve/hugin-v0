# ARIA Attributes

## Interactive Elements

```tsx
// Button with state
<button
  aria-expanded={isOpen}
  aria-controls="menu-id"
  aria-haspopup="menu"
>
  Menu
</button>

// Menu
<ul
  id="menu-id"
  role="menu"
  aria-labelledby="button-id"
>
  <li role="menuitem" tabIndex={-1}>Option 1</li>
  <li role="menuitem" tabIndex={-1}>Option 2</li>
</ul>
```

## Form Elements

```tsx
// Input with error
<div>
    <label id="email-label" htmlFor="email">
        Email
    </label>
    <input
        id="email"
        type="email"
        aria-labelledby="email-label"
        aria-describedby="email-error"
        aria-invalid={hasError}
    />
    {hasError && (
        <span id="email-error" role="alert">
            Please enter a valid email
        </span>
    )}
</div>
```

## Live Regions

```tsx
// Announce dynamic content
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Urgent announcements
<div role="alert" aria-live="assertive">
  {errorMessage}
</div>
```
