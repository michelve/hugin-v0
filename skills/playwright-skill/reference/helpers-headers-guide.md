# Available Helpers & Custom HTTP Headers

## Available Helpers

Optional utility functions in `lib/helpers.js`:

```javascript
const helpers = require("./lib/helpers");

// Detect running dev servers (CRITICAL - use this first!)
const servers = await helpers.detectDevServers();
console.log("Found servers:", servers);

// Safe click with retry
await helpers.safeClick(page, "button.submit", { retries: 3 });

// Safe type with clear
await helpers.safeType(page, "#username", "testuser");

// Take timestamped screenshot
await helpers.takeScreenshot(page, "test-result");

// Handle cookie banners
await helpers.handleCookieBanner(page);

// Extract table data
const data = await helpers.extractTableData(page, "table.results");
```

See `lib/helpers.js` for full list.

## Custom HTTP Headers

Configure custom headers for all HTTP requests via environment variables. Useful for:

- Identifying automated traffic to your backend
- Getting LLM-optimized responses (e.g., plain text errors instead of styled HTML)
- Adding authentication tokens globally

### Configuration

**Single header (common case):**

```bash
PW_HEADER_NAME=X-Automated-By PW_HEADER_VALUE=playwright-skill \
  cd $SKILL_DIR && node run.js /tmp/my-script.js
```

**Multiple headers (JSON format):**

```bash
PW_EXTRA_HEADERS='{"X-Automated-By":"playwright-skill","X-Debug":"true"}' \
  cd $SKILL_DIR && node run.js /tmp/my-script.js
```

### How It Works

Headers are automatically applied when using `helpers.createContext()`:

```javascript
const context = await helpers.createContext(browser);
const page = await context.newPage();
// All requests from this page include your custom headers
```

For scripts using raw Playwright API, use the injected `getContextOptionsWithHeaders()`:

```javascript
const context = await browser.newContext(
    getContextOptionsWithHeaders({ viewport: { width: 1920, height: 1080 } }),
);
```
