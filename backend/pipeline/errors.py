class PipelineError(RuntimeError):
    """Base error whose message is safe to expose as a stage failure."""


class ConfigurationError(PipelineError):
    """A required provider, executable, or credential is unavailable."""


class ArtifactError(PipelineError):
    """An input or output artifact is missing or invalid."""

