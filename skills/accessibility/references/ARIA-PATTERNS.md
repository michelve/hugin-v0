# ARIA Patterns Reference

Common ARIA patterns for draft_v0 components (React 19 + shadcn/ui).

## Button Pattern

```tsx
<button
    type="button"
    aria-pressed={isPressed} // For toggle buttons
    aria-expanded={isExpanded} // For buttons that expand/collapse
    aria-haspopup="true" // For menu buttons
    aria-controls="menu-id" // ID of controlled element
    aria-disabled={isDisabled} // When visually disabled but focusable
    disabled={isDisabled} // When truly disabled
>
    Button Label
</button>
```

## Input Pattern

```tsx
<div>
    <label htmlFor="input-id" id="label-id">
        Label Text
    </label>
    <input
        id="input-id"
        type="text"
        aria-labelledby="label-id"
        aria-describedby="help-id error-id"
        aria-required={isRequired}
        aria-invalid={hasError}
        aria-errormessage="error-id"
    />
    <span id="help-id">Help text</span>
    {hasError && (
        <span id="error-id" role="alert">
            Error message
        </span>
    )}
</div>
```

## Checkbox Pattern

```tsx
<label>
    <input
        type="checkbox"
        checked={isChecked}
        aria-checked={isChecked} // For custom checkboxes
        aria-describedby="desc-id"
    />
    <span>Checkbox Label</span>
</label>
```

## Radio Group Pattern

```tsx
<fieldset>
    <legend>Radio Group Label</legend>
    <div role="radiogroup" aria-labelledby="legend-id">
        <label>
            <input
                type="radio"
                name="group-name"
                value="option1"
                aria-checked={selectedValue === "option1"}
            />
            Option 1
        </label>
        <label>
            <input
                type="radio"
                name="group-name"
                value="option2"
                aria-checked={selectedValue === "option2"}
            />
            Option 2
        </label>
    </div>
</fieldset>
```

## Switch/Toggle Pattern

```tsx
<button
    type="button"
    role="switch"
    aria-checked={isOn}
    aria-label="Toggle feature"
    onClick={toggle}
>
    <span aria-hidden="true">{isOn ? "ON" : "OFF"}</span>
</button>
```

## Dialog/Modal Pattern

```tsx
<div
    role="dialog"
    aria-modal="true"
    aria-labelledby="dialog-title"
    aria-describedby="dialog-description"
>
    <h2 id="dialog-title">Dialog Title</h2>
    <p id="dialog-description">Dialog description</p>

    <button type="button" aria-label="Close dialog">
        ×
    </button>

    <div>{/* Dialog content */}</div>

    <footer>
        <button type="button">Cancel</button>
        <button type="submit">Confirm</button>
    </footer>
</div>
```

## Alert Pattern

```tsx
// Assertive alert (interrupts screen reader)
<div role="alert" aria-live="assertive">
  Error: Something went wrong
</div>

// Polite notification (waits for pause)
<div role="status" aria-live="polite">
  Changes saved successfully
</div>
```

## Menu Pattern

```tsx
<div>
    <button type="button" aria-haspopup="true" aria-expanded={isOpen} aria-controls="menu-id">
        Menu
    </button>

    <ul id="menu-id" role="menu" aria-labelledby="menu-button-id" hidden={!isOpen}>
        <li role="menuitem" tabIndex={-1}>
            Option 1
        </li>
        <li role="menuitem" tabIndex={-1}>
            Option 2
        </li>
        <li role="separator" aria-hidden="true" />
        <li role="menuitem" tabIndex={-1}>
            Option 3
        </li>
    </ul>
</div>
```

## Tabs Pattern

```tsx
<div>
    <div role="tablist" aria-label="Tab navigation">
        <button
            role="tab"
            aria-selected={activeTab === 0}
            aria-controls="panel-0"
            id="tab-0"
            tabIndex={activeTab === 0 ? 0 : -1}
        >
            Tab 1
        </button>
        <button
            role="tab"
            aria-selected={activeTab === 1}
            aria-controls="panel-1"
            id="tab-1"
            tabIndex={activeTab === 1 ? 0 : -1}
        >
            Tab 2
        </button>
    </div>

    <div role="tabpanel" id="panel-0" aria-labelledby="tab-0" hidden={activeTab !== 0} tabIndex={0}>
        Panel 1 content
    </div>
    <div role="tabpanel" id="panel-1" aria-labelledby="tab-1" hidden={activeTab !== 1} tabIndex={0}>
        Panel 2 content
    </div>
</div>
```

## Accordion Pattern

```tsx
<div>
    <h3>
        <button
            type="button"
            aria-expanded={isExpanded}
            aria-controls="section-content"
            id="section-header"
        >
            Section Title
        </button>
    </h3>
    <div id="section-content" role="region" aria-labelledby="section-header" hidden={!isExpanded}>
        Section content
    </div>
</div>
```

## Tooltip Pattern

```tsx
<div>
    <button
        type="button"
        aria-describedby="tooltip-id"
        onMouseEnter={showTooltip}
        onMouseLeave={hideTooltip}
        onFocus={showTooltip}
        onBlur={hideTooltip}
    >
        Hover me
    </button>

    <div id="tooltip-id" role="tooltip" hidden={!isVisible}>
        Tooltip content
    </div>
</div>
```

## Progress Pattern

```tsx
// Determinate progress
<div
  role="progressbar"
  aria-valuenow={progress}
  aria-valuemin={0}
  aria-valuemax={100}
  aria-label="Upload progress"
>
  {progress}%
</div>

// Indeterminate progress
<div
  role="progressbar"
  aria-label="Loading"
  aria-busy="true"
>
  <span className="spinner" aria-hidden="true" />
</div>
```

## Live Region Pattern

```tsx
// For dynamic content updates
<div
    aria-live="polite" // or "assertive" for urgent
    aria-atomic="true" // Announce entire region
    aria-relevant="additions text" // What changes to announce
>
    {/* Dynamic content */}
</div>
```

## Table Pattern

```tsx
<table aria-labelledby="table-caption">
    <caption id="table-caption">Table Title</caption>
    <thead>
        <tr>
            <th scope="col">Column 1</th>
            <th scope="col">Column 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th scope="row">Row 1</th>
            <td>Data</td>
        </tr>
    </tbody>
</table>
```

## Keyboard Navigation Reference

| Component | Key              | Action                |
| --------- | ---------------- | --------------------- |
| Button    | Enter, Space     | Activate              |
| Checkbox  | Space            | Toggle                |
| Radio     | Arrow Up/Down    | Select prev/next      |
| Menu      | Arrow Down       | Open menu / next item |
| Menu      | Arrow Up         | Previous item         |
| Menu      | Escape           | Close menu            |
| Tabs      | Arrow Left/Right | Switch tabs           |
| Dialog    | Escape           | Close dialog          |
| Dialog    | Tab              | Cycle focus within    |

## Screen Reader Announcements

```tsx
// Visually hidden but announced
<span className="visually-hidden">
  Screen reader only text
</span>

// Hide from screen readers
<span aria-hidden="true">
  Visual decoration only
</span>

// Announce on change
<div aria-live="polite" aria-atomic="true">
  {count} items selected
</div>
```
