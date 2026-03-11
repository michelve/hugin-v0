# Common Issues and Solutions

## Issue: "No published components found in this selection"

**Cause:** The Figma component is not published to a team library. Code Connect only works with published components.
**Solution:** The user needs to publish the component to a team library in Figma:

1. In Figma, select the component or component set
2. Right-click and choose "Publish to library" or use the Team Library publish modal
3. Publish the component
4. Once published, retry the Code Connect mapping with the same node ID

## Issue: "Code Connect is only available on Organization and Enterprise plans"

**Cause:** The user's Figma plan does not include Code Connect access.
**Solution:** The user needs to upgrade to an Organization or Enterprise plan, or contact their administrator.

## Issue: No matching component found in codebase

**Cause:** The codebase search did not find a component with a matching name or structure.
**Solution:** Ask the user if the component exists under a different name or in a different location. They may need to create the component first, or it might be located in an unexpected directory.

## Issue: "Published component not found" (CODE_CONNECT_ASSET_NOT_FOUND)

**Cause:** The source file path is incorrect, the component doesn't exist at that location, or the componentName doesn't match the actual export.
**Solution:** Verify the source path is correct and relative to the project root. Check that the component is properly exported from the file with the exact componentName specified.

## Issue: "Component is already mapped to code" (CODE_CONNECT_MAPPING_ALREADY_EXISTS)

**Cause:** A Code Connect mapping already exists for this component.
**Solution:** The component is already connected. If the user wants to update the mapping, they may need to remove the existing one first in Figma.

## Issue: "Insufficient permissions to create mapping" (CODE_CONNECT_INSUFFICIENT_PERMISSIONS)

**Cause:** The user does not have edit permissions on the Figma file or library.
**Solution:** The user needs edit access to the file containing the component. Contact the file owner or team admin.

## Issue: Code Connect mapping fails with URL errors

**Cause:** The Figma URL format is incorrect or missing the `node-id` parameter.
**Solution:** Verify the URL follows the required format: `https://figma.com/design/:fileKey/:fileName?node-id=1-2`. The `node-id` parameter is required. Also ensure you convert `1-2` to `1:2` when calling tools.

## Issue: Multiple similar components found

**Cause:** The codebase contains multiple components that could match the Figma component.
**Solution:** Present all candidates to the user with their file paths and let them choose which one to connect. Different components might be used in different contexts (e.g., `Button.tsx` vs `LinkButton.tsx`).
