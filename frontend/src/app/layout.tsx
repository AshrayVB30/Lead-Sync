/**
 * Root Layout Component - Next.js App Router
 * 
 * This is the root layout that wraps all pages in the application.
 * In Next.js 13+ App Router, layout.tsx defines the HTML structure
 * and common elements that persist across all pages.
 * 
 * Key responsibilities:
 * - Define HTML structure (<html> and <body> tags)
 * - Set metadata (title, description) for SEO
 * - Import global CSS styles
 * - Wrap all page content with common UI elements (if needed)
 */

import type { Metadata } from 'next';
import './globals.css'; // Global CSS styles applied to entire application

/**
 * Metadata configuration for SEO and browser tabs
 * This appears in:
 * - Browser tab title
 * - Search engine results
 * - Social media previews (when shared)
 */
export const metadata: Metadata = {
    title: 'Lead Sync + AI Notes',
    description: 'Manage your leads with AI-powered note summaries',
};

/**
 * Root layout component
 * 
 * @param children - The page content that will be rendered inside this layout
 * @returns The complete HTML document structure
 */
export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            {/* Body contains all page content passed as children */}
            <body>{children}</body>
        </html>
    );
}
