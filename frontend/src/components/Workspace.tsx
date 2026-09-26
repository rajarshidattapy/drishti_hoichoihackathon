"use client";

import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import {
  ArrowLeft, BadgeCheck, Captions, Check, ChevronDown, ChevronRight, CircleAlert, Clock3,
  Copy, Download, FileJson2, Film, Gauge, Info, ListFilter, MapPin, MoreHorizontal, Pause,
  Play, Search, Sparkles, Tag, TriangleAlert, Users, Volume2, X,
} from "lucide-react";
import SemanticTimeline from "./SemanticTimeline";
import { API_URL, api } from "@/lib/api";
import { formatTime, presenceLabel, sentenceCase } from "@/lib/format";
import type { AdCandidate, Entity, Episode, QCIssue, Scene, SubtitleCue, Timeline, Utterance } from "@/lib/types";

const tabs = ["Scenes", "Transcript", "Entities", "Ads", "Subtitles", "QC", "JSON"] as const;
type Tab = (typeof tabs)[number];

export default function Workspace({ episodeId }: { episodeId: string }) {
  const [episode, setEpisode] = useState<Episode | null>(null);
  const [data, setData] = useState<Timeline | null>(null);
  const [error, setError] = useState("");
  const [currentTime, setCurrentTime] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [activeTab, setActiveTab] = useState<Tab>("Scenes");
  const [captions, setCaptions] = useState<"off" | "sub" | "cc">("cc");
  const [search, setSearch] = useState("");
  const [exportOpen, setExportOpen] = useState(false);

  useEffect(() => {
    let cancelled = false;
    let timer: number | undefined;
    async function load() {
      try {
        const episodeResult = await api.episode(episodeId);
        if (cancelled) return;
        setEpisode(episodeResult);
        if (episodeResult.status === "processed") {
          const timelineResult = await api.timeline(episodeId);
          if (!cancelled) setData(timelineResult);
        } else if (episodeResult.status === "failed") {
          const failed = episodeResult.stages.find((stage) => stage.status === "failed");
          setError(failed ? `${failed.label}: ${failed.error ?? "Processing failed"}` : "Episode processing failed");
        } else {
          timer = window.setTimeout(load, 900);
        }
      } catch (reason) {
        if (!cancelled) setError(reason instanceof Error ? reason.message : "Episode request failed");
      }
    }
    load();
    return () => { cancelled = true; if (timer) window.clearTimeout(timer); };
  }, [episodeId]);

  useEffect(() => {
    if (!playing || !data || data.episode.video_available) return;
    const timer = window.setInterval(() => setCurrentTime((value) => value >= data.episode.duration ? 0 : value + 0.25), 250);
    return () => window.clearInterval(timer);
  }, [playing, data]);

  const currentScene = useMemo(() => data?.scenes.find((scene) => currentTime >= scene.start && currentTime < scene.end) ?? data?.scenes.at(-1), [data, currentTime]);
  const currentCue = useMemo(() => {
    if (!data || captions === "off") return undefined;
    const source = captions === "cc" ? data.cc_cues : data.subtitle_cues;
    return source.find((cue) => currentTime >= cue.start && currentTime <= cue.end);
  }, [data, captions, currentTime]);

  function seek(time: number) {
    setCurrentTime(Math.max(0, Math.min(data?.episode.duration ?? 0, time)));
  }

  if (error) return <ErrorState message={error} />;
  if (!data || !episode || !currentScene) return <LoadingState episode={episode} />;

  const q = search.trim().toLocaleLowerCase();
  const searchResults = q ? [
    ...data.scenes.filter((scene) => `${scene.semantic.title} ${scene.semantic.summary}`.toLocaleLowerCase().includes(q)).map((scene) => ({ id: scene.scene_id, time: scene.start, text: scene.semantic.title, type: "Scene" })),
    ...data.utterances.filter((utterance) => utterance.text.toLocaleLowerCase().includes(q)).map((utterance) => ({ id: utterance.utt_id, time: utterance.start, text: utterance.text, type: "Dialogue" })),
  ].slice(0, 6) : [];

  return (
    <main className="workspace-shell">
      <header className="workspace-header">
        <Link href="/" className="back-link" aria-label="Back to library"><ArrowLeft size={17} /></Link>
        <div className="workspace-brand"><span className="mini-glyph"><i /><i /><i /></span><strong>DRISHTI</strong></div>
        <div className="episode-heading">
          <h1>{episode.title}</h1>
          <span>{formatTime(data.episode.duration, true)}</span>
          <span className="processed-mark"><BadgeCheck size={14} />{episode.status}</span>
        </div>
        <div className="workspace-actions">
          <div className="search-box">
            <Search size={15} />
            <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search scenes or dialogue" />
            {search && <button onClick={() => setSearch("")}><X size={13} /></button>}
            {search && <div className="search-popover">
              {searchResults.length ? searchResults.map((result) => <button key={result.id} onClick={() => { seek(result.time); setSearch(""); }}><span>{result.type}</span><strong>{result.text}</strong><small>{formatTime(result.time)}</small></button>) : <p>No results in this episode.</p>}
            </div>}
          </div>
          <div className="export-wrap">
            <button className="quiet-button" onClick={() => setExportOpen((value) => !value)}><Download size={15} />Export<ChevronDown size={14} /></button>
            {exportOpen && <div className="export-menu">
              <a href={`${API_URL}/episodes/${episodeId}/export/semantic_timeline.json`}><FileJson2 size={15} />Semantic timeline</a>
              <a href={`${API_URL}/episodes/${episodeId}/export/ad_cuepoints.csv`}><Gauge size={15} />Ad cue points</a>
              <a href={`${API_URL}/episodes/${episodeId}/export/qc_report.json`}><CircleAlert size={15} />QC report</a>
            </div>}
          </div>
          <button className="icon-button" aria-label="More options"><MoreHorizontal size={18} /></button>
        </div>
      </header>

      {episode.status !== "processed" && <ProcessingBar episode={episode} />}

      <section className="stage-grid">
        <Player
          episodeId={episodeId}
          videoAvailable={data.episode.video_available}
          currentTime={currentTime}
          duration={data.episode.duration}
          scene={currentScene}
          playing={playing}
          cue={currentCue}
          captions={captions}
          onTime={seek}
          onPlaying={setPlaying}
          onCaptions={setCaptions}
        />
        <SceneInspector scene={currentScene} entities={data.entities.filter((entity) => currentScene.entity_ids.includes(entity.entity_id))} />
      </section>

      <SemanticTimeline data={data} currentTime={currentTime} onSeek={seek} />

      <section className="data-panel">
        <nav className="tab-list" aria-label="Episode data views">
          {tabs.map((tab) => <button key={tab} className={activeTab === tab ? "active" : ""} onClick={() => setActiveTab(tab)}>{tab}{tab === "QC" && <span>{data.qc.length}</span>}</button>)}
        </nav>
        <div className="tab-body">
          {activeTab === "Scenes" && <ScenesTab scenes={data.scenes} currentScene={currentScene} onSeek={seek} />}
          {activeTab === "Transcript" && <TranscriptTab utterances={data.utterances} currentTime={currentTime} onSeek={seek} />}
          {activeTab === "Entities" && <EntitiesTab episodeId={episodeId} entities={data.entities} onSeek={seek} />}
          {activeTab === "Ads" && <AdsTab episodeId={episodeId} candidates={data.ad_candidates} onSeek={seek} />}
          {activeTab === "Subtitles" && <SubtitlesTab episodeId={episodeId} subtitleCues={data.subtitle_cues} ccCues={data.cc_cues} onSeek={seek} />}
          {activeTab === "QC" && <QCTab issues={data.qc} onSeek={seek} />}
          {activeTab === "JSON" && <JsonTab data={data} episodeId={episodeId} />}
        </div>
      </section>
    </main>
  );
}

