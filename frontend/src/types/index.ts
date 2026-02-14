export interface Lead {
    name: string;
    email: string;
    phone: string;
}

export interface Note {
    email: string;
    note: string;
    summary?: string;
}

export interface NoteResponse {
    email: string;
    note: string;
    summary: string;
}
