/**
 * TypeScript Type Definitions
 * 
 * This module defines the core data structures used throughout the frontend application.
 * TypeScript interfaces provide type safety, better IDE autocomplete, and catch errors
 * at compile time rather than runtime.
 * 
 * These types should match the Pydantic models in the backend to ensure consistency
 * between frontend and backend data structures.
 */

/**
 * Lead Interface - Represents a potential customer
 * 
 * This interface defines the structure of a lead object as received from the backend.
 * Leads are fetched from an external CRM API and displayed in the dashboard.
 * 
 * Usage:
 *   const lead: Lead = { name: "John Doe", email: "john@example.com", phone: "555-1234" };
 */
export interface Lead {
    /** Full name of the lead */
    name: string;

    /** Email address (used as unique identifier) */
    email: string;

    /** Phone number in any format */
    phone: string;
}

/**
 * Note Interface - Represents a note with optional AI summary
 * 
 * This interface is used for note data that may or may not have a summary yet.
 * The summary is optional because it might not be generated yet or the AI service
 * might be unavailable.
 * 
 * Usage:
 *   const note: Note = { email: "john@example.com", note: "Customer called...", summary: "..." };
 */
export interface Note {
    /** Email of the lead this note belongs to */
    email: string;

    /** The original note text */
    note: string;

    /** AI-generated summary (optional, max 20 words) */
    summary?: string;
}

/**
 * NoteResponse Interface - API response when creating a note
 * 
 * This interface represents the data structure returned by the backend
 * when a note is successfully created. Unlike the Note interface, the
 * summary is required here because the backend always generates one
 * (or provides a fallback if AI fails).
 * 
 * Usage:
 *   const response: NoteResponse = await api.createNote(email, note);
 *   console.log(response.summary); // Always present
 */
export interface NoteResponse {
    /** Email of the lead this note belongs to */
    email: string;

    /** The original note text */
    note: string;

    /** AI-generated summary (always present in API responses) */
    summary: string;
}
