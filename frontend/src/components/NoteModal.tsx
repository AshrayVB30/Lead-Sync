/**
 * NoteModal Component - Modal Dialog for Adding/Editing Notes
 * 
 * This component provides a modal interface for users to:
 * - Create notes for a specific lead
 * - Automatically generate AI summaries via the backend
 * - Handle form validation and submission
 * - Show loading states during API calls
 * - Display error messages if something goes wrong
 * 
 * The modal uses an overlay pattern (click outside to close) and prevents
 * event propagation to avoid accidental closes when clicking inside the modal.
 */

'use client'; // Client component for interactivity

import React, { useState } from 'react';
import { Lead, NoteResponse } from '@/types';
import { api } from '@/lib/api';
import styles from './NoteModal.module.css';

/**
 * Props interface for NoteModal component
 */
interface NoteModalProps {
    /** The lead this note is being created for */
    lead: Lead;

    /** Callback to close the modal */
    onClose: () => void;

    /** Callback when note is successfully saved (receives the note data with AI summary) */
    onSuccess: (noteData: NoteResponse) => void;
}

/**
 * NoteModal Component
 * 
 * @param lead - The lead object for which the note is being created
 * @param onClose - Function to call when modal should close
 * @param onSuccess - Function to call when note is successfully saved
 */
export default function NoteModal({ lead, onClose, onSuccess }: NoteModalProps) {
    // ========================================================================
    // STATE MANAGEMENT
    // ========================================================================

    // The note text entered by the user
    const [note, setNote] = useState('');

    // Loading state - true while submitting to backend
    const [loading, setLoading] = useState(false);

    // Error message to display if validation or API call fails
    const [error, setError] = useState('');

    // ========================================================================
    // FORM HANDLING
    // ========================================================================

    /**
     * Handle form submission
     * 
     * This async function:
     * 1. Prevents default form submission (which would reload the page)
     * 2. Validates that note is not empty
     * 3. Calls backend API to save note and generate AI summary
     * 4. Notifies parent component of success
     * 5. Closes the modal
     * 6. Handles errors gracefully
     * 
     * @param e - The form submission event
     */
    const handleSubmit = async (e: React.FormEvent) => {
        // Prevent default form behavior (page reload)
        e.preventDefault();

        // Validation: Check if note is empty or just whitespace
        if (!note.trim()) {
            setError('Please enter a note');
            return; // Stop execution if validation fails
        }

        // Start loading state (disables form, shows spinner)
        setLoading(true);
        setError(''); // Clear any previous errors

        try {
            // Call backend API to create note with AI summary
            // This may take 1-3 seconds depending on AI processing time
            const response = await api.createNote(lead.email, note);

            // Notify parent component that note was saved successfully
            // Parent will update its state to show the new note
            onSuccess(response);

            // Close the modal
            onClose();
        } catch (err) {
            // If API call fails, show error message to user
            setError('Failed to save note. Please try again.');
        } finally {
            // Always clear loading state, whether success or failure
            setLoading(false);
        }
    };

    // ========================================================================
    // RENDER
    // ========================================================================

    return (
        // Modal overlay - clicking this closes the modal
        <div className="modal-overlay" onClick={onClose}>
            {/* Modal content - clicking inside doesn't close the modal */}
            {/* stopPropagation prevents clicks from bubbling up to the overlay */}
            <div className="modal" onClick={(e) => e.stopPropagation()}>
                {/* Modal Header with Title and Close Button */}
                <div className={styles.header}>
                    <h2>Add Note</h2>
                    <button className={styles.closeBtn} onClick={onClose}>
                        ✕
                    </button>
                </div>

                {/* Lead Information Display */}
                {/* Shows which lead this note is for */}
                <div className={styles.leadInfo}>
                    <p><strong>Name:</strong> {lead.name}</p>
                    <p><strong>Email:</strong> {lead.email}</p>
                    <p><strong>Phone:</strong> {lead.phone}</p>
                </div>

                {/* Note Form */}
                <form onSubmit={handleSubmit}>
                    {/* Textarea Input for Note */}
                    <div className={styles.formGroup}>
                        <label htmlFor="note">Note</label>
                        <textarea
                            id="note"
                            className="textarea"
                            value={note}
                            onChange={(e) => setNote(e.target.value)} // Update state on every keystroke
                            placeholder="Enter your note here..."
                            disabled={loading} // Disable input while submitting
                        />
                    </div>

                    {/* Error Message Display */}
                    {/* Only shown if error state is not empty */}
                    {error && <div className={styles.error}>{error}</div>}

                    {/* Form Action Buttons */}
                    <div className={styles.actions}>
                        {/* Cancel Button - Closes modal without saving */}
                        <button
                            type="button" // Not a submit button
                            className="btn btn-secondary"
                            onClick={onClose}
                            disabled={loading} // Disable while submitting
                        >
                            Cancel
                        </button>

                        {/* Submit Button - Saves note and generates AI summary */}
                        <button
                            type="submit" // Triggers form onSubmit handler
                            className="btn btn-primary"
                            disabled={loading} // Disable while submitting
                        >
                            {/* Conditional rendering: show spinner while loading, text otherwise */}
                            {loading ? (
                                <>
                                    {/* Loading spinner */}
                                    <span className="spinner" style={{ width: '16px', height: '16px', borderWidth: '2px' }}></span>
                                    Saving...
                                </>
                            ) : (
                                'Save Note'
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
