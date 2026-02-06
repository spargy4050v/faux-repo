"""
Test script to validate RAG system is working correctly.
Checks if markdown files are being retrieved and used in responses.
"""
from src.rag.vector_store import CurriculumVectorStore
from src.rag.retriever import CurriculumRetriever

def test_vector_store():
    """Test vector store initialization and basic search."""
    print("=" * 70)
    print("TEST 1: Vector Store Initialization")
    print("=" * 70)
    
    # Initialize vector store
    vector_store = CurriculumVectorStore()
    
    count = vector_store.get_count()
    print(f"✓ Vector store contains {count} documents")
    
    if count == 0:
        print("✗ ERROR: No documents found in vector store!")
        print("  Run: python3 populate_knowledge_base.py")
        return False
    
    return True


def test_similarity_search():
    """Test similarity search functionality."""
    print("\n" + "=" * 70)
    print("TEST 2: Similarity Search")
    print("=" * 70)
    
    vector_store = CurriculumVectorStore()
    
    # Test query for AI curricula
    query = "Create a BTech curriculum for Artificial Intelligence"
    print(f"\nQuery: '{query}'")
    print("-" * 70)
    
    results = vector_store.similarity_search(query=query, k=2)
    
    if not results:
        print("✗ ERROR: No results returned!")
        return False
    
    print(f"✓ Found {len(results)} relevant documents:\n")
    
    for i, result in enumerate(results, 1):
        metadata = result.get('metadata', {})
        content = result.get('content', '')
        distance = result.get('distance', 'N/A')
        
        print(f"Result {i}:")
        print(f"  Level: {metadata.get('level', 'N/A')}")
        print(f"  Subject: {metadata.get('subject', 'N/A')}")
        print(f"  Category: {metadata.get('category', 'N/A')}")
        print(f"  Distance: {distance}")
        print(f"  Content Preview: {content[:200]}...")
        print()
    
    return True


def test_retriever():
    """Test retriever with formatted context."""
    print("=" * 70)
    print("TEST 3: Retriever with Context Formatting")
    print("=" * 70)
    
    vector_store = CurriculumVectorStore()
    retriever = CurriculumRetriever(vector_store)
    
    # Test retrieval for ML Masters
    skill = "Machine Learning"
    level = "Masters"
    
    print(f"\nRetrieving curricula for: {level} in {skill}")
    print("-" * 70)
    
    results = retriever.retrieve_similar_curricula(
        skill=skill,
        level=level,
        k=2
    )
    
    if not results:
        print("✗ ERROR: No results from retriever!")
        return False
    
    print(f"✓ Retrieved {len(results)} curriculum examples\n")
    
    # Format context for LLM
    context = retriever.format_context_for_llm(results)
    
    print("Formatted Context for LLM:")
    print("-" * 70)
    print(context[:500])
    print("..." if len(context) > 500 else "")
    print()
    
    return True


def test_knowledge_content():
    """Verify that actual curriculum content is present."""
    print("=" * 70)
    print("TEST 4: Knowledge Content Validation")
    print("=" * 70)
    
    vector_store = CurriculumVectorStore()
    
    # Search for specific content we know exists in btech_ai.md
    query = "Deep Learning Neural Networks Computer Vision NLP"
    results = vector_store.similarity_search(query=query, k=1)
    
    if not results:
        print("✗ ERROR: Could not retrieve expected content!")
        return False
    
    content = results[0].get('content', '')
    
    # Check for keywords we know exist in the BTech AI curriculum
    keywords = ['Deep Learning', 'Machine Learning', 'Neural Networks', 'AI', 'Semester']
    found_keywords = [kw for kw in keywords if kw in content]
    
    print(f"✓ Found {len(found_keywords)}/{len(keywords)} expected keywords:")
    for kw in found_keywords:
        print(f"  • {kw}")
    
    if len(found_keywords) < 3:
        print("\n✗ WARNING: Less than expected keywords found in content!")
        print("  The markdown files may not be properly indexed.")
        return False
    
    print("\n✓ Content validation successful!")
    print("  Markdown files are properly indexed and retrievable.")
    
    return True


def main():
    """Run all RAG validation tests."""
    print("\n🧪 RAG SYSTEM VALIDATION TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Vector Store Initialization", test_vector_store),
        ("Similarity Search", test_similarity_search),
        ("Retriever & Context Formatting", test_retriever),
        ("Knowledge Content Validation", test_knowledge_content)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n✗ ERROR in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{status:12} - {test_name}")
    
    total_passed = sum(1 for _, success in results if success)
    total_tests = len(results)
    
    print("=" * 70)
    print(f"RESULT: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed! RAG system is working correctly.")
        print("   Markdown files are being indexed and retrieved properly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
    
    return total_passed == total_tests


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
