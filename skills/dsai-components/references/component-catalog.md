# DSAI Component Catalog

## Layout & Structure

### Accordion
Import: `import { Accordion } from '@/components/ui/accordion'`

Collapsible sections with keyboard navigation.
```tsx
<Accordion defaultActiveKey="0">
  <Accordion.Item eventKey="0">
    <Accordion.Header>Section 1</Accordion.Header>
    <Accordion.Body>Content 1</Accordion.Body>
  </Accordion.Item>
</Accordion>
```
Key Props: defaultActiveKey, alwaysOpen, flush

### Breadcrumb
Import: `import { Breadcrumb, BreadcrumbItem } from '@/components/ui/breadcrumb'`

```tsx
<Breadcrumb>
  <BreadcrumbItem href="/">Home</BreadcrumbItem>
  <BreadcrumbItem active>Current</BreadcrumbItem>
</Breadcrumb>
```

### Card (Compound)
Import: `import { Card } from '@/components/ui/card'`

```tsx
<Card variant="elevated" color="primary" size="md">
  <Card.Header>
    <Card.Title>Title</Card.Title>
    <Card.Subtitle>Subtitle</Card.Subtitle>
  </Card.Header>
  <Card.Body>
    <Card.Text>Content text</Card.Text>
  </Card.Body>
  <Card.Footer>Footer actions</Card.Footer>
</Card>
```
Variants: elevated | outlined | ghost
Colors: primary | secondary | success | danger | warning | info | light | dark
Props: horizontal, interactive, href, imgPosition

### CardList
Import: `import { CardList } from '@/components/ui/card-list'`

```tsx
<CardList items={cards} columns={3} gap="md" />
```

### Container
Import: `import { Container } from '@/components/ui/container'`

```tsx
<Container fluid="md">Content</Container>
```

### Modal (Compound)
Import: `import { Modal } from '@/components/ui/modal'`

```tsx
<Modal isOpen={open} onClose={close} size="lg" centered backdrop>
  <Modal.Header closeButton>
    <Modal.Title>Edit Profile</Modal.Title>
    <Modal.Description>Update your information</Modal.Description>
  </Modal.Header>
  <Modal.Body>Form content</Modal.Body>
  <Modal.Footer>
    <Button variant="secondary" onClick={close}>Cancel</Button>
    <Button variant="primary" onClick={save}>Save</Button>
  </Modal.Footer>
</Modal>
```
Sizes: sm | md | lg | xl | fullscreen
Props: isOpen, onClose, centered, backdrop, closeOnEscape, closeOnBackdrop, initialFocusRef, returnFocusRef, scrollable, fullscreenBreakpoint

### Navbar
Import: `import { Navbar, Nav } from '@/components/ui/navbar'`

```tsx
<Navbar expand="lg" variant="dark" sticky="top">
  <Container>
    <Navbar.Brand href="/">App</Navbar.Brand>
    <Navbar.Toggle />
    <Navbar.Collapse>
      <Nav>
        <Nav.Link href="/about">About</Nav.Link>
      </Nav>
    </Navbar.Collapse>
  </Container>
</Navbar>
```

### Sheet
Import: `import { Sheet } from '@/components/ui/sheet'`

```tsx
<Sheet isOpen={open} onClose={close} position="right" size="md">
  <Sheet.Header>Settings</Sheet.Header>
  <Sheet.Body>Content</Sheet.Body>
</Sheet>
```

### Tabs (Compound)
Import: `import { Tabs, TabList, Tab, TabPanel } from '@/components/ui/tabs'`

```tsx
<Tabs variant="pills" orientation="horizontal" defaultActiveTab="general">
  <TabList aria-label="Settings">
    <Tab id="general">General</Tab>
    <Tab id="security" disabled>Security</Tab>
  </TabList>
  <TabPanel id="general">General content</TabPanel>
  <TabPanel id="security">Security content</TabPanel>
</Tabs>
```
Variants: underline | pills | tabs
Props: orientation, activationMode (automatic|manual), lazyMount, unmountOnExit, onChange

