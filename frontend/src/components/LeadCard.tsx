/**
 * LeadCard Component - Individual Lead Display Card
 * 
 * This component displays a single lead's information in a card format.
 * It shows:
 * - Lead's name, email, and phone number
 * - Saved note and AI summary (if available)
 * - Button to add/update notes
 * 
 * The card is reusable and receives all its data via props, making it
 * a "presentational component" that focuses on UI rather than logic.
 */

'use client'; // Client component for interactivity

import React from 'react';
import { Lead } from '@/types';
import styles from './LeadCard.module.css';

/**
 * Props interface for LeadCard component
 * Defines what data the component needs to function
 */
interface LeadCardProps {
    /** The lead data to display (name, email, phone) */
    lead: Lead;

    /** Callback function when user clicks "Add Note" button */
    onAddNote: (lead: Lead) => void;

    /** Optional saved note data - if present, displays note and summary */
    savedNote?: {
        note: string;      // Original note text
        summary: string;   // AI-generated summary
    };
}

/**
 * LeadCard Component
 * 
 * @param lead - The lead object containing contact information
 * @param onAddNote - Function to call when "Add Note" button is clicked
 * @param savedNote - Optional note data to display if a note has been saved
 */
export default function LeadCard({ lead, onAddNote, savedNote }: LeadCardProps) {
    return (
        <div className="card">
            {/* Card Header - Name and Badge */}
            <div className={styles.cardHeader}>
                <h3 className={styles.name}>{lead.name}</h3>
                {/* Show "Has Note" badge if a note exists for this lead */}
                {savedNote && <span className="badge">Has Note</span>}
            </div>

            {/* Contact Information Section */}
            <div className={styles.info}>
                {/* Email Row */}
                <div className={styles.infoRow}>
                    <span className={styles.icon}>📧</span>
                    <span className={styles.text}>{lead.email}</span>
                </div>
                {/* Phone Row */}
                <div className={styles.infoRow}>
                    <span className={styles.icon}>📱</span>
                    <span className={styles.text}>{lead.phone}</span>
                </div>
            </div>

            {/* Note Section - Only shown if savedNote exists */}
            {/* The && operator means: if savedNote is truthy, render this section */}
            {savedNote && (
                <div className={styles.noteSection}>
                    {/* Display the original note */}
                    <div className={styles.noteLabel}>Note:</div>
                    <div className={styles.noteText}>{savedNote.note}</div>

                    {/* Display AI summary if it exists */}
                    {/* Nested conditional: only show if savedNote exists AND has a summary */}
                    {savedNote.summary && (
                        <>
                            <div className={styles.summaryLabel}>
                                <span className={styles.aiIcon}>✨</span> AI Summary:
                            </div>
                            <div className={styles.summaryText}>{savedNote.summary}</div>
                        </>
                    )}
                </div>
            )}

            {/* Action Button - Add or Update Note */}
            {/* Button text changes based on whether a note already exists */}
            <button
                className="btn btn-primary"
                onClick={() => onAddNote(lead)} // Pass the lead object to parent component
                style={{ width: '100%', marginTop: '1rem' }}
            >
                {savedNote ? 'Update Note' : 'Add Note'}
            </button>
        </div>
    );
}
