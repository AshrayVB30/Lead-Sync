'use client';

import { useState, useEffect } from 'react';
import { Lead, NoteResponse } from '@/types';
import { api } from '@/lib/api';
import LeadCard from '@/components/LeadCard';
import NoteModal from '@/components/NoteModal';
import styles from './page.module.css';

export default function Home() {
    const [leads, setLeads] = useState<Lead[]>([]);
    const [notes, setNotes] = useState<Record<string, { note: string; summary: string }>>({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [selectedLead, setSelectedLead] = useState<Lead | null>(null);

    useEffect(() => {
        fetchLeads();
    }, []);

    const fetchLeads = async () => {
        try {
            setLoading(true);
            const data = await api.getLeads();
            setLeads(data);
        } catch (err) {
            setError('Failed to load leads. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleNoteSuccess = (noteData: NoteResponse) => {
        setNotes(prev => ({
            ...prev,
            [noteData.email]: {
                note: noteData.note,
                summary: noteData.summary
            }
        }));
    };

    if (loading) {
        return (
            <div className={styles.loadingContainer}>
                <div className="spinner"></div>
                <p className={styles.loadingText}>Loading leads...</p>
            </div>
        );
    }

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

    return (
        <main className="container">
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

            <div className={styles.stats}>
                <div className={styles.statCard}>
                    <div className={styles.statNumber}>{leads.length}</div>
                    <div className={styles.statLabel}>Total Leads</div>
                </div>
                <div className={styles.statCard}>
                    <div className={styles.statNumber}>{Object.keys(notes).length}</div>
                    <div className={styles.statLabel}>Notes Added</div>
                </div>
            </div>

            <div className="grid">
                {leads.map((lead) => (
                    <LeadCard
                        key={lead.email}
                        lead={lead}
                        onAddNote={setSelectedLead}
                        savedNote={notes[lead.email]}
                    />
                ))}
            </div>

            {selectedLead && (
                <NoteModal
                    lead={selectedLead}
                    onClose={() => setSelectedLead(null)}
                    onSuccess={handleNoteSuccess}
                />
            )}
        </main>
    );
}
