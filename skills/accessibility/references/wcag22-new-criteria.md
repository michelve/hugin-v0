# WCAG 2.2 New Criteria — Implementation Guide

WCAG 2.2 added 9 success criteria not present in WCAG 2.1. This file provides detailed implementation guidance for each one in the context of React 19 + shadcn/ui + Tailwind CSS v4.

**Required (AA):** 2.4.11 · 2.5.7 · 2.5.8 · 3.2.6 · 3.3.7 · 3.3.8
**Aspirational (AAA):** 2.4.12 · 2.4.13 · 3.3.9

---

## Contents

- [2.4.11 Focus Not Obscured (Minimum) — AA](#2411-focus-not-obscured-minimum--aa-required)
- [2.4.12 Focus Not Obscured (Enhanced) — AAA](#2412-focus-not-obscured-enhanced--aaa-aspirational)
- [2.4.13 Focus Appearance — AAA](#2413-focus-appearance--aaa-aspirational)
- [2.5.7 Dragging Movements — AA](#257-dragging-movements--aa-required)
- [2.5.8 Target Size (Minimum) — AA](#258-target-size-minimum--aa-required)
- [3.2.6 Consistent Help — A](#326-consistent-help--a-required)
- [3.3.7 Redundant Entry — A](#337-redundant-entry--a-required)
- [3.3.8 Accessible Authentication (Minimum) — AA](#338-accessible-authentication-minimum--aa-required)
- [3.3.9 Accessible Authentication (Enhanced) — AAA](#339-accessible-authentication-enhanced--aaa-aspirational)

---

## 2.4.11 Focus Not Obscured (Minimum) — AA (Required)

### Requirement

When a keyboard-operable component receives focus, it is not entirely hidden by author-created content (cookie banners, sticky headers, sticky footers, floating action buttons). The component may be partially obscured, but the focused element must not be **completely** hidden.

### The Problem

A user navigating by keyboard reaches a link at the top of the page content. The sticky site header is 64px tall and the link scrolls under it — visually the focused link is completely hidden behind the header. The user has no way to see what they are interacting with.

### Implementation

**Global CSS approach** — add a `scroll-margin-top` value that matches the height of your sticky header:

```css
/* src/client/index.css */

/* Match this value to your sticky header height.
   If the header is 64px (h-16), use scroll-margin-top: 4.5rem to add a buffer. */
*:focus-visible {
  scroll-margin-top: 5rem; /* 80px — clears a 64px header with a small buffer */
}
```

**Tailwind per-element approach** — when a specific element needs a larger or smaller offset:

```tsx
// On the focusable element, not the container
<a
  href="/about"
  className="focus-visible:scroll-mt-20 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
>
  About us
</a>
```

**Reading the sticky header height dynamically:**

```tsx
// src/client/hooks/useHeaderHeight.ts
import { useEffect, useState } from "react";

export function useHeaderHeight(): number {
  const [height, setHeight] = useState(64); // sensible default
  useEffect(() => {
    const header = document.querySelector("header");
    if (!header) return;
    const observer = new ResizeObserver(([entry]) => {
      setHeight(entry.contentRect.height);
    });
    observer.observe(header);
    return () => observer.disconnect();
  }, []);
  return height;
}
```

```tsx
// Inject as CSS custom property so all :focus-visible rules inherit it
export function AppLayout({ children }: { children: React.ReactNode }) {
  const headerHeight = useHeaderHeight();
  return (
    <div style={{ "--header-height": `${headerHeight}px` } as React.CSSProperties}>
      <header className="sticky top-0 z-50 h-16">...</header>
      <main id="main-content" tabIndex={-1}>
        {children}
      </main>
    </div>
  );
}
```

```css
/* src/client/index.css */
*:focus-visible {
  scroll-margin-top: calc(var(--header-height, 64px) + 1rem);
}
```

### Common Failures

- **Fail:** Setting `overflow: hidden` on a container that clips the focused element
- **Fail:** Sticky footer that covers footer links when they are focused
- **Fail:** Cookie consent banner (fixed at top/bottom) that fully covers focused elements behind it
- **Fail:** Using `scroll-behavior: smooth` without `scroll-margin-top` — smooth scrolling reaches the exact top of the element which may already be behind the sticky header

### How to Test

1. Open the page using keyboard only (Tab key to navigate)
2. Tab through all interactive elements in the main content area
3. Verify the focused element is never **completely** hidden behind the sticky header, footer, or any fixed overlay
4. In DevTools, check the element's computed `scroll-margin-top` value
5. Resize the window to trigger content reflow and retest

---

## 2.4.12 Focus Not Obscured (Enhanced) — AAA (Aspirational)

### Requirement

Same as 2.4.11 but **no part** of the focused component may be obscured by author-created content. The focused element must be **fully visible** — not just partially visible.

### Implementation

Increase `scroll-margin-top` by the full height of the sticky element plus a comfortable buffer:

```css
/* AAA — use a larger margin so the entire focused element is visible above the header */
*:focus-visible {
  scroll-margin-top: calc(var(--header-height, 64px) + 2rem); /* 2rem buffer */
}
```

For sticky footers or bottom toolbars, also add `scroll-margin-bottom`:

```css
*:focus-visible {
  scroll-margin-top: calc(var(--header-height, 64px) + 1rem);
  scroll-margin-bottom: calc(var(--footer-toolbar-height, 0px) + 1rem);
}
```

### How to Test

Same steps as 2.4.11, but verify the **entire** focused element — including all borders and focus rings — is visible, not just a portion of it.

---

## 2.4.13 Focus Appearance — AAA (Aspirational)

### Requirement

Keyboard focus indicators must:
1. Have a **perimeter** (area of focus indicator) that is at least as large as a **2px perimeter** of the focused component
2. Have a **contrast ratio of at least 3:1** between focused and unfocused states

This does not mandate a specific style — it mandates minimum visibility.

### Implementation

The project focus ring (`focus-visible:ring-[3px]` with `--ring` token) should already meet this criterion, but verify the ring contrast against both light and dark backgrounds.

```tsx
// ✔ Meets 2.4.13 — 3px ring with ring color vs background
<button
  className={cn(
    "rounded-md px-4 py-2",
    "focus-visible:outline-none",
    "focus-visible:ring-[3px]",
    "focus-visible:ring-ring/50", // --ring token must be 3:1 against --background
  )}
/>
```

**Checking ring contrast:** In `src/client/index.css`, look up `--ring` in `oklch()`. Convert this to hex and run through [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) against the background color (`--background`). The result must be ≥ 3:1.

**High-contrast mode support:**

```css
/* src/client/index.css */
@media (prefers-contrast: more) {
  :root {
    --ring: oklch(0 0 0); /* solid black ring in high-contrast mode */
  }
  .dark {
    --ring: oklch(1 0 0); /* solid white ring in dark + high-contrast */
  }
}

/* Force 2px solid outline in Windows High Contrast mode (forced-colors) */
@media (forced-colors: active) {
  *:focus-visible {
    outline: 2px solid ButtonText;
    outline-offset: 2px;
  }
}
```

### Common Failures

- **Fail:** Focus ring with `opacity: 0.3` — may drop below 3:1 contrast ratio
- **Fail:** 1px dotted outline — does not meet the 2px perimeter requirement
- **Fail:** Focus ring that matches the element's background color

### How to Test

1. Navigate to all interactive elements by keyboard and observe the focus ring
2. Use browser DevTools color picker to sample the ring color and the unfocused background
3. Check contrast ratio — must be ≥ 3:1

---

## 2.5.7 Dragging Movements — AA (Required)

### Requirement

All functionality that uses a dragging motion for its operation can also be achieved with a single pointer (click, tap) without dragging. This applies to drag-and-drop reordering, sliders operated by dragging, drawing tools, etc.

Exception: The drag operation is **essential** and the outcome cannot be otherwise achieved (e.g., signature fields).

### The Problem

A user with a motor disability who uses a switch access device or voice control software cannot reliably perform a press-and-drag gesture. They need an alternative (for example, buttons) to reorder a list.

### Implementation

**Drag-to-reorder list with move-up/move-down buttons:**

```tsx
// src/client/components/SortableList.tsx
import { useState } from "react";
import { Button } from "@/components/ui/button";

interface Item {
  id: string;
  label: string;
}

interface SortableListProps {
  initialItems: Item[];
  onReorder: (items: Item[]) => void;
}

export function SortableList({ initialItems, onReorder }: SortableListProps) {
  const [items, setItems] = useState(initialItems);

  function move(fromIndex: number, toIndex: number) {
    if (toIndex < 0 || toIndex >= items.length) return;
    const next = [...items];
    const [removed] = next.splice(fromIndex, 1);
    next.splice(toIndex, 0, removed);
    setItems(next);
    onReorder(next);
  }

  return (
    <ul
      role="listbox"
      aria-label="Reorderable list"
      className="space-y-2"
    >
      {items.map((item, index) => (
        <li
          key={item.id}
          role="option"
          aria-selected={false}
          className="flex items-center gap-2 rounded-md border px-3 py-2"
          // Drag-and-drop wiring (e.g., @dnd-kit/core)
          draggable
          aria-roledescription="draggable item"
        >
          {/* Drag handle — still present for pointer users */}
          <span aria-hidden="true" className="cursor-grab text-muted-foreground">⠿</span>

          <span className="flex-1">{item.label}</span>

          {/* ✔ Single-pointer alternatives (WCAG 2.5.7 AA) */}
          <div className="flex gap-1" role="group" aria-label={`Move ${item.label}`}>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => move(index, index - 1)}
              disabled={index === 0}
              aria-label={`Move ${item.label} up`}
              className="h-7 w-7"
            >
              ↑
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => move(index, index + 1)}
              disabled={index === items.length - 1}
              aria-label={`Move ${item.label} down`}
              className="h-7 w-7"
            >
              ↓
            </Button>
          </div>
        </li>
      ))}
    </ul>
  );
}
```

**Custom range slider with increment/decrement buttons:**

```tsx
// ✔ Slider + button alternative
<div className="flex items-center gap-2">
  <Button
    variant="outline"
    size="icon"
    onClick={() => setValue(v => Math.max(min, v - step))}
    aria-label={`Decrease ${label} by ${step}`}
  >–</Button>

  <Slider
    value={[value]}
    onValueChange={([v]) => setValue(v)}
    min={min}
    max={max}
    step={step}
    aria-label={label}
    className="w-48"
  />

  <Button
    variant="outline"
    size="icon"
    onClick={() => setValue(v => Math.min(max, v + step))}
    aria-label={`Increase ${label} by ${step}`}
  >+</Button>
</div>
```

### Common Failures

- **Fail:** Drag-to-sort list with no button/keyboard mechanism to change order
- **Fail:** Custom image-cropping tool where dragging the crop handles is the only interaction
- **Fail:** Map pan that only supports click-and-drag (if custom-built, not a third-party embed)

### How to Test

1. Identify every feature that accepts a dragging gesture
2. Confirm an alternative single-pointer action exists (a button, a keyboard shortcut surfaced in the UI) that achieves the same result
3. Test the alternative using only Tab + Enter/Space (keyboard only)

---

## 2.5.8 Target Size (Minimum) — AA (Required)

### Requirement

The size of the target for pointer inputs is at least **24×24 CSS pixels**, with exceptions:
- **Spacing exception:** If there is at least 24px of spacing between the target boundary and any adjacent same-row target, the target itself can be smaller
- **Inline exception:** Text links in a sentence are exempt
- **User agent exception:** Size is determined by the browser/OS (checkboxes styled by the OS)
- **Essential exception:** The size is essential to the information conveyed (e.g., a simulation of a real-world control)

> **(AAA — 2.5.5 Target Size Enhanced):** Targets should be ≥ 44×44 CSS pixels.

### Implementation

**Tailwind utilities:**

```tsx
// ✔ 24×24px minimum (AA) — use these everywhere
<button className="min-h-6 min-w-6 p-1">
  <XIcon aria-hidden="true" className="h-4 w-4" />
</button>

// ✔ 44×44px recommended (AAA) — primary actions should aim for this
<button className="min-h-[44px] min-w-[44px] px-4 py-2">
  Save
</button>
```

**Icon button with invisible tap area (common pattern for icon-dense UIs):**

```tsx
// The visible icon is 16×16 but the hit area is 32×32
<button
  aria-label="Remove tag"
  className={cn(
    // Invisible hit area — large enough for touch
    "relative inline-flex items-center justify-center",
    "min-h-8 min-w-8",              // 32×32 hit area
    "rounded-full",
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
    // No visible padding — icon appears tight
    "p-0",
  )}
>
  <XIcon aria-hidden="true" className="h-4 w-4" /> {/* 16×16 visual icon */}
</button>
```

**Audit common problem areas:**

| Component | Default Size | Fix |
|-----------|-------------|-----|
| Close (×) icon button | 16×16 typically | Add `min-h-6 min-w-6` or `min-h-8 min-w-8` |
| Tag/chip delete button | often 12×12 | Wrap in `<button className="min-h-6 min-w-6">` |
| Checkbox | OS-rendered (exempt) | — |
| Table row action icons | often 20×20 | Add `p-1` padding to reach 24px min |
| Pagination dots | often 8×8 | Use `min-h-6 min-w-6` + `p-1` |
| Inline text links | exempt (inline text) | No change needed |

### Common Failures

- **Fail:** Icon buttons sized only by the icon (`h-4 w-4` = 16px) without added padding
- **Fail:** Close button on dismissible chips/badges with no surrounding clickable area
- **Fail:** Custom radio button dots that are only styled circles without a larger click target

### How to Test

1. In DevTools, inspect each interactive element and check its **box model** dimensions (border box, not content box)
2. Width and height must both be ≥ 24px (unless a spacing or inline exception applies)
3. On mobile, use DevTools device emulation and check touch target sizes
4. Run `npx axe` or use the axe browser extension — it checks target size

---

## 3.2.6 Consistent Help — A (Required)

### Requirement

If a help mechanism (contact page, phone number, live chat button, FAQ link, human agent access) is present on multiple pages of a website, it occurs in the **same relative location** across those pages.

This is an A-level criterion — it must be met.

### Implementation

Place help links/features in the application shell (AppLayout), not inside individual page components. This guarantees the same relative position:

```tsx
// src/client/components/AppLayout.tsx
export function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-50 h-16 border-b bg-background">
        <MainNav />
      </header>

      <main id="main-content" tabIndex={-1} className="flex-1">
        {children}
      </main>

      {/* ✔ Help links always in the same footer position across all pages */}
      <footer className="border-t bg-muted py-8">
        <nav aria-label="Help and support">
          <ul className="flex gap-4">
            <li>
              <a href="/faq">FAQ</a>
            </li>
            <li>
              <a href="/contact">Contact us</a>
            </li>
            <li>
              <a href="tel:+15555551234">+1 (555) 555-1234</a>
            </li>
          </ul>
        </nav>
      </footer>
    </div>
  );
}
```

**Persistent help widget (fixed position):**

```tsx
// Fixed position maintains the same location regardless of page content
<button
  aria-label="Open help chat"
  className={cn(
    "fixed bottom-6 right-6 z-50",
    "h-12 w-12 rounded-full",
    "bg-primary text-primary-foreground shadow-lg",
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
  )}
>
  <MessageCircleIcon aria-hidden="true" className="h-5 w-5" />
</button>
```

### Common Failures

- **Fail:** "Contact us" in the top-right nav on the home page but in the footer on all other pages
- **Fail:** Live chat widget present on product pages but absent from checkout/payment pages
- **Fail:** Help phone number visible only on the error pages, not throughout the application

### How to Test

1. Visit at least 3 different pages of the application
2. Identify every help mechanism on page 1 (chat, FAQ link, phone number, contact link)
3. Confirm each mechanism appears in the same visual location on the other pages

---

## 3.3.7 Redundant Entry — A (Required)

### Requirement

Information that was previously entered by the user, and that is required again in the same process/session, is either **auto-populated** or **available for the user to select** (e.g., from a dropdown of previously used values). The user must not be required to type the same information twice.

### The Problem

A checkout flow asks for shipping address on Step 2, then asks for billing address on Step 3. If shipping = billing, the user must re-type the entire address. This is a burden for users with cognitive disabilities or motor impairments.

### Implementation

**Multi-step form with auto-populate (sameAsShipping pattern):**

```tsx
// src/client/components/CheckoutBilling.tsx
import { useEffect } from "react";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

interface CheckoutData {
  shipping: AddressData;
  billing: AddressData;
}

interface CheckoutBillingProps {
  formData: CheckoutData;
  onChange: (field: keyof CheckoutData, value: AddressData) => void;
}

export function CheckoutBilling({ formData, onChange }: CheckoutBillingProps) {
  const [sameAsShipping, setSameAsShipping] = useState(false);

  useEffect(() => {
    if (sameAsShipping) {
      // ✔ Auto-populate billing from already-entered shipping data (WCAG 3.3.7 A)
      onChange("billing", { ...formData.shipping });
    }
  }, [sameAsShipping, formData.shipping, onChange]);

  return (
    <fieldset>
      <legend className="text-lg font-semibold">Billing address</legend>

      {/* ✔ Offer to reuse previously entered data */}
      <div className="flex items-center gap-2 mb-4">
        <Checkbox
          id="same-as-shipping"
          checked={sameAsShipping}
          onCheckedChange={(checked) => setSameAsShipping(Boolean(checked))}
        />
        <Label htmlFor="same-as-shipping">
          Same as shipping address
        </Label>
      </div>

      {/* Address fields — pre-filled if sameAsShipping is checked */}
      <AddressFields
        value={formData.billing}
        onChange={(value) => onChange("billing", value)}
        readOnly={sameAsShipping}
      />
    </fieldset>
  );
}
```

**Session-level reuse (profile data):**

```tsx
// Auto-populate from user profile on first use in session
function PersonalInfoStep({ profileData }: { profileData: UserProfile }) {
  const [formData, setFormData] = useState({
    firstName: profileData?.firstName ?? "",
    lastName: profileData?.lastName ?? "",
    email: profileData?.email ?? "",
  });

  // Pre-fill note for screen readers
  return (
    <form>
      <p role="note" className="text-sm text-muted-foreground mb-4">
        Fields have been pre-filled from your profile. Review and update as needed.
      </p>
      {/* form fields */}
    </form>
  );
}
```

### Common Failures

- **Fail:** Multi-step shipping + billing address forms with no "same as shipping" checkbox
- **Fail:** Account registration followed by profile setup that asks for name/email again
- **Fail:** Filtering/search results that clear the filter when navigating back to the page

### How to Test

1. Identify multi-step processes that collect similar information across steps
2. Enter data in step N-1
3. Proceed to step N and verify the previously entered data is either pre-filled or selectable
4. Confirm the auto-populated data is correct and can be edited

---

## 3.3.8 Accessible Authentication (Minimum) — AA (Required)

### Requirement

Authentication processes (login, account creation, step-up verification) must **not require users to solve or recall a cognitive function test** unless:
- A **supported alternative** is available (e.g., email magic link)
- An **assistance mechanism** is provided (e.g., copy/paste is not blocked, password manager injection works)
- The test is essential

**Specifically required:**
- Allow paste into password fields
- Do not block password managers from auto-filling
- Provide an alternative to image-based CAPTCHA (audio CAPTCHA counts as alternative)
- Do not require memorizing or transcribing codes

### Implementation

**Password input — allow paste and password managers:**

```tsx
// src/client/components/PasswordInput.tsx
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { EyeIcon, EyeOffIcon } from "lucide-react";

interface PasswordInputProps {
  id: string;
  label: string;
  autoComplete: "current-password" | "new-password";
  value: string;
  onChange: (value: string) => void;
}

export function PasswordInput({ id, label, autoComplete, value, onChange }: PasswordInputProps) {
  const [visible, setVisible] = useState(false);

  return (
    <div>
      <label htmlFor={id} className="text-sm font-medium">
        {label}
      </label>
      <div className="relative mt-1">
        <Input
          id={id}
          type={visible ? "text" : "password"}
          autoComplete={autoComplete}
          // ✔ Do NOT add: onPaste={e => e.preventDefault()} — WCAG 3.3.8 AA
          // ✔ Do NOT add: readOnly or disabled without clear UX reason
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="pr-10"
          aria-describedby={`${id}-hint`}
        />
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="absolute right-1 top-1/2 -translate-y-1/2 h-7 w-7"
          onClick={() => setVisible((v) => !v)}
          aria-label={visible ? "Hide password" : "Show password"}
          aria-pressed={visible}
        >
          {visible ? (
            <EyeOffIcon aria-hidden="true" className="h-4 w-4" />
          ) : (
            <EyeIcon aria-hidden="true" className="h-4 w-4" />
          )}
        </Button>
      </div>
      <p id={`${id}-hint`} className="mt-1 text-xs text-muted-foreground">
        Use a password manager to auto-fill securely.
      </p>
    </div>
  );
}
```

**Magic link / email OTP as CAPTCHA alternative:**

```tsx
// src/client/components/LoginForm.tsx — offer magic link as alternative
export function LoginForm() {
  const [mode, setMode] = useState<"password" | "magic-link">("password");

  return (
    <form>
      {/* Tab switcher between password login and passwordless email */}
      <Tabs value={mode} onValueChange={(v) => setMode(v as typeof mode)}>
        <TabsList>
          <TabsTrigger value="password">Password</TabsTrigger>
          <TabsTrigger value="magic-link">Email link (no password)</TabsTrigger>
        </TabsList>
        <TabsContent value="password">
          <PasswordInput
            id="password"
            label="Password"
            autoComplete="current-password"
            value={password}
            onChange={setPassword}
          />
          {/* ✔ No CAPTCHA that is purely cognitive — use invisible hCaptcha or reCAPTCHA v3
              If CAPTCHA is required: always provide audio alternative */}
        </TabsContent>
        <TabsContent value="magic-link">
          {/* No password, no CAPTCHA — just email a secure link */}
          <p className="text-sm text-muted-foreground">
            Enter your email to receive a sign-in link — no password needed.
          </p>
          <Input type="email" autoComplete="email" placeholder="you@example.com" />
        </TabsContent>
      </Tabs>
    </form>
  );
}
```

### Common Failures

- **Fail:** `onPaste={e => e.preventDefault()}` on any password or code input
- **Fail:** Using `autocomplete="off"` on a password field — this blocks password managers
- **Fail:** A CAPTCHA with no audio alternative for users who cannot see images
- **Fail:** Requiring users to type a 6-digit OTP from memory without a paste-allowed input
- **Fail:** Blocking browser auto-fill via `autocomplete="off"` on login forms

### How to Test

1. On the login form, copy a password from a password manager and paste it — it must work
2. Check that `autocomplete="current-password"` is set on the password field
3. Verify paste is not blocked on any auth input field
4. Check that any image-based verification has an audio alternative

---

## 3.3.9 Accessible Authentication (Enhanced) — AAA (Aspirational)

### Requirement

Same as 3.3.8 but **without any exceptions** — no cognitive function test is allowed in any authentication step, even if an alternative exists. This means no CAPTCHA of any kind, no transcription, no image matching.

### Implementation

The only WCAG conformant AAA-level approach is to use authentication methods that do not require any cognitive test:

```tsx
// ✔ AAA — Passkeys (WebAuthn) — no passwords, no CAPTCHA, no memory required
async function signInWithPasskey() {
  const credential = await navigator.credentials.get({
    publicKey: {
      challenge: await fetchChallenge(), // server-generated
      rpId: window.location.hostname,
      userVerification: "required",
      timeout: 60_000,
    },
  });
  await sendCredentialToServer(credential);
}

// ✔ AAA — SSO / OAuth (Google, Microsoft, GitHub)
<Button onClick={() => signIn("google")}>
  Sign in with Google
</Button>

// ✔ AAA — Magic link / email OTP with no manual transcription
// (User clicks link in email — no typing required)
```

**Auth strategy table:**

| Method | AA (3.3.8) | AAA (3.3.9) |
|--------|-----------|------------|
| Password + paste allowed | ✔ | ✗ |
| Password + CAPTCHA (with audio alt) | ✔ | ✗ |
| Password + CAPTCHA (no alt) | ✗ | ✗ |
| Email magic link | ✔ | ✔ |
| Passkeys / WebAuthn | ✔ | ✔ |
| Google/Microsoft SSO | ✔ | ✔ |
| SMS OTP (pasted) | ✔ | ✗ |
| SMS OTP (typed from memory) | ✗ | ✗ |

### How to Test

Review the entire authentication flow. Identify any step that requires:
- Memorizing a code or password
- Recognizing or transcribing characters (CAPTCHA)
- Matching images

If any such step exists, the page fails AAA. Provide passkey, SSO, or magic link alternatives.