### TabsPro
Import: `import { TabsPro } from '@/components/ui/tabs-pro'`

```tsx
<TabsPro tabs={tabs} onTabClose={handleClose} onTabAdd={handleAdd} draggable />
```

## Form Controls

### Button
Import: `import { Button } from '@/components/ui/button'`

```tsx
<Button variant="primary" size="md" loading={isLoading} startIcon={<SaveIcon />}>
  Save Changes
</Button>
<Button as="a" href="/link" variant="link">Navigate</Button>
```
Variants: primary | secondary | success | danger | warning | info | light | dark | outline-primary | outline-secondary | ... | subtle-primary | subtle-secondary | ... | ghost | link
Sizes: sm | md | lg | icon
Props: loading, error, disabled, startIcon, endIcon, announceText, as (polymorphic)

### Checkbox / CheckboxGroup
Import: `import { Checkbox, CheckboxGroup } from '@/components/ui/checkbox'`

```tsx
<CheckboxGroup label="Options" orientation="vertical">
  <Checkbox value="a" label="Option A" />
  <Checkbox value="b" label="Option B" indeterminate />
</CheckboxGroup>
```

### Input
Import: `import { Input } from '@/components/ui/input'`

```tsx
<Input
  label="Email"
  type="email"
  size="md"
  helperText="We'll never share your email"
  error="Invalid email format"
  prefix={<MailIcon />}
  clearable
  showCount
  maxLength={100}
/>
```
Types: text | email | password | number | tel | url | search
Sizes: sm | md | lg
Props: label, helperText, error, success, prefix, suffix, clearable, showCount, floating, plaintext

### Radio / RadioGroup
Import: `import { Radio, RadioGroup } from '@/components/ui/radio'`

```tsx
<RadioGroup label="Size" value={size} onChange={setSize}>
  <Radio value="sm" label="Small" />
  <Radio value="md" label="Medium" />
  <Radio value="lg" label="Large" />
</RadioGroup>
```

### Select
Import: `import { Select } from '@/components/ui/select'`

```tsx
<Select<UserOption>
  options={options}
  value={selected}
  onChange={setSelected}
  label="Assignee"
  searchable
  clearable
  renderOption={(opt) => <UserAvatar user={opt} />}
  renderValue={(opt) => opt.name}
/>
```
Props: options, value, onChange, multiple, searchable, filterable, clearable, loading, renderOption, renderValue, groups

### Switch
Import: `import { Switch } from '@/components/ui/switch'`

```tsx
<Switch checked={enabled} onChange={setEnabled} label="Enable notifications" />
```

### SearchSelectField
Import: `import { SearchSelectField } from '@/components/ui/search-select-field'`

```tsx
<SearchSelectField options={options} onSearch={handleSearch} loading={isSearching} />
```

### SelectableCard
Import: `import { SelectableCard } from '@/components/ui/selectable-card'`

```tsx
<SelectableCard selected={isSelected} onSelect={toggle} variant="outlined">
  <Card.Body>Selectable content</Card.Body>
</SelectableCard>
```

## Display & Feedback

### Alert
Import: `import { Alert } from '@/components/ui/alert'`

```tsx
<Alert variant="warning" dismissible onClose={handleClose}>
  <Alert.Heading>Warning</Alert.Heading>
  Please review your settings before continuing.
</Alert>
```

### Avatar / AvatarGroup
Import: `import { Avatar, AvatarGroup } from '@/components/ui/avatar'`

```tsx
<AvatarGroup max={3}>
  <Avatar src="/user1.jpg" alt="User 1" size="md" />
  <Avatar src="/user2.jpg" alt="User 2" size="md" />
  <Avatar fallback="JD" />
</AvatarGroup>
```

### Badge / BadgeWrapper
Import: `import { Badge, BadgeWrapper } from '@/components/ui/badge'`

```tsx
<Badge variant="primary" pill>New</Badge>
<BadgeWrapper count={5}><BellIcon /></BadgeWrapper>
```

