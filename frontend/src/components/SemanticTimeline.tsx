"use client";

import { useMemo, useState } from "react";
import { Minus, Plus, SlidersHorizontal } from "lucide-react";
import type { Timeline } from "@/lib/types";
import { formatTime } from "@/lib/format";

type Lane = "Scenes" | "Speech" | "Entities" | "Sounds" | "Intensity" | "Ads";

const laneY: Record<Lane, number> = {
  Scenes: 4,
  Speech: 40,
  Entities: 65,
  Sounds: 90,
  Intensity: 115,
  Ads: 150,
};

const moodColors: Record<string, string> = {
  restrained: "#596783",
  warm: "#B78B52",
  tense: "#A74C5B",
  relieved: "#3F8A72",
  focused: "#5574A7",
  melancholic: "#775D96",
};

export default function SemanticTimeline({ data, currentTime, onSeek }: { data: Timeline; currentTime: number; onSeek: (time: number) => void }) {
  const duration = data.episode.duration;
  const [zoom, setZoom] = useState(1);
  const [lanes, setLanes] = useState<Record<Lane, boolean>>({ Scenes: true, Speech: true, Entities: true, Sounds: true, Intensity: true, Ads: true });
  const windowDuration = duration / zoom;
  const start = zoom === 1 ? 0 : Math.max(0, Math.min(duration - windowDuration, currentTime - windowDuration / 2));
  const end = start + windowDuration;
  const x = (time: number) => ((time - start) / windowDuration) * 1000;
  const visibleLanes = (Object.keys(lanes) as Lane[]).filter((lane) => lanes[lane]);
  const ticks = useMemo(() => Array.from({ length: 9 }, (_, index) => start + (windowDuration / 8) * index), [start, windowDuration]);

  function seekFromPointer(event: React.PointerEvent<SVGSVGElement>) {
    const bounds = event.currentTarget.getBoundingClientRect();
    onSeek(start + ((event.clientX - bounds.left) / bounds.width) * windowDuration);
  }

  return (
    <section className="timeline-block">
      <div className="timeline-toolbar">
        <div className="timeline-title"><SlidersHorizontal size={15} />Semantic film strip</div>
        <div className="lane-switches">
          {(Object.keys(lanes) as Lane[]).map((lane) => (
            <button key={lane} className={lanes[lane] ? "active" : ""} onClick={() => setLanes((value) => ({ ...value, [lane]: !value[lane] }))}>{lane}</button>
          ))}
        </div>
        <div className="zoom-control">
          <button aria-label="Zoom out" onClick={() => setZoom((value) => Math.max(1, value / 1.5))}><Minus size={14} /></button>
          <span>{zoom.toFixed(1)}×</span>
          <button aria-label="Zoom in" onClick={() => setZoom((value) => Math.min(6, value * 1.5))}><Plus size={14} /></button>
        </div>
      </div>
      <div className="timeline-ruler">
        <span />
        <div>{ticks.map((tick) => <i key={tick} style={{ left: `${x(tick) / 10}%` }}>{formatTime(tick)}</i>)}</div>
      </div>
      <div className="timeline-chart">
        <div className="lane-labels">
          {visibleLanes.map((lane) => <span key={lane}>{lane}</span>)}
        </div>
        <svg
          role="slider"
          aria-label="Episode semantic timeline"
          aria-valuemin={0}
          aria-valuemax={duration}
          aria-valuenow={currentTime}
          viewBox="0 0 1000 182"
          preserveAspectRatio="none"
          onPointerDown={seekFromPointer}
          onWheel={(event) => { event.preventDefault(); setZoom((value) => event.deltaY < 0 ? Math.min(6, value * 1.2) : Math.max(1, value / 1.2)); }}
        >
          <defs>
            <linearGradient id="intensityFill" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#FF6B6B" stopOpacity=".65" /><stop offset="1" stopColor="#FF6B6B" stopOpacity=".04" /></linearGradient>
            <pattern id="grid" width="62.5" height="22" patternUnits="userSpaceOnUse"><path d="M 62.5 0 L 0 0 0 22" fill="none" stroke="#ffffff" strokeOpacity=".035" strokeWidth="1" /></pattern>
          </defs>
          <rect width="1000" height="182" fill="url(#grid)" />

          {lanes.Scenes && data.scenes.map((scene) => {
            const left = x(Math.max(scene.start, start));
            const right = x(Math.min(scene.end, end));
            if (right < 0 || left > 1000) return null;
            return <g key={scene.scene_id}>
              <rect x={left} y={laneY.Scenes} width={Math.max(1, right - left - 2)} height="29" rx="2" fill={moodColors[scene.semantic.mood] ?? "#596783"} opacity=".86" />
              {right - left > 80 && <text x={left + 10} y="23" fill="#fff" fontSize="10" fontWeight="600">{scene.semantic.title}</text>}
            </g>;
          })}

          {lanes.Speech && data.utterances.map((utterance) => {
            const colors: Record<string, string> = { SPK_A: "#62E6A7", SPK_B: "#81A7FF", SPK_C: "#E79BEF" };
            return <rect key={utterance.utt_id} x={x(utterance.start)} y={laneY.Speech + (utterance.speaker.charCodeAt(4) % 3) * 5} width={Math.max(2, x(utterance.end) - x(utterance.start))} height="4" rx="2" fill={colors[utterance.speaker] ?? "#DDE3EE"} />;
          })}

          {lanes.Entities && data.entities.flatMap((entity) => entity.mentions.map((mention, index) => {
            const color = entity.presence === "mentioned_only" ? "#F3B64B" : entity.presence === "shown_only" ? "#81A7FF" : entity.presence === "mentioned_and_shown" ? "#62E6A7" : "#7F8798";
            return <g key={`${entity.entity_id}-${index}`} transform={`translate(${x(mention.time)}, ${laneY.Entities + 7})`}>
              <circle r="7" fill="#101522" stroke={color} strokeWidth="2" />
              <circle r="2" fill={color} />
            </g>;
          }))}

          {lanes.Sounds && data.audio_events.map((event) => <g key={event.event_id} transform={`translate(${x(event.start)},${laneY.Sounds + 8})`}><path d="M-5 1h3l4-5v13l-4-5h-3z" fill="#9AA3B6" /><path d="M5-2q4 4 0 8" fill="none" stroke="#9AA3B6" strokeWidth="1.5" /></g>)}

          {lanes.Intensity && <path
            d={`${data.curves.intensity.filter(([time]) => time >= start && time <= end).map(([time, value], index) => `${index ? "L" : "M"}${x(time)},${laneY.Intensity + 29 - value * 27}`).join(" ")} L1000,${laneY.Intensity + 30} L0,${laneY.Intensity + 30} Z`}
            fill="url(#intensityFill)"
            stroke="#FF7D7D"
            strokeWidth="1.3"
            vectorEffect="non-scaling-stroke"
          />}

          {lanes.Ads && data.ad_candidates.map((ad) => <g key={ad.cand_id} transform={`translate(${x(ad.time)},${laneY.Ads + 13})`}>
            <path d="M0-10 8 4H-8Z" fill={ad.selected ? "#F3B64B" : "#343C50"} stroke={ad.selected ? "#F3B64B" : "#8E97AA"} strokeWidth="1.5" />
            <text x="12" y="3" fill="#CCD2DF" fontSize="9" fontWeight="700">{Math.round(ad.score.total * 100)}</text>
          </g>)}

          <line x1={x(currentTime)} x2={x(currentTime)} y1="0" y2="182" stroke="#F5F7FB" strokeWidth="1.5" vectorEffect="non-scaling-stroke" />
          <path d={`M${x(currentTime) - 5} 0h10l-5 7z`} fill="#F5F7FB" />
        </svg>
      </div>
    </section>
  );
}