function Player({ episodeId, videoAvailable, currentTime, duration, scene, playing, cue, captions, onTime, onPlaying, onCaptions }: {
  episodeId: string; videoAvailable: boolean; currentTime: number; duration: number; scene: Scene; playing: boolean; cue?: SubtitleCue;
  captions: "off" | "sub" | "cc"; onTime: (time: number) => void; onPlaying: (playing: boolean) => void; onCaptions: (value: "off" | "sub" | "cc") => void;
}) {
  const videoRef = useRef<HTMLVideoElement>(null);
  useEffect(() => {
    const video = videoRef.current;
    if (video && Math.abs(video.currentTime - currentTime) > 1) video.currentTime = currentTime;
  }, [currentTime]);

  function togglePlayback() {
    if (videoRef.current) {
      if (videoRef.current.paused) videoRef.current.play(); else videoRef.current.pause();
    } else onPlaying(!playing);
  }

  return (
    <div className={`player-frame mood-${scene.semantic.mood}`}>
      {videoAvailable ? <video ref={videoRef} src={`${API_URL}/episodes/${episodeId}/video`} onTimeUpdate={(event) => onTime(event.currentTarget.currentTime)} onPlay={() => onPlaying(true)} onPause={() => onPlaying(false)} /> : <div className="scene-visual" aria-label="Demo scene visualization">
        <div className="visual-grain" /><div className="visual-window" /><div className="visual-table" />
        <div className="person person-a" /><div className="person person-b" />
        <div className="preview-label"><Film size={13} />Demo timeline · attach a video for picture</div>
      </div>}
      <div className="player-shade" />
      {cue && <div className="caption-render">{cue.lines.map((line) => <span key={line}>{line}</span>)}</div>}
      <div className="player-controls">
        <button className="play-button" onClick={togglePlayback} aria-label={playing ? "Pause" : "Play"}>{playing ? <Pause size={18} fill="currentColor" /> : <Play size={18} fill="currentColor" />}</button>
        <span className="player-time">{formatTime(currentTime)} <i>/</i> {formatTime(duration)}</span>
        <input aria-label="Play position" type="range" min="0" max={duration} step="0.1" value={currentTime} onChange={(event) => onTime(Number(event.target.value))} style={{ "--progress": `${(currentTime / duration) * 100}%` } as React.CSSProperties} />
        <Volume2 size={17} />
        <div className="caption-toggle">
          <Captions size={17} />
          {(["off", "sub", "cc"] as const).map((value) => <button key={value} className={captions === value ? "active" : ""} onClick={() => onCaptions(value)}>{value.toUpperCase()}</button>)}
        </div>
      </div>
    </div>
  );
}

