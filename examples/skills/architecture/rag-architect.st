SKILL:   rag-architect | retrieval+chunking+embedding+eval | rag+vector-db | v1.0.0
USE:     rag-architect | when:llm+knowledge-base+semantic-search+document-qa
STACK:   rag-architect | embedding | openai-ada+sentence-transformers | vectors
STACK:   rag-architect | vector-db | pinecone+qdrant+pgvector | similarity-search
STACK:   rag-architect | retrieval | hybrid-bm25+semantic | accuracy
STACK:   rag-architect | eval | ragas+tru-lens | measure-quality
PHASE:   rag-architect | 1 | chunk | choose-strategy+test-recall
PHASE:   rag-architect | 2 | embed | generate+store-vectors
PHASE:   rag-architect | 3 | retrieve | test-retrieval-quality
PHASE:   rag-architect | 4 | generate | prompt-with-context
PHASE:   rag-architect | 5 | evaluate | measure-faithfulness+relevance
RULE:    rag-architect | evaluate-retrieval-before-generation | hard
RULE:    rag-architect | chunk-size-affects-recall | hard
RULE:    rag-architect | hybrid-retrieval-over-pure-semantic | soft
CHECK:   rag-architect | retrieval-precision-measured | required
CHECK:   rag-architect | hallucination-rate-measured | required
AVOID:   rag-architect | fixed-chunking+no-eval+blindly-trust-generation+single-retrieval-mode
