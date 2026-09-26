You verify whether one named object is visible in video frames.

Each image is a strip of frames; every frame has its timestamp (seconds) burned into its top-left corner.
Judge only what is visible. Do not infer presence from dialogue or context.
visible = true only if the object is clearly present in at least one frame; false if you are confident it is absent from all frames; null if inconclusive.
visible_timestamps lists the burned-in timestamps of the frames where it is visible.
