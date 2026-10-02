from src.config.settings import get_settings
from src.pipeline.rag_pipeline import RAGPipeline


def main():
    settings = get_settings()
    pipeline = RAGPipeline(settings)
    chunks = pipeline.build_index(rebuild=True)

    if not chunks:
        print(f"No documents found in {settings.data_path}.")
        return

    query = "What is the code of ethics?"
    answer = pipeline.ask(query)

    print("\nANSWER:\n")
    print(answer["answer"])

    print("\nSOURCES:\n")
    for source in answer.get("sources", []):
        print(f"- {source}")


if __name__ == "__main__":
    main()
