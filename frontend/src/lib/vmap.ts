export type AdBreak = { id: string; time: number; mediaUrl: string; title: string };

/** Linear breaks from a VMAP 1.0 manifest with inline VAST (as served by /episodes/{id}/ads/vmap.xml). */
export function parseVmap(xml: string): AdBreak[] {
  if (!xml) return [];
  const doc = new DOMParser().parseFromString(xml, "application/xml");
  return Array.from(doc.getElementsByTagNameNS("*", "AdBreak")).flatMap((node) => {
    const mediaUrl = node.getElementsByTagName("MediaFile")[0]?.textContent?.trim();
    const [hours, minutes, seconds] = (node.getAttribute("timeOffset") ?? "").split(":").map(Number);
    if (!mediaUrl || [hours, minutes, seconds].some((value) => Number.isNaN(value))) return [];
    return [{
      id: node.getAttribute("breakId") ?? `${hours}:${minutes}:${seconds}`,
      time: hours * 3600 + minutes * 60 + seconds,
      mediaUrl,
      title: node.getElementsByTagName("AdTitle")[0]?.textContent ?? "Advertisement",
    }];
  });
}
