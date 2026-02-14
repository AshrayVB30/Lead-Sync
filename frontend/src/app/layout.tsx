import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
    title: 'Lead Sync + AI Notes',
    description: 'Manage your leads with AI-powered note summaries',
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            <body>{children}</body>
        </html>
    );
}
