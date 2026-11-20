class ChunkingService:

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str) -> list[str]:
        words = text.split()

        chunks = []
        start = 0

        while start < len(words):
            end = start + self.chunk_size

            chunk = " ".join(words[start:end])
            chunks.append(chunk)

            start = end - self.overlap

        return chunks


chunking_service = ChunkingService()