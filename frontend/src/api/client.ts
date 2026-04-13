export type CitationStyle = "APA" | "MLA" | "IEEE";

export interface CitationResponse {
  references: string[];
  annotated_text: string;
  warnings: string[];
}

const API_BASE_URL = "http://localhost:8000";

export async function generateCitations(file: File, style: CitationStyle): Promise<CitationResponse> {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("style", style);

  const response = await fetch(`${API_BASE_URL}/citations/generate`, {
    method: "POST",
    body: formData
  });

  if (!response.ok) {
    let message = "Failed to generate citations.";
    try {
      const payload = (await response.json()) as { detail?: string };
      if (payload.detail) {
        message = payload.detail;
      }
    } catch {
      // Keep generic fallback message.
    }
    throw new Error(message);
  }

  return (await response.json()) as CitationResponse;
}
