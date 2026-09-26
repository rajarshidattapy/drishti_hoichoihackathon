import Workspace from "@/components/Workspace";

export default async function EpisodePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <Workspace episodeId={id} />;
}

