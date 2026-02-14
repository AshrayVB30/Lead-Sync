'use client';

import React from 'react';
import { Lead } from '@/types';
import styles from './LeadCard.module.css';

interface LeadCardProps {
    lead: Lead;
    onAddNote: (lead: Lead) => void;
    savedNote?: {
        note: string;
        summary: string;
    };
}

export default function LeadCard({ lead, onAddNote, savedNote }: LeadCardProps) {
    return (
        <div className="card">
            <div className={styles.cardHeader}>
                <h3 className={styles.name}>{lead.name}</h3>
                {savedNote && <span className="badge">Has Note</span>}
            </div>

            <div className={styles.info}>
                <div className={styles.infoRow}>
                    <span className={styles.icon}>📧</span>
                    <span className={styles.text}>{lead.email}</span>
                </div>
                <div className={styles.infoRow}>
                    <span className={styles.icon}>📱</span>
                    <span className={styles.text}>{lead.phone}</span>
                </div>
            </div>

            {savedNote && (
                <div className={styles.noteSection}>
                    <div className={styles.noteLabel}>Note:</div>
                    <div className={styles.noteText}>{savedNote.note}</div>

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

            <button
                className="btn btn-primary"
                onClick={() => onAddNote(lead)}
                style={{ width: '100%', marginTop: '1rem' }}
            >
                {savedNote ? 'Update Note' : 'Add Note'}
            </button>
        </div>
    );
}
