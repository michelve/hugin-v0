# Forms Accessibility — Reference

Accessible forms work correctly for keyboard users, screen reader users, and users with cognitive and motor disabilities. This reference covers WCAG conformant implementation for all common form patterns in React 19 with shadcn/ui.

## Contents

- [Labels](#labels)
- [autocomplete Attributes (WCAG 1.3.5 AA)](#autocomplete-attributes-wcag-135-aa)
- [Required Fields](#required-fields)
- [Error Handling (WCAG 3.3.1 A / 3.3.3 AA)](#error-handling-wcag-331-a--error-identification-333-aa--error-suggestion)
- [Grouped Inputs — fieldset / legend](#grouped-inputs--fieldset--legend)
- [Character Count (Textarea)](#character-count-textarea)
- [Multi-step Forms](#multi-step-forms)
- [Redundant Entry (WCAG 3.3.7 A)](#redundant-entry-wcag-337-a)
- [Accessible Authentication (WCAG 3.3.8 AA)](#accessible-authentication-wcag-338-aa)
- [Form Submission Feedback](#form-submission-feedback)
- [Search Forms](#search-forms)

---

## Labels

Every input **must** have an associated label. Do not rely on `placeholder` alone — it disappears when the user types.

```tsx
// ✔ Visible label — preferred approach
<div className="space-y-2">
  <Label htmlFor="email">Email address</Label>
  <Input id="email" type="email" autoComplete="email" />
</div>

// ✔ Visible label with required indicator
<div className="space-y-2">
  <Label htmlFor="first-name">
    First name
    <span aria-hidden="true" className="ml-1 text-destructive">*</span>
    <span className="sr-only">(required)</span>
  </Label>
  <Input
    id="first-name"
    type="text"
    autoComplete="given-name"
    required
    aria-required="true"
  />
</div>

// ✔ Visually-hidden label (search field where placeholder is sufficient for most users)
<div className="relative">
  <Label htmlFor="site-search" className="sr-only">Search the site</Label>
  <Input
    id="site-search"
    type="search"
    placeholder="Search…"
    autoComplete="off"
  />
</div>
```

---

## autocomplete Attributes (WCAG 1.3.5 AA)

Input fields that collect personal information **must** have the appropriate `autocomplete` attribute. This allows browsers and password managers to auto-fill, benefiting users with cognitive disabilities and motor impairments.

| Input Type | autocomplete Value |
|-----------|-------------------|
| Full name | `name` |
| Given (first) name | `given-name` |
| Family (last) name | `family-name` |
| Email address | `email` |
| Phone number | `tel` |
| Street address | `street-address` |
| Address line 2 | `address-line2` |
| City | `address-level2` |
| State/Province | `address-level1` |
| ZIP/Postal code | `postal-code` |
| Country | `country-name` |
| Current password | `current-password` |
| New password | `new-password` |
| One-time code | `one-time-code` |
| Credit card number | `cc-number` |
| Credit card expiry | `cc-exp` |
| Credit card CVV | `cc-csc` |
| Username | `username` |
| Organization | `organization` |
| Job title | `organization-title` |

```tsx
// ✔ Personal info form with correct autocomplete values
<form>
  <div className="grid grid-cols-2 gap-4">
    <div className="space-y-2">
      <Label htmlFor="given-name">First name</Label>
      <Input id="given-name" type="text" autoComplete="given-name" />
    </div>
    <div className="space-y-2">
      <Label htmlFor="family-name">Last name</Label>
      <Input id="family-name" type="text" autoComplete="family-name" />
    </div>
  </div>
  <div className="space-y-2">
    <Label htmlFor="email-field">Email</Label>
    <Input id="email-field" type="email" autoComplete="email" />
  </div>
  <div className="space-y-2">
    <Label htmlFor="phone">Phone</Label>
    <Input id="phone" type="tel" autoComplete="tel" />
  </div>
</form>
```

---

## Required Fields

Communicate required fields both visually and programmatically:

```tsx
// ✔ Visual indicator + programmatic aria-required + sr-only description
// Mark ALL required fields (or ALL optional fields if most are required)
<div className="space-y-2">
  <Label htmlFor="username-field">
    Username
    <span aria-hidden="true" className="ml-1 text-destructive" title="Required">*</span>
  </Label>
  <Input
    id="username-field"
    type="text"
    autoComplete="username"
    required
    aria-required="true"
    aria-describedby="username-hint"
  />
  <p id="username-hint" className="text-xs text-muted-foreground">
    3–20 characters, letters and numbers only.
  </p>
</div>

{/* Explain the asterisk at the top of the form */}
<p className="text-sm text-muted-foreground">
  Fields marked with <span aria-hidden="true">*</span>
  <span className="sr-only">an asterisk</span> are required.
</p>
```

---

## Error Handling (WCAG 3.3.1 A — Error Identification, 3.3.3 AA — Error Suggestion)

Screen readers must be notified of validation errors. The error must identify the field and describe the problem in text.

### Inline field error pattern

```tsx
// src/client/components/FormField.tsx
import { ReactNode } from "react";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

interface FormFieldProps {
  id: string;
  label: string;
  error?: string;
  hint?: string;
  children?: ReactNode;
  inputProps?: React.InputHTMLAttributes<HTMLInputElement>;
}

export function FormField({ id, label, error, hint, inputProps }: FormFieldProps) {
  const errorId = `${id}-error`;
  const hintId = `${id}-hint`;
  const describedBy = [hint ? hintId : "", error ? errorId : ""].filter(Boolean).join(" ");

  return (
    <div className="space-y-2">
      <Label htmlFor={id}>{label}</Label>

      <Input
        id={id}
        {...inputProps}
        aria-invalid={error ? "true" : undefined}
        aria-describedby={describedBy || undefined}
        className={cn(
          inputProps?.className,
          error && "border-destructive focus-visible:ring-destructive/50",
        )}
      />

      {hint && (
        <p id={hintId} className="text-xs text-muted-foreground">
          {hint}
        </p>
      )}

      {/* role="alert" announces the error immediately when it appears */}
      {error && (
        <p id={errorId} role="alert" className="text-xs text-destructive">
          {error}
        </p>
      )}
    </div>
  );
}
```

```tsx
// Usage
<FormField
  id="email-input"
  label="Email address"
  error={errors.email}
  hint="We'll send a confirmation to this address"
  inputProps={{
    type: "email",
    autoComplete: "email",
    value: email,
    onChange: (e) => setEmail(e.target.value),
  }}
/>
```

### Form-level error summary (for long forms)

When a form has multiple errors, move focus to an error summary at the top of the form:

```tsx
// src/client/components/ErrorSummary.tsx
import { useEffect, useRef } from "react";

interface ErrorSummaryProps {
  errors: Record<string, string>;
  formId: string;
}

export function ErrorSummary({ errors, formId }: ErrorSummaryProps) {
  const ref = useRef<HTMLDivElement>(null);
  const errorEntries = Object.entries(errors).filter(([, v]) => v);

  useEffect(() => {
    if (errorEntries.length > 0 && ref.current) {
      // Move focus to the summary so screen reader users hear the error list
      ref.current.focus();
    }
  }, [errorEntries.length]);

  if (errorEntries.length === 0) return null;

  return (
    <div
      ref={ref}
      tabIndex={-1}
      role="alert"
      aria-labelledby={`${formId}-error-heading`}
      className="rounded-md border border-destructive p-4 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
    >
      <h2 id={`${formId}-error-heading`} className="text-sm font-semibold text-destructive">
        There are {errorEntries.length} error{errorEntries.length > 1 ? "s" : ""} in this form:
      </h2>
      <ul className="mt-2 list-disc pl-5 text-sm text-destructive">
        {errorEntries.map(([field, message]) => (
          <li key={field}>
            <a href={`#${field}`} className="underline hover:no-underline">
              {message}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
```

---

## Grouped Inputs — fieldset / legend

Use `<fieldset>` and `<legend>` to group related inputs. Screen readers read the `<legend>` before each field name inside the group.

### Radio group

```tsx
<fieldset className="space-y-3">
  <legend className="text-sm font-medium">Preferred contact method</legend>
  <div className="flex items-center gap-2">
    <input
      type="radio"
      id="contact-email"
      name="contact-method"
      value="email"
      className="h-4 w-4"
    />
    <label htmlFor="contact-email">Email</label>
  </div>
  <div className="flex items-center gap-2">
    <input
      type="radio"
      id="contact-phone"
      name="contact-method"
      value="phone"
      className="h-4 w-4"
    />
    <label htmlFor="contact-phone">Phone</label>
  </div>
  <div className="flex items-center gap-2">
    <input
      type="radio"
      id="contact-post"
      name="contact-method"
      value="post"
      className="h-4 w-4"
    />
    <label htmlFor="contact-post">Post</label>
  </div>
</fieldset>
```

### Grouped address fields

```tsx
<fieldset className="space-y-4 rounded-md border p-4">
  <legend className="px-2 text-sm font-semibold">Shipping address</legend>

  <div className="space-y-2">
    <Label htmlFor="street">Street address</Label>
    <Input id="street" autoComplete="street-address" />
  </div>
  <div className="grid grid-cols-2 gap-4">
    <div className="space-y-2">
      <Label htmlFor="city">City</Label>
      <Input id="city" autoComplete="address-level2" />
    </div>
    <div className="space-y-2">
      <Label htmlFor="postcode">Postal code</Label>
      <Input id="postcode" autoComplete="postal-code" />
    </div>
  </div>
</fieldset>
```

---

## Character Count (Textarea)

```tsx
// src/client/components/TextareaWithCount.tsx
import { useId } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";

interface TextareaWithCountProps {
  label: string;
  maxLength: number;
  value: string;
  onChange: (value: string) => void;
}

export function TextareaWithCount({ label, maxLength, value, onChange }: TextareaWithCountProps) {
  const id = useId();
  const countId = `${id}-count`;
  const remaining = maxLength - value.length;

  return (
    <div className="space-y-2">
      <Label htmlFor={id}>{label}</Label>
      <Textarea
        id={id}
        maxLength={maxLength}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        // Link both the visible count and any fixed hint to this textarea
        aria-describedby={countId}
      />
      {/* role="status" announces count updates politely (not every keystroke) */}
      <p
        id={countId}
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="text-xs text-muted-foreground"
      >
        {remaining} character{remaining === 1 ? "" : "s"} remaining
      </p>
    </div>
  );
}
```

---

## Multi-step Forms

### Progress indication

```tsx
// ✔ Communicate current step to screen readers
<nav aria-label="Form progress">
  <ol className="flex gap-2">
    {steps.map((step, index) => {
      const stepNumber = index + 1;
      const isComplete = stepNumber < currentStep;
      const isCurrent = stepNumber === currentStep;
      return (
        <li
          key={step.id}
          aria-current={isCurrent ? "step" : undefined}
          className={cn(
            "flex items-center gap-1 text-sm",
            isCurrent ? "font-semibold text-primary" : "text-muted-foreground",
          )}
        >
          <span aria-hidden="true">{stepNumber}.</span>
          {step.label}
          {isComplete && <span className="sr-only">(completed)</span>}
          {isCurrent && <span className="sr-only">(current)</span>}
        </li>
      );
    })}
  </ol>
</nav>
```

### State preservation across steps

```tsx
// Keep form data in a parent component — never lose data when navigating between steps
export function MultiStepForm() {
  // Centralized state that persists across step renders
  const [formData, setFormData] = useState<CheckoutFormData>({
    personal: { firstName: "", lastName: "", email: "" },
    shipping: { street: "", city: "", postalCode: "" },
    billing: { street: "", city: "", postalCode: "" },
    payment: { cardNumber: "", expiry: "", cvv: "" },
  });
  const [currentStep, setCurrentStep] = useState(1);

  function updateStep<K extends keyof CheckoutFormData>(
    section: K,
    data: CheckoutFormData[K],
  ) {
    setFormData((prev) => ({ ...prev, [section]: data }));
  }

  return (
    <>
      <StepProgress currentStep={currentStep} totalSteps={4} />

      {/* Each step component receives and updates shared formData */}
      {currentStep === 1 && (
        <PersonalStep
          data={formData.personal}
          onChange={(data) => updateStep("personal", data)}
          onNext={() => setCurrentStep(2)}
        />
      )}
      {currentStep === 2 && (
        <ShippingStep
          data={formData.shipping}
          onChange={(data) => updateStep("shipping", data)}
          onBack={() => setCurrentStep(1)}
          onNext={() => setCurrentStep(3)}
        />
      )}
      {/* … subsequent steps … */}
    </>
  );
}
```

---

## Redundant Entry (WCAG 3.3.7 A)

Data entered in an earlier step must be auto-populated if required again in a later step.

```tsx
// ✔ Billing = Shipping checkbox (sameAsShipping pattern)
export function BillingStep({ formData, onChange }: BillingStepProps) {
  const [sameAsShipping, setSameAsShipping] = useState(false);

  function handleSameAsShipping(checked: boolean) {
    setSameAsShipping(checked);
    if (checked) {
      // Copy shipping data into billing — user must not retype it
      onChange({ ...formData.shipping });
    }
  }

  return (
    <fieldset>
      <legend className="text-lg font-semibold">Billing address</legend>

      <div className="flex items-center gap-2 mb-6">
        <Checkbox
          id="same-as-shipping"
          checked={sameAsShipping}
          onCheckedChange={(c) => handleSameAsShipping(Boolean(c))}
        />
        <Label htmlFor="same-as-shipping">
          Same as shipping address
        </Label>
      </div>

      <AddressFields
        data={formData.billing}
        onChange={onChange}
        readOnly={sameAsShipping}
      />
    </fieldset>
  );
}
```

---

## Accessible Authentication (WCAG 3.3.8 AA)

See [wcag22-new-criteria.md](wcag22-new-criteria.md#338-accessible-authentication-minimum--aa-required) for full implementation.

**Quick rules:**
- Allow paste in all password and OTP fields — **never** add `onPaste={e => e.preventDefault()}`
- Use `autoComplete="current-password"` or `autoComplete="new-password"` on password fields — **never** `autocomplete="off"`
- Provide show/hide password toggle
- Offer a non-cognitive alternative: magic link, passkey, or SSO
- Any image/audio CAPTCHA must have both alternatives for WCAG AA

```tsx
// ✔ Password field — correctly configured
<Input
  id="password"
  type={showPassword ? "text" : "password"}
  autoComplete="current-password"
  // ✔ No onPaste prevention
  // ✔ No autocomplete="off"
  value={password}
  onChange={(e) => setPassword(e.target.value)}
/>
```

---

## Form Submission Feedback

After form submission, communicate success or failure to screen reader users:

```tsx
// ✔ polite announcement via role="status"
{submitState === "success" && (
  <div role="status" aria-live="polite" className="rounded-md bg-green-50 p-4">
    <p className="text-sm font-medium text-green-800">
      Your message has been sent. We'll reply within 24 hours.
    </p>
  </div>
)}

// ✔ Assertive announcement for critical errors (use sparingly)
{submitState === "error" && (
  <div role="alert" className="rounded-md bg-destructive/10 p-4">
    <p className="text-sm font-medium text-destructive">
      Failed to submit. Please check your connection and try again.
    </p>
  </div>
)}
```

---

## Search Forms

```tsx
// ✔ Search uses role="search" (landmark) via <search> element or role attr
<search>
  <form role="search" onSubmit={handleSearch}>
    <Label htmlFor="main-search" className="sr-only">Search products</Label>
    <div className="relative">
      <Input
        id="main-search"
        type="search"
        autoComplete="off"
        placeholder="Search products…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        aria-controls="search-results"   // Points to the results region
        aria-autocomplete="list"          // Indicates suggestion list
        aria-expanded={suggestions.length > 0}
      />
    </div>
  </form>

  {/* Results as a live region */}
  <div id="search-results" aria-live="polite" aria-atomic="false">
    {results.map((result) => (
      <a key={result.id} href={result.url}>{result.title}</a>
    ))}
  </div>
</search>

{/* Announce result count for screen readers */}
<div role="status" className="sr-only">
  {results.length} result{results.length !== 1 ? "s" : ""} found
</div>
```
