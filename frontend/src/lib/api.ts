import { mockApi } from "./mock";
import type { AdCandidate, Episode, Timeline } from "./types";

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
export const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK === "true";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, { ...init, cache: "no-store" });
  if (!response.ok) {
    const detail = await response.json().catch(() => ({ detail: "Request failed" }));
    const message = typeof detail.detail === "string"
      ? detail.detail
      : detail.detail?.error ?? detail.detail?.message ?? `Request failed (${response.status})`;
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}

const httpApi = {
  episodes: () => request<Episode[]>("/episodes"),
  episode: (id: string) => request<Episode>(`/episodes/${id}`),
  /** partial: whatever stages have finished so far, while the episode is still processing. */
  timeline: (id: string, partial = false) => request<Timeline>(`/episodes/${id}/timeline${partial ? "?partial=true" : ""}`),
  ads: (id: string, minGap: number, count: number) =>
    request<AdCandidate[]>(`/episodes/${id}/ads?min_gap=${minGap}&n_breaks=${count}`),
  selectAd: (id: string, candidateId: string, selected: boolean) =>
    request<AdCandidate>(`/episodes/${id}/ads/${candidateId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ selected }),
    }),
  upload: (form: FormData) => request<Episode>("/episodes", { method: "POST", body: form }),
  ingestUrl: (url: string) => request<Episode>("/episodes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  }),
};

export const api: typeof httpApi = USE_MOCK ? mockApi : httpApi;
