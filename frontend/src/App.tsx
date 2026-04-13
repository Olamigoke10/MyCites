import { useState } from "react";
import { CitationResponse, CitationStyle, generateCitations } from "./api/client";
import ResultPanel from "./components/ResultPanel";
import UploadForm from "./components/UploadForm";

function App() {
  const [result, setResult] = useState<CitationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleGenerate(file: File, style: CitationStyle) {
    setLoading(true);
    setError(null);
    try {
      const apiResponse = await generateCitations(file, style);
      setResult(apiResponse);
    } catch (requestError) {
      const message = requestError instanceof Error ? requestError.message : "Something went wrong.";
      setError(message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <h1>MyCites</h1>
      <p>Upload your report/project document and get references plus inline citations.</p>
      <UploadForm onSubmit={handleGenerate} loading={loading} />
      {error && <p className="error card">{error}</p>}
      {result && <ResultPanel result={result} />}
    </main>
  );
}

export default App;
