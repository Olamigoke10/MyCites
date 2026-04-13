import { CitationResponse } from "../api/client";

interface ResultPanelProps {
  result: CitationResponse;
}

function ResultPanel({ result }: ResultPanelProps) {
  return (
    <section className="results-grid">
      <article className="card">
        <h2>References</h2>
        {result.references.length === 0 ? (
          <p>No references detected.</p>
        ) : (
          <ol>
            {result.references.map((reference) => (
              <li key={reference}>{reference}</li>
            ))}
          </ol>
        )}
      </article>

      <article className="card">
        <h2>Annotated text</h2>
        <textarea value={result.annotated_text} readOnly rows={14} />
      </article>

      {result.warnings.length > 0 && (
        <article className="card warning-card">
          <h2>Warnings</h2>
          <ul>
            {result.warnings.map((warning) => (
              <li key={warning}>{warning}</li>
            ))}
          </ul>
        </article>
      )}
    </section>
  );
}

export default ResultPanel;
