# Framework Examples

## Example 1: React + Tailwind Project

User says: "Create design system rules for my React project"

**Actions:**

1. Run `create_design_system_rules(clientLanguages="typescript,javascript", clientFrameworks="react")`
2. Analyze codebase structure
3. Generate rules:

```markdown
# Figma MCP Integration Rules

## Component Organization

- UI components are in `src/components/ui/`
- Page components are in `src/app/`
- Use Tailwind for styling

## Figma Implementation Flow

1. Run get_design_context for the node
2. Run get_screenshot for visual reference
3. Map Figma colors to Tailwind colors defined in `tailwind.config.js`
4. Reuse components from `src/components/ui/` when possible
5. Validate against screenshot before completing

## Styling Rules

- IMPORTANT: Use Tailwind utility classes, not inline styles
- Colors are defined in `tailwind.config.js` theme.colors
- Spacing uses Tailwind's default scale
- Custom components go in `src/components/ui/`

## Asset Rules

- IMPORTANT: Use localhost sources from Figma MCP server directly
- Store static assets in `public/assets/`
- DO NOT install new icon libraries
```

4. Save to the appropriate rule file for the user's agent
5. Test with a simple button implementation

**Result:** The agent now consistently follows the project's conventions when implementing Figma designs.

## Example 2: Vue + Custom CSS Project

User says: "Set up Figma rules for my Vue app"

**Actions:**

1. Run `create_design_system_rules(clientLanguages="typescript,javascript", clientFrameworks="vue")`
2. Discover that project uses CSS modules and a custom design token system
3. Generate rules:

```markdown
# Figma MCP Integration Rules

## Component Organization

- Components are in `src/components/`
- Composables are in `src/composables/`
- Vue SFC structure: <script setup>, <template>, <style scoped>

## Design Tokens

- IMPORTANT: All colors defined in `src/styles/tokens.css` as CSS variables
- Use `var(--color-primary)`, `var(--color-secondary)`, etc.
- Spacing: `var(--space-xs)` through `var(--space-xl)`
- Typography: `var(--text-sm)` through `var(--text-2xl)`

## Figma Implementation Flow

1. Run get_design_context and get_screenshot
2. Translate React output to Vue 3 Composition API
3. Map Figma colors to CSS variables in `src/styles/tokens.css`
4. Use CSS Modules for component styles
5. Check for existing components in `src/components/` before creating new ones

## Styling Rules

- Use CSS Modules (`.module.css` files)
- IMPORTANT: Reference design tokens, never hardcode values
- Scoped styles with CSS modules
```

4. Save to the appropriate rule file for the user's agent
5. Validate with a card component

**Result:** The agent now correctly translates Figma designs to Vue components using the project's design token system.

## Example 3: Design System Team

User says: "Generate rules for our design system library"

**Actions:**

1. Run `create_design_system_rules(clientLanguages="typescript", clientFrameworks="react")`
2. Analyze the monorepo structure with design system package
3. Generate comprehensive rules:

```markdown
# Design System Rules

## Repository Structure

- Design system components: `packages/design-system/src/components/`
- Documentation: `packages/docs/`
- Design tokens: `packages/tokens/src/`

## Component Development

- IMPORTANT: All components must be in `packages/design-system/src/components/`
- Component file structure: `ComponentName/index.tsx`, `ComponentName.stories.tsx`, `ComponentName.test.tsx`
- Export all components from `packages/design-system/src/index.ts`

## Design Tokens

- Colors: `packages/tokens/src/colors.ts`
- Typography: `packages/tokens/src/typography.ts`
- Spacing: `packages/tokens/src/spacing.ts`
- IMPORTANT: Never hardcode values - import from tokens package

## Documentation Requirements

- Add Storybook story for every component
- Include JSDoc with @example
- Document all props with descriptions
- Add accessibility notes

## Figma Integration

1. Get design context and screenshot from Figma
2. Map Figma tokens to design system tokens
3. Create or extend component in design system package
4. Add Storybook stories showing all variants
5. Validate against Figma screenshot
6. Update documentation
```

4. Save to the appropriate rule file and share with team
5. Add to team documentation

**Result:** Entire team follows consistent patterns when adding components from Figma to the design system.
