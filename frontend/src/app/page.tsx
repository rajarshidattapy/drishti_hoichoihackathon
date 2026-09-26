"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowUpRight, Check, Clapperboard, Clock3, FileVideo2, Link2, LoaderCircle, Upload, X } from "lucide-react";
import { api } from "@/lib/api";
import { formatTime } from "@/lib/format";
import type { Episode } from "@/lib/types";

export default function LibraryPage() {
  const router = useRouter();
  const inputRef = useRef<HTMLInputElement>(null);
  const [episodes, setEpisodes] = useState<Episode[]>([]);
  const [loading, setLoading] = useState(true);
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [url, setUrl] = useState("");
  const [fetching, setFetching] = useState(false);

  useEffect(() => {
    api.episodes().then(setEpisodes).catch((reason: Error) => setError(reason.message)).finally(() => setLoading(false));
  }, []);

  async function handleFile(file?: File) {
    if (!file) return;
    setUploading(true);
    setError("");
    const form = new FormData();
    form.append("file", file);
    try {
      const episode = await api.upload(form);
      router.push(`/episode/${episode.id}`);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Upload failed");
      setUploading(false);
    }
  }

  async function handleUrl(event: React.FormEvent) {
    event.preventDefault();
    if (!url.trim()) return;
    setFetching(true);
    setError("");
    try {
      const episode = await api.ingestUrl(url.trim());
      router.push(`/episode/${episode.id}`);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Could not add the link");
      setFetching(false);
    }
  }

  return (
    <main className="library-shell">
      <header className="library-header">
        <Brand />
        <div className="header-note"><span className="signal-dot" />Semantic pipeline online</div>
      </header>

      <section className="library-intro">
        <div>
          <p className="kicker">Episode library</p>
          <h1>See what every<br />scene <span>means.</span></h1>
          <p className="intro-copy">One time-indexed layer for better ad breaks, Bengali subtitles, closed captions, and fast human review.</p>
        </div>
        <div className="intro-mark" aria-hidden="true">দৃ</div>
      </section>

      <section
        className={`upload-strip ${dragging ? "is-dragging" : ""}`}
        onDragEnter={(event) => { event.preventDefault(); setDragging(true); }}
        onDragOver={(event) => event.preventDefault()}
        onDragLeave={() => setDragging(false)}
        onDrop={(event) => { event.preventDefault(); setDragging(false); handleFile(event.dataTransfer.files[0]); }}
      >
        <div className="upload-icon"><FileVideo2 size={23} strokeWidth={1.7} /></div>
        <div>
          <h2>{uploading ? "Preparing your episode…" : "Add an episode"}</h2>
          <p>Drop an MP4, MKV, MOV, or WebM. Processing continues in the background.</p>
        </div>
        <button className="primary-button" onClick={() => inputRef.current?.click()} disabled={uploading}>
          {uploading ? <LoaderCircle className="spin" size={17} /> : <Upload size={17} />}
          {uploading ? "Uploading" : "Choose video"}
        </button>
        <input ref={inputRef} hidden type="file" accept="video/mp4,video/x-matroska,video/quicktime,video/webm" onChange={(event) => handleFile(event.target.files?.[0])} />
      </section>

      <form className="url-strip" onSubmit={handleUrl}>
        <Link2 size={17} />
        <input type="url" value={url} onChange={(event) => setUrl(event.target.value)} placeholder="…or paste a YouTube or Google Drive video link" aria-label="Video link" disabled={fetching} />
        <button className="quiet-button" type="submit" disabled={fetching || !url.trim()}>
          {fetching ? <LoaderCircle className="spin" size={15} /> : <ArrowUpRight size={15} />}
          {fetching ? "Adding" : "Fetch video"}
        </button>
      </form>

      {error && <div className="error-banner"><X size={16} />{error}{error === "Failed to fetch" ? ". Start the FastAPI server on port 8000 and try again." : ""}</div>}

      <section className="catalog-section">
        <div className="section-heading">
          <div><h2>Episodes</h2><span>{episodes.length} in this library</span></div>
          <div className="table-labels"><span>Duration</span><span>Status</span><span>Processed</span><i /></div>
        </div>
        <div className="episode-list">
          {loading ? (
            <div className="empty-row"><LoaderCircle className="spin" /> Loading library…</div>
          ) : episodes.map((episode, index) => (
            <button className="episode-row" key={episode.id} onClick={() => router.push(`/episode/${episode.id}`)}>
              <span className="episode-index">{String(index + 1).padStart(2, "0")}</span>
              <span className="episode-main">
                <span className="episode-thumb"><Clapperboard size={22} /><i>{episode.status === "processed" ? "Ready" : episode.status === "downloading" ? `↓ ${episode.progress}%` : `${episode.progress}%`}</i></span>
                <span><strong>{episode.title}</strong><small>{episode.id}</small></span>
              </span>
              <span className="row-data"><Clock3 size={14} />{episode.duration ? formatTime(episode.duration, true) : "Analyzing"}</span>
              <span className={`status-pill ${episode.status}`}>
                {episode.status === "processed" ? <Check size={13} /> : <LoaderCircle className={episode.status === "processing" || episode.status === "downloading" ? "spin" : ""} size={13} />}
                {episode.status}
              </span>
              <span className="row-data date">{new Intl.DateTimeFormat("en-IN", { day: "2-digit", month: "short", year: "numeric" }).format(new Date(episode.created_at))}</span>
              <span className="row-open"><ArrowUpRight size={18} /></span>
            </button>
          ))}
        </div>
      </section>

      <footer className="library-footer">
        <span></span><span>Semantic understanding for regional stories</span><span>Schema v1.0</span>
      </footer>
    </main>
  );
}

function Brand() {
  return (
    <div className="brand">
      <span className="brand-glyph"><i /><i /><i /></span>
      <span><strong>DRISHTI</strong><small>দৃষ্টি</small></span>
    </div>
  );
}