function SceneInspector({ scene, entities }: { scene: Scene; entities: Entity[] }) {
  return <aside className="scene-inspector">
    <div className="inspector-top"><span>Current scene</span><strong>{scene.scene_id.replace("scene_", "#")}</strong></div>
    <h2>{scene.semantic.title}</h2>
    <div className="scene-time"><Clock3 size={14} />{formatTime(scene.start)} — {formatTime(scene.end)}<span>{formatTime(scene.end - scene.start)}</span></div>
    <p className="scene-summary">{scene.semantic.summary}</p>
    <div className="fact-grid">
      <div><MapPin size={14} /><span>Location</span><strong>{sentenceCase(scene.visual.location)}</strong></div>
      <div><Sparkles size={14} /><span>Mood</span><strong>{sentenceCase(scene.semantic.mood)}</strong></div>
      <div><Users size={14} /><span>Speakers</span><strong>{scene.speakers.join(", ")}</strong></div>
      <div><Tag size={14} /><span>Activity</span><strong>{sentenceCase(scene.visual.activity)}</strong></div>
    </div>
    <div className="intensity-block">
      <div><span>Narrative intensity</span><strong>{Math.round(scene.semantic.narrative_intensity * 100)}</strong></div>
      <div className="intensity-track"><i style={{ width: `${scene.semantic.narrative_intensity * 100}%` }} /></div>
      {scene.semantic.is_cliffhanger && <small><TriangleAlert size={12} />Protected cliffhanger zone</small>}
    </div>
    <div className="entity-mini-list">
      <span>Scene entities</span>
      {entities.length ? entities.map((entity) => <div key={entity.entity_id}><strong>{entity.name_bn ?? entity.name}</strong><em className={`presence ${entity.presence}`}>{presenceLabel(entity.presence)}</em><small>{Math.round(entity.confidence * 100)}%</small></div>) : <p>No product or topic entities in this scene.</p>}
    </div>
  </aside>;
}

