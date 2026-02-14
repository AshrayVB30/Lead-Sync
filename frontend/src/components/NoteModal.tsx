'use client';

import React, { useState } from 'react';
import { Lead, NoteResponse } from '@/types';
import { api } from '@/lib/api';
import styles from './NoteModal.module.css';

interface NoteModalProps {
    lead: Lead;
    onClose: () => void;
    onSuccess: (noteData: NoteResponse) => void;
}

export default function NoteModal({ lead, onClose, onSuccess }: NoteModalProps) {
    const [note, setNote] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!note.trim()) {
            setError('Please enter a note');
            return;
        }

        setLoading(true);
        setError('');

        try {
            const response = await api.createNote(lead.email, note);
            onSuccess(response);
            onClose();
        } catch (err) {
            setError('Failed to save note. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
                <div className={styles.header}>
                    <h2>Add Note</h2>
                    <button className={styles.closeBtn} onClick={onClose}>
                        ✕
                    </button>
                </div>

                <div className={styles.leadInfo}>
                    <p><strong>Name:</strong> {lead.name}</p>
                    <p><strong>Email:</strong> {lead.email}</p>
                    <p><strong>Phone:</strong> {lead.phone}</p>
                </div>

                <form onSubmit={handleSubmit}>
                    <div className={styles.formGroup}>
                        <label htmlFor="note">Note</label>
                        <textarea
                            id="note"
                            className="textarea"
                            value={note}
                            onChange={(e) => setNote(e.target.value)}
                            placeholder="Enter your note here..."
                            disabled={loading}
                        />
                    </div>

                    {error && <div className={styles.error}>{error}</div>}

                    <div className={styles.actions}>
                        <button
                            type="button"
                            className="btn btn-secondary"
                            onClick={onClose}
                            disabled={loading}
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            className="btn btn-primary"
                            disabled={loading}
                        >
                            {loading ? (
                                <>
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
