import { FormEvent, useState } from "react";
import { CitationStyle } from "../api/client";

interface UploadFormProps {
  onSubmit: (file: File, style: CitationStyle) => Promise<void>;
  loading: boolean;
}

function UploadForm({ onSubmit, loading }: UploadFormProps) {
  const [file, setFile] = useState<File | null>(null);
  const [style, setStyle] = useState<CitationStyle>("APA");
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!file) {
      setError("Please choose a PDF or DOCX file.");
      return;
    }
    setError(null);
    await onSubmit(file, style);
  }

  return (
    <form className="card form-grid" onSubmit={handleSubmit}>
      <label>
        Document
        <input
          type="file"
          accept=".pdf,.docx,.txt,.md"
          onChange={(event) => setFile(event.target.files?.[0] ?? null)}
        />
      </label>

      <label>
        Citation style
        <select value={style} onChange={(event) => setStyle(event.target.value as CitationStyle)}>
          <option value="APA">APA</option>
          <option value="MLA">MLA</option>
          <option value="IEEE">IEEE</option>
        </select>
      </label>

      {error && <p className="error">{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? "Generating..." : "Generate References & Citations"}
      </button>
    </form>
  );
}

export default UploadForm;