function ScenesTab({ scenes, currentScene, onSeek }: { scenes: Scene[]; currentScene: Scene; onSeek: (time: number) => void }) {
  return <div className="table-wrap"><table className="scene-table"><thead><tr><th>Time</th><th>Scene</th><th>Location</th><th>Mood</th><th>Intensity</th><th>Entities</th></tr></thead><tbody>{scenes.map((scene) => <tr key={scene.scene_id} className={scene.scene_id === currentScene.scene_id ? "current" : ""} onClick={() => onSeek(scene.start)}><td><button>{formatTime(scene.start)}</button></td><td><strong>{scene.semantic.title}</strong><span>{scene.semantic.summary}</span></td><td>{sentenceCase(scene.visual.location)}</td><td><em className={`mood mood-${scene.semantic.mood}`}>{sentenceCase(scene.semantic.mood)}</em></td><td><div className="micro-meter"><i style={{ width: `${scene.semantic.narrative_intensity * 100}%` }} /></div><small>{scene.semantic.narrative_intensity.toFixed(2)}</small></td><td>{scene.entity_ids.length || "—"}</td></tr>)}</tbody></table></div>;
}

function TranscriptTab({ utterances, currentTime, onSeek }: { utterances: Utterance[]; currentTime: number; onSeek: (time: number) => void }) {
  return <div className="transcript-list">{utterances.map((utterance) => <button key={utterance.utt_id} className={currentTime >= utterance.start && currentTime <= utterance.end ? "current" : ""} onClick={() => onSeek(utterance.start)}><span className={`speaker-dot ${utterance.speaker}`} /> <span className="transcript-meta"><strong>{utterance.speaker_name ?? utterance.speaker}</strong><small>{utterance.speaker} · {formatTime(utterance.start)}</small></span><p lang="bn">{utterance.text}</p><em>{Math.round((utterance.confidence ?? 0) * 100)}%</em>{utterance.overlap && <i>Overlap</i>}</button>)}</div>;
}

function EntitiesTab({ episodeId, entities, onSeek }: { episodeId: string; entities: Entity[]; onSeek: (time: number) => void }) {
  const [expanded, setExpanded] = useState<string | null>(entities[0]?.entity_id ?? null);
  const grouped = Object.entries(Object.groupBy(entities, (entity) => entity.ad_categories[0] ?? "other"));
  return <div className="entity-groups">{grouped.map(([category, items]) => <section key={category}><div className="entity-group-title"><span>{sentenceCase(category)}</span><small>{items?.length} entities</small></div>{items?.map((entity) => <div className={`entity-row ${expanded === entity.entity_id ? "expanded" : ""}`} key={entity.entity_id}><button className="entity-summary" onClick={() => setExpanded(expanded === entity.entity_id ? null : entity.entity_id)}><ChevronRight size={15} /><span className="entity-name"><strong>{entity.name_bn ?? entity.name}</strong><small>{entity.name}</small></span><em className={`presence ${entity.presence}`}>{presenceLabel(entity.presence)}</em><span className={`sentiment ${entity.sentiment}`}>{entity.sentiment}</span><span className="confidence">{Math.round(entity.confidence * 100)}%</span></button>{expanded === entity.entity_id && <div className="entity-detail"><div><h4>Evidence</h4>{entity.mentions.map((mention, index) => <button key={index} onClick={() => onSeek(mention.time)}>{formatTime(mention.time)} <span>{mention.source}</span> “{mention.surface}”</button>)}</div><div><h4>Visual verification</h4>{entity.visual_check ? <><p>{entity.visual_check.note}</p><div className="frame-strip">{entity.visual_check.frames_checked.slice(0, 10).map((frame, index) => <span key={frame} className={entity.visual_check?.visible_frames.includes(frame) ? "visible" : ""}><img src={`${API_URL}/episodes/${episodeId}/frames/${frame.split("/").pop()}`} alt="" loading="lazy" onError={(event) => event.currentTarget.remove()} /><i>{index + 1}</i><small>{frame.split("/").pop()?.replace(".jpg", "")}</small></span>)}</div></> : <p>No targeted frame check was required.</p>}</div></div>}</div>)}</section>)}</div>;
}

