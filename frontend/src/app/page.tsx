/**
 * Lead Sync Dashboard - Main Page Component
 * 
 * This is the main dashboard page that displays all leads and allows users to:
 * - View a list of leads fetched from the backend API
 * - Add notes to individual leads
 * - See AI-generated summaries of their notes
 * - Track statistics (total leads, notes added)
 * 
 * The page uses React hooks for state management and handles loading/error states
 * gracefully to provide a smooth user experience.
 */

'use client'; // This directive tells Next.js to render this component on the client side

import { useState, useEffect } from 'react';
import { Lead, NoteResponse } from '@/types';
import { api } from '@/lib/api';
import LeadCard from '@/components/LeadCard';
import NoteModal from '@/components/NoteModal';
import styles from './page.module.css';

export default function Home() {
    // ========================================================================
    // STATE MANAGEMENT
    // ========================================================================

    // Array of all leads fetched from the backend
    const [leads, setLeads] = useState<Lead[]>([]);

    // Dictionary mapping email addresses to their notes and summaries
    // Structure: { "email@example.com": { note: "...", summary: "..." } }
    const [notes, setNotes] = useState<Record<string, { note: string; summary: string }>>({});

    // Loading state - true while fetching data from API
    const [loading, setLoading] = useState(true);

    // Error message to display if API calls fail
    const [error, setError] = useState('');

    // Currently selected lead for adding/editing a note (null when modal is closed)
    const [selectedLead, setSelectedLead] = useState<Lead | null>(null);

    // ========================================================================
    // LIFECYCLE & DATA FETCHING
    // ========================================================================

    /**
     * useEffect hook runs once when the component first mounts
     * This is where we fetch the initial list of leads from the backend
     */
    useEffect(() => {
        fetchLeads();
    }, []); // Empty dependency array = run only once on mount

    /**
     * Fetch leads from the backend API
     * 
     * This async function:
     * 1. Sets loading state to show spinner
     * 2. Calls the API to get leads
     * 3. Updates state with the fetched leads
     * 4. Handles errors gracefully by showing error message
     * 5. Always clears loading state when done (success or failure)
     */
    const fetchLeads = async () => {
        try {
            setLoading(true);
            const data = await api.getLeads();
            setLeads(data);
        } catch (err) {
            setError('Failed to load leads. Please try again.');
        } finally {
            // This runs whether the try block succeeds or fails
            setLoading(false);
        }
    };

    // ========================================================================
    // EVENT HANDLERS
    // ========================================================================

    /**
     * Handle successful note creation
     * 
     * This is called by the NoteModal when a note is successfully saved.
     * It updates the local state to immediately show the new note without
     * needing to refetch all data from the server.
     * 
     * @param noteData - The note response from the backend including email, note, and summary
     */
    const handleNoteSuccess = (noteData: NoteResponse) => {
        setNotes(prev => ({
            ...prev, // Keep all existing notes
            [noteData.email]: { // Add or update the note for this email
                note: noteData.note,
                summary: noteData.summary
            }
        }));
    };

    // ========================================================================
    // CONDITIONAL RENDERING - LOADING STATE
    // ========================================================================

    /**
     * Show loading spinner while fetching leads
     * This provides visual feedback that the app is working
     */
    if (loading) {
        return (
            <div className={styles.loadingContainer}>
                <div className="spinner"></div>
                <p className={styles.loadingText}>Loading leads...</p>
            </div>
        );
    }

    // ========================================================================
    // CONDITIONAL RENDERING - ERROR STATE
    // ========================================================================

    /**
     * Show error message if API call failed
     * Includes a retry button to let users try again without refreshing the page
     */
    if (error) {
        return (
            <div className={styles.errorContainer}>
                <div className={styles.errorBox}>
                    <h2>⚠️ Error</h2>
                    <p>{error}</p>
                    <button className="btn btn-primary" onClick={fetchLeads}>
                        Retry
                    </button>
                </div>
            </div>
        );
    }

    // ========================================================================
    // MAIN RENDER - SUCCESS STATE
    // ========================================================================

    /**
     * Main dashboard UI
     * Shows header, statistics, lead cards grid, and note modal
     */
    return (
        <main className="container">
            {/* Header Section */}
            <div className={styles.header}>
                <h1 className={styles.title}>
                    <span className={styles.titleGradient}>Lead Sync</span>
                    <span className={styles.titlePlus}>+</span>
                    <span className={styles.titleAI}>AI Notes</span>
                </h1>
                <p className={styles.subtitle}>
                    Manage your leads with AI-powered note summaries
                </p>
            </div>

            {/* Statistics Cards */}
            <div className={styles.stats}>
                {/* Total number of leads */}
                <div className={styles.statCard}>
                    <div className={styles.statNumber}>{leads.length}</div>
                    <div className={styles.statLabel}>Total Leads</div>
                </div>
                {/* Number of leads with notes added */}
                <div className={styles.statCard}>
                    <div className={styles.statNumber}>{Object.keys(notes).length}</div>
                    <div className={styles.statLabel}>Notes Added</div>
                </div>
            </div>

            {/* Lead Cards Grid */}
            {/* Maps over each lead and renders a LeadCard component */}
            <div className="grid">
                {leads.map((lead) => (
                    <LeadCard
                        key={lead.email} // Unique key for React's reconciliation
                        lead={lead}
                        onAddNote={setSelectedLead} // Opens modal when "Add Note" is clicked
                        savedNote={notes[lead.email]} // Pass saved note if it exists
                    />
                ))}
            </div>

            {/* Note Modal - Only rendered when a lead is selected */}
            {/* The && operator means: if selectedLead is truthy, render the modal */}
            {selectedLead && (
                <NoteModal
                    lead={selectedLead}
                    onClose={() => setSelectedLead(null)} // Close modal by clearing selection
                    onSuccess={handleNoteSuccess} // Update state when note is saved
                />
            )}
        </main>
    );
}