### Typography (Display, Heading, Text)
Import: `import { Display } from '@/components/ui/display'`
Import: `import { Heading } from '@/components/ui/heading'`
Import: `import { Text } from '@/components/ui/text'`

```tsx
<Display size={1}>Hero Title</Display>
<Heading level={2}>Section Title</Heading>
<Text variant="body-secondary" size="sm">Description text</Text>
```

### ListGroup / ListGroupItem
Import: `import { ListGroup, ListGroupItem } from '@/components/ui/list-group'`

```tsx
<ListGroup>
  <ListGroupItem active>Active Item</ListGroupItem>
  <ListGroupItem action onClick={handle}>Clickable Item</ListGroupItem>
</ListGroup>
```

### Pagination
Import: `import { Pagination } from '@/components/ui/pagination'`

```tsx
<Pagination currentPage={page} totalPages={10} onPageChange={setPage} siblingCount={1} />
```

### Popover (Compound)
Import: `import { Popover, PopoverHeader, PopoverBody } from '@/components/ui/popover'`

```tsx
<Popover trigger="click" placement="top">
  <Popover.Trigger><Button>Open</Button></Popover.Trigger>
  <Popover.Content>
    <PopoverHeader>Title</PopoverHeader>
    <PopoverBody>Popover content</PopoverBody>
    <PopoverCloseButton />
  </Popover.Content>
</Popover>
```

### Progress
Import: `import { Progress } from '@/components/ui/progress'`

```tsx
<Progress value={75} variant="success" striped animated label="75%" />
```

### Spinner
Import: `import { Spinner } from '@/components/ui/spinner'`

```tsx
<Spinner size="md" variant="primary" />
<Spinner as="span" animation="grow" size="sm" role="status" />
```

### Table
Import: `import { Table } from '@/components/ui/table'`

```tsx
<Table striped hover responsive>
  <thead><tr><th>Name</th><th>Email</th></tr></thead>
  <tbody>{rows.map(row => <tr key={row.id}><td>{row.name}</td><td>{row.email}</td></tr>)}</tbody>
</Table>
```

### Toast / ToastContainer / ToastProvider
Import: `import { Toast, ToastContainer, ToastProvider } from '@/components/ui/toast'`

```tsx
<ToastProvider>
  <ToastContainer position="top-end">
    <Toast variant="success" autoDismiss timeout={5000}>
      <Toast.Header closeButton>Success</Toast.Header>
      <Toast.Body>Operation completed successfully.</Toast.Body>
    </Toast>
  </ToastContainer>
</ToastProvider>
```

### Tooltip / TooltipProvider / TooltipGroup
Import: `import { Tooltip, TooltipProvider } from '@/components/ui/tooltip'`

```tsx
<TooltipProvider delayDuration={200}>
  <Tooltip content="Save your changes" placement="top">
    <Button>Save</Button>
  </Tooltip>
</TooltipProvider>
```

### Dropdown
Import: `import { Dropdown } from '@/components/ui/dropdown'`

```tsx
<Dropdown>
  <Dropdown.Toggle variant="secondary">Actions</Dropdown.Toggle>
  <Dropdown.Menu>
    <Dropdown.Item onClick={edit}>Edit</Dropdown.Item>
    <Dropdown.Divider />
    <Dropdown.Item onClick={remove} className="text-danger">Delete</Dropdown.Item>
  </Dropdown.Menu>
</Dropdown>
```

### Carousel
Import: `import { Carousel, CarouselItem } from '@/components/ui/carousel'`

```tsx
<Carousel controls indicators interval={5000} pause="hover">
  <CarouselItem>
    <img src="/slide1.jpg" alt="Slide 1" />
    <CarouselCaption>Caption 1</CarouselCaption>
  </CarouselItem>
</Carousel>
```

### Scrollspy
Import: `import { Scrollspy } from '@/components/ui/scrollspy'`

```tsx
<Scrollspy items={['section-1', 'section-2']} currentClassName="active">
  <a href="#section-1">Section 1</a>
  <a href="#section-2">Section 2</a>
</Scrollspy>
```