function AdsTab({ episodeId, candidates: initial, onSeek }: { episodeId: string; candidates: AdCandidate[]; onSeek: (time: number) => void }) {
  const [candidates, setCandidates] = useState(initial);
  const [minGap, setMinGap] = useState(8);
  const [count, setCount] = useState(2);
  const [loading, setLoading] = useState(false);
  async function recalculate() { setLoading(true); try { setCandidates(await api.ads(episodeId, minGap * 60, count)); } finally { setLoading(false); } }
  async function toggle(candidate: AdCandidate) { const updated = await api.selectAd(episodeId, candidate.cand_id, !candidate.selected); setCandidates((value) => value.map((item) => item.cand_id === updated.cand_id ? updated : item)); }
  return <div className="ads-layout"><aside className="ad-settings"><h3>Break settings</h3><label>Breaks wanted <strong>{count}</strong><input type="range" min="1" max="5" value={count} onChange={(event) => setCount(Number(event.target.value))} /></label><label>Minimum gap <strong>{minGap} min</strong><input type="range" min="0" max="12" value={minGap} onChange={(event) => setMinGap(Number(event.target.value))} /></label><div className="blocked-zones"><span>Blocked zones</span><strong>Opening 00:00</strong><strong>Closing 00:00</strong></div><button className="primary-button" onClick={recalculate}>{loading ? "Calculating…" : "Recalculate"}</button><p>Selection uses cached candidates and updates instantly. No media is reprocessed.</p></aside><div className="candidate-list">{[...candidates].sort((a, b) => b.score.total - a.score.total).map((candidate, index) => <article className={`candidate-card ${candidate.selected ? "selected" : ""}`} key={candidate.cand_id}><div className="candidate-rank">{String(index + 1).padStart(2, "0")}</div><div className="candidate-content"><div className="candidate-heading"><button onClick={() => onSeek(candidate.time)}><strong>{formatTime(candidate.time)}</strong><span>{sentenceCase(candidate.kind)}</span></button><em className={`disruption ${candidate.disruption}`}>{candidate.disruption} disruption</em><button className={`selection-toggle ${candidate.selected ? "active" : ""}`} onClick={() => toggle(candidate)}><i />{candidate.selected ? "Selected" : "Select"}</button></div><p>{candidate.reason}</p><ScoreBar candidate={candidate} /><div className="score-legend"><span>Pause {Math.round(candidate.score.pause * 100)}</span><span>Scene end {Math.round(candidate.score.scene_end * 100)}</span><span>Low intensity {Math.round(candidate.score.low_intensity * 100)}</span><span>Context {Math.round(candidate.score.context_match * 100)}</span></div></div><div className="total-score"><strong>{Math.round(candidate.score.total * 100)}</strong><span>score</span></div></article>)}</div></div>;
}

function ScoreBar({ candidate }: { candidate: AdCandidate }) { const values = [candidate.score.pause, candidate.score.scene_end, candidate.score.low_intensity, candidate.score.context_match]; const colors = ["#81A7FF", "#62E6A7", "#B895E3", "#F3B64B"]; const total = values.reduce((sum, value) => sum + value, 0); return <div className="score-bar">{values.map((value, index) => <i key={colors[index]} style={{ width: `${total ? value / total * 100 : 0}%`, background: colors[index] }} />)}</div>; }

function SubtitlesTab({ episodeId, subtitleCues, ccCues, onSeek }: { episodeId: string; subtitleCues: SubtitleCue[]; ccCues: SubtitleCue[]; onSeek: (time: number) => void }) {
  const [kind, setKind] = useState<"sub" | "cc">("sub"); const cues = kind === "sub" ? subtitleCues : ccCues;
  return <div className="subtitle-layout"><div className="subtitle-tools"><div className="segmented"><button className={kind === "sub" ? "active" : ""} onClick={() => setKind("sub")}>Subtitles</button><button className={kind === "cc" ? "active" : ""} onClick={() => setKind("cc")}>Closed captions</button></div><div><a className="quiet-button" href={`${API_URL}/episodes/${episodeId}/subs/${kind}.srt`}><Download size={14} />SRT</a><a className="quiet-button" href={`${API_URL}/episodes/${episodeId}/subs/${kind}.vtt`}><Download size={14} />VTT</a></div></div><div className="cue-list">{[...cues].sort((a, b) => a.start - b.start).map((cue) => <button key={`${cue.idx}-${cue.kind}`} onClick={() => onSeek(cue.start)}><span>{cue.idx}</span><time>{formatTime(cue.start)} — {formatTime(cue.end)}</time><p lang="bn">{cue.lines.join("\n")}</p><em className={cue.cps > 17 ? "warn" : ""}>{cue.cps} cps</em><i className={cue.kind}>{cue.kind}</i></button>)}</div></div>;
}

