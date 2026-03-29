# FSM (Finite State Machine) Pattern

## Overview
Interactive DSAI components use finite state machines via useReducer for predictable state transitions. This prevents impossible states and makes behavior explicit.

## Architecture
```
Component
  ├── *.types.ts    — State, Event, Props types
  ├── *.fsm.ts      — Reducer + initial state creator
  └── *.tsx          — Component using useReducer(fsmReducer, ...)
```

## Button FSM Example

### States
```typescript
interface ButtonFSMState extends FSMStateBase {
  status: 'idle' | 'hovered' | 'focused' | 'pressed' | 'disabled' | 'loading' | 'error';
  isPressed: boolean;
  isHovered: boolean;
  isFocused: boolean;
  isDisabled: boolean;
  isLoading: boolean;
  hasError: boolean;
  errorMessage?: string;
}
```

### Events
```typescript
type ButtonFSMEvent =
  | { type: 'HOVER' }
  | { type: 'UNHOVER' }
  | { type: 'FOCUS' }
  | { type: 'BLUR' }
  | { type: 'PRESS' }
  | { type: 'RELEASE' }
  | { type: 'DISABLE' }
  | { type: 'ENABLE' }
  | { type: 'START_LOADING' }
  | { type: 'STOP_LOADING' }
  | { type: 'ERROR'; message: string }
  | { type: 'CLEAR_ERROR' };
```

### Reducer
```typescript
function buttonFSMReducer(state: ButtonFSMState, event: ButtonFSMEvent): ButtonFSMState {
  // Guard: disabled and loading states block most transitions
  if (state.isDisabled && event.type !== 'ENABLE') return state;
  if (state.isLoading && !['STOP_LOADING', 'ERROR'].includes(event.type)) return state;

  switch (event.type) {
    case 'HOVER':
      return { ...state, status: 'hovered', isHovered: true };
    case 'PRESS':
      return { ...state, status: 'pressed', isPressed: true };
    case 'START_LOADING':
      return { ...state, status: 'loading', isLoading: true };
    // ... etc
  }
}
```

### Usage in Component
```tsx
const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  function Button({ loading, disabled, error, ...props }, ref) {
    const [fsmState, dispatch] = useReducer(
      buttonFSMReducer,
      { loading, disabled, error },
      createInitialButtonFSMState
    );

    // Sync props → FSM
    useEffect(() => {
      if (loading) dispatch({ type: 'START_LOADING' });
      else dispatch({ type: 'STOP_LOADING' });
    }, [loading]);

    return (
      <button
        ref={ref}
        disabled={fsmState.isDisabled || fsmState.isLoading}
        onMouseEnter={() => dispatch({ type: 'HOVER' })}
        onMouseLeave={() => dispatch({ type: 'UNHOVER' })}
        onFocus={() => dispatch({ type: 'FOCUS' })}
        onBlur={() => dispatch({ type: 'BLUR' })}
        onMouseDown={() => dispatch({ type: 'PRESS' })}
        onMouseUp={() => dispatch({ type: 'RELEASE' })}
        className={cn('btn', `btn-${variant}`, fsmState.isLoading && 'btn-loading')}
      >
        {fsmState.isLoading ? <Spinner size="sm" /> : children}
      </button>
    );
  }
);
```

## Visual State Mapping
```typescript
interface VisualStateBase {
  state: string;
  shouldRender: boolean;
  modifiers?: string[];
}

// Maps FSM state → CSS classes
function getButtonVisualState(fsmState: ButtonFSMState): VisualStateBase {
  return {
    state: fsmState.status,
    shouldRender: true,
    modifiers: [
      fsmState.isLoading && 'btn-loading',
      fsmState.hasError && 'btn-error',
      fsmState.isDisabled && 'btn-disabled',
    ].filter(Boolean) as string[],
  };
}
```

## Key Rules
1. FSM types go in *.types.ts, reducer in *.fsm.ts
2. NEVER have conflicting boolean states — FSM status is the source of truth
3. Props sync to FSM via useEffect (loading → START_LOADING)
4. Guards prevent impossible transitions (disabled blocks HOVER)
5. Visual state derived from FSM state (never independent CSS state)
6. All event handlers dispatch FSM events (not direct state mutation)
