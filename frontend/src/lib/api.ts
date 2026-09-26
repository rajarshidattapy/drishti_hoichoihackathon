import type { AdCandidate, Episode, Timeline } from "./types";

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, { ...init, cache: "no-store" });
  if (!response.ok) {
    const detail = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(detail.detail ?? `Request failed (${response.status})`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  episodes: () => request<Episode[]>("/episodes"),
  episode: (id: string) => request<Episode>(`/episodes/${id}`),
  timeline: (id: string) => request<Timeline>(`/episodes/${id}/timeline`),
  ads: (id: string, minGap: number, count: number) =>
    request<AdCandidate[]>(`/episodes/${id}/ads?min_gap=${minGap}&n_breaks=${count}&blocked=0,0`),
  selectAd: (id: string, candidateId: string, selected: boolean) =>
    request<AdCandidate>(`/episodes/${id}/ads/${candidateId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ selected }),
    }),
  upload: (form: FormData) => request<Episode>("/episodes", { method: "POST", body: form }),
};

