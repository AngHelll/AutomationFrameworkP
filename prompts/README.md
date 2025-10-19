# AI-Powered Automation Framework - Prompts Directory

## 🤖 Overview

This directory contains all the context, examples, and system prompts needed to power an AI assistant for this automation framework. The AI can help with code generation, troubleshooting, optimization, and learning.

## 📁 Directory Structure

```
prompts/
├── context/              # Framework documentation for AI
│   ├── framework_overview.md      # Complete framework context
│   ├── architecture.md            # Deep architectural details
│   ├── best_practices.md          # Coding standards
│   ├── troubleshooting.md         # Common issues & solutions
│   └── add_features.md            # Feature addition guide
│
├── examples/             # Few-shot learning examples
│   └── few_shot_examples.json     # Example Q&A pairs
│
├── system/               # System prompts
│   └── system_prompt.md           # AI assistant instructions
│
└── README.md            # This file
```

## 🎯 Purpose

The AI assistant can help with:

### 1. Code Generation
- Create page objects
- Write tests
- Add utilities
- Generate configuration

### 2. Troubleshooting
- Debug element location issues
- Fix timing problems
- Resolve configuration issues
- Diagnose test failures

### 3. Optimization
- Improve test performance
- Suggest better locators
- Recommend parallel execution
- Optimize resource usage

### 4. Learning
- Explain framework concepts
- Teach best practices
- Provide examples
- Answer questions

## 📚 Context Files

### framework_overview.md
Complete overview including:
- Framework identity and purpose
- Technology stack
- Project structure
- Key components
- Configuration
- Test execution
- Current statistics

### architecture.md
Deep architectural details:
- Design patterns (POM, Factory, Decorator, etc.)
- Component architecture
- Data flow diagrams
- Configuration hierarchy
- Error handling strategy
- Parallel execution model

### best_practices.md
Coding standards and patterns:
- Code organization
- Naming conventions
- Locator strategies
- Wait strategies
- Error handling
- Logging practices
- Performance tips

### troubleshooting.md
Common issues and solutions:
- Element not found errors
- Stale element references
- Timeout exceptions
- Click intercepted errors
- WebDriver issues
- Configuration problems
- Debugging strategies

### add_features.md
Step-by-step guides for:
- Adding page objects
- Creating tests
- Adding utilities
- Configuring options
- Adding test data
- Supporting new browsers

## 🎓 How to Use

### For AI Model Training
```python
# Load all context files
context = {
    "framework": read_file("context/framework_overview.md"),
    "architecture": read_file("context/architecture.md"),
    "best_practices": read_file("context/best_practices.md"),
    "troubleshooting": read_file("context/troubleshooting.md"),
    "features": read_file("context/add_features.md"),
}

# Load few-shot examples
examples = json.load(open("examples/few_shot_examples.json"))

# Load system prompt
system_prompt = read_file("system/system_prompt.md")

# Create AI assistant
assistant = create_ai_assistant(
    system_prompt=system_prompt,
    context=context,
    examples=examples
)
```

### For Chat Interfaces
```python
# Initialize with system prompt and context
chat = ChatInterface(
    system_prompt="prompts/system/system_prompt.md",
    context_dir="prompts/context/",
    examples="prompts/examples/few_shot_examples.json"
)

# User interaction
response = chat.ask("How do I create a page object?")
```

### For Code Generators
```python
# Use examples for code generation
generator = CodeGenerator(
    examples="prompts/examples/few_shot_examples.json",
    best_practices="prompts/context/best_practices.md"
)

code = generator.create_page_object(
    name="LoginPage",
    elements=["username", "password", "submit"]
)
```

## 🔄 Few-Shot Learning

The `few_shot_examples.json` contains:

### Example Categories
1. **create_page_object**: Page object creation
2. **create_test**: Test generation
3. **debug_element_not_found**: Debugging help
4. **add_configuration**: Configuration guidance
5. **optimize_performance**: Performance tips

### Conversation Patterns
- Greeting responses
- Clarification requests
- Code generation guidelines
- Response formatting

## 🛠️ Integration Examples

### Example 1: Using with OpenAI API
```python
import openai

# Load context
with open("prompts/system/system_prompt.md") as f:
    system_prompt = f.read()

with open("prompts/context/framework_overview.md") as f:
    framework_context = f.read()

# Create completion
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": framework_context},
        {"role": "user", "content": "How do I add a new page object?"}
    ]
)
```

### Example 2: Using with Anthropic Claude
```python
import anthropic

client = anthropic.Client(api_key=API_KEY)

# Load all context
context = load_all_context_files()

message = client.messages.create(
    model="claude-3-opus-20240229",
    system=context["system_prompt"] + "\n\n" + context["framework"],
    messages=[
        {"role": "user", "content": "Create a checkout page object"}
    ]
)
```

### Example 3: Local RAG System
```python
from langchain import FAISS, OpenAIEmbeddings

# Create vector store from context files
embeddings = OpenAIEmbeddings()
docs = load_markdown_files("prompts/context/")
vectorstore = FAISS.from_documents(docs, embeddings)

# Query
results = vectorstore.similarity_search(
    "How to fix element not found errors?",
    k=3
)
```

## 📊 Context Statistics

- **Total Context Size**: ~50,000 tokens
- **Context Files**: 5
- **Few-Shot Examples**: 5
- **Conversation Patterns**: 3
- **Coverage**: Complete framework documentation

## 🔧 Maintenance

### Updating Context
When framework changes:
1. Update relevant context files
2. Add new examples if needed
3. Update framework statistics
4. Test AI responses
5. Commit changes

### Adding New Examples
```json
{
  "task": "new_feature",
  "user_query": "User question",
  "ai_response": "AI response with code examples"
}
```

### Testing AI Responses
```python
# Test AI with common queries
test_queries = [
    "How do I create a page object?",
    "My test is failing with element not found",
    "How do I optimize test performance?",
]

for query in test_queries:
    response = ai_assistant.ask(query)
    validate_response(response)
```

## 🎯 Best Practices

### For Context Updates
- Keep information current
- Use clear examples
- Include code snippets
- Reference actual framework code
- Update statistics regularly

### For AI Integration
- Load all relevant context
- Use few-shot examples
- Provide clear system prompts
- Handle errors gracefully
- Log interactions

### For Users
- Ask specific questions
- Provide error messages
- Share relevant code
- Specify goals clearly
- Give feedback

## 🚀 Future Enhancements

Planned additions:
- [ ] More few-shot examples
- [ ] Video tutorial transcripts
- [ ] API documentation context
- [ ] Performance benchmarks
- [ ] CI/CD integration guides
- [ ] Advanced patterns library

## 📖 Related Documentation

- Main README: `../README.md`
- Spanish Guide: `../GUIA_NOVATOS.md`
- Fixes Documentation: `../FIXES_APPLIED.md`
- Framework Docs: `../docs/`

---

## 💡 Quick Start

To use the AI assistant:

1. **Load Context**
```bash
export CONTEXT_DIR="prompts/context"
export EXAMPLES="prompts/examples/few_shot_examples.json"
```

2. **Ask Questions**
```python
response = ai.ask("How do I create a login page object?")
```

3. **Get Help**
```python
response = ai.troubleshoot("Element not found error")
```

4. **Generate Code**
```python
code = ai.generate_page_object(
    name="ProfilePage",
    url="/profile",
    elements=["username", "email", "save_button"]
)
```

---

**The AI assistant makes this framework accessible to everyone, from beginners to experts!** 🎉