function QCTab({ issues, onSeek }: { issues: QCIssue[]; onSeek: (time: number) => void }) {
  const [filter, setFilter] = useState("all"); const filtered = issues.filter((issue) => filter === "all" || issue.severity === filter);
  return <div className="qc-layout"><div className="qc-summary"><div><strong>{issues.filter((issue) => issue.severity === "error").length}</strong><span>Errors</span></div><div><strong>{issues.filter((issue) => issue.severity === "warn").length}</strong><span>Warnings</span></div><div><strong>{issues.filter((issue) => issue.severity === "info").length}</strong><span>Info</span></div><p><Check size={16} />Subtitle output passes demo thresholds.</p></div><div className="qc-content"><div className="filter-row"><ListFilter size={15} />{["all", "error", "warn", "info"].map((value) => <button key={value} className={filter === value ? "active" : ""} onClick={() => setFilter(value)}>{sentenceCase(value)}</button>)}</div><div className="issue-list">{filtered.map((issue) => <button key={issue.issue_id} onClick={() => onSeek(issue.time)}><span className={`issue-icon ${issue.severity}`}>{issue.severity === "warn" ? <TriangleAlert size={16} /> : <Info size={16} />}</span><span className="issue-main"><strong>{sentenceCase(issue.rule)}</strong><p>{issue.message}</p><small>{issue.suggestion}</small></span><time>{formatTime(issue.time)}</time><ChevronRight size={15} /></button>)}</div></div></div>;
}

function JsonTab({ data, episodeId }: { data: Timeline; episodeId: string }) {
  const [copied, setCopied] = useState(false); const json = JSON.stringify(data, null, 2);
  async function copy() { await navigator.clipboard.writeText(json); setCopied(true); window.setTimeout(() => setCopied(false), 1500); }
  return <div className="json-view"><div className="json-tools"><div><FileJson2 size={17} /><strong>semantic_timeline.json</strong><span>{(new Blob([json]).size / 1024).toFixed(1)} KB</span></div><div><button className="quiet-button" onClick={copy}>{copied ? <Check size={14} /> : <Copy size={14} />}{copied ? "Copied" : "Copy"}</button><a className="quiet-button" href={`${API_URL}/episodes/${episodeId}/export/semantic_timeline.json`}><Download size={14} />Download</a></div></div><pre>{json}</pre></div>;
}

function ProcessingBar({ episode }: { episode: Episode }) { return <div className="processing-bar"><span className="signal-dot" /><strong>Processing episode</strong><div><i style={{ width: `${episode.progress}%` }} /></div><span>{episode.progress}%</span><small>{episode.stages.find((stage) => stage.status === "running")?.label ?? "Queued"}</small></div>; }
function LoadingState({ episode }: { episode: Episode | null }) { const active = episode?.stages.find((stage) => stage.status === "running"); return <main className="state-screen"><span className="brand-glyph"><i /><i /><i /></span><h1>Building the semantic timeline</h1><p>{active ? `${active.label} is running. ${episode?.progress ?? 0}% complete.` : "Loading scenes, entities, captions, and ad candidates…"}</p>{episode && <div className="loading-progress"><i style={{ width: `${episode.progress}%` }} /></div>}</main>; }
function ErrorState({ message }: { message: string }) { return <main className="state-screen error"><CircleAlert size={30} /><h1>The episode could not be opened</h1><p>{message}</p><Link href="/" className="primary-button"><ArrowLeft size={16} />Back to library</Link></main>; }
