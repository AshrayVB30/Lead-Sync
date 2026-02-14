# Frontend Dependencies Documentation

This document explains all the dependencies in `package.json` for the Lead Sync frontend application.

## NPM Scripts

Run these with: `npm run <script-name>`

- **`dev`** - Start development server with hot reload on http://localhost:3000
- **`build`** - Build optimized production bundle
- **`start`** - Start production server (must run 'build' first)
- **`lint`** - Run ESLint to check for code quality issues

## Runtime Dependencies

These are required to run the application and are installed in both production and development:

### next (^14.2.35)
Next.js - React framework with server-side rendering, routing, and optimization. Provides the foundation for the entire frontend application.

### react (^18)
React - JavaScript library for building user interfaces. The core library for creating components and managing UI state.

### react-dom (^18)
React DOM - React package for working with the DOM. Handles rendering React components to the browser.

## Development Dependencies

These are only needed during development and are NOT installed in production to reduce bundle size:

### @types/node (^20)
TypeScript type definitions for Node.js APIs. Provides type safety when using Node.js built-in modules.

### @types/react (^18)
TypeScript type definitions for React. Enables TypeScript autocomplete and type checking for React components.

### @types/react-dom (^18)
TypeScript type definitions for React DOM. Provides types for React DOM-specific APIs.

### eslint (9.39.2)
ESLint - JavaScript/TypeScript linter for code quality. Catches common errors and enforces coding standards.

### eslint-config-next (16.1.6)
ESLint configuration optimized for Next.js projects. Includes recommended rules for Next.js development.

### typescript (^5)
TypeScript - Adds static typing to JavaScript. Catches type errors at compile time and improves code quality.
