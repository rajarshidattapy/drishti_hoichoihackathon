export function formatTime(totalSeconds: number, withHours = false) {
  const value = Math.max(0, Math.floor(totalSeconds));
  const hours = Math.floor(value / 3600);
  const minutes = Math.floor((value % 3600) / 60);
  const seconds = value % 60;
  if (withHours || hours > 0) return `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
  return `${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
}

export function presenceLabel(value: string) {
  return {
    mentioned_and_shown: "Mentioned + shown",
    mentioned_only: "Mentioned only",
    shown_only: "Shown only",
    unverified: "Unverified",
  }[value] ?? value;
}

export function sentenceCase(value: string) {
  return value.replaceAll("_", " ").replace(/^./, (letter) => letter.toUpperCase());
}

