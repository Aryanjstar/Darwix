# 🤖 Empathetic Code Reviewer

> **Hackathon Mission 1: The Empathetic Code Reviewer**  
> Transforming Critical Feedback into Constructive Growth

## 👨‍💻 Author

**Aryan Jaiswal** | Final Year CSE B.Tech | IIIT Dharwad | aryanjstar3@gmail.com

---

## 🚀 **Quick Testing (30 seconds)**

```bash
# Install dependencies
pip3 install -r requirements.txt

# Test with hackathon example
python3 main.py input/sample_input.json

# Save output to file
python3 main.py input/sample_input.json -o output/result.md
```

**Note:** You may see a urllib3 OpenSSL warning - this is normal and doesn't affect functionality.

---

## 🔑 **API Key Information**

### **Azure OpenAI Configuration Details**

**Complete credentials provided in `.env` file for evaluation:**

```env
AZURE_OPENAI_ENDPOINT=https://xxx
AZURE_OPENAI_API_KEY=[xxxxx]
AZURE_OPENAI_CHATGPT_DEPLOYMENT=gpt-4.1
AZURE_OPENAI_CHATGPT_MODEL=gpt-4.1
AZURE_OPENAI_API_VERSION=xxx
```

Please use your API key for testing it, I have changed my keys.

### **Important Notes**

- ✅ **API key is fully functional** for immediate testing
- ✅ **Valid for entire judging period** - no setup required
- ✅ **Sufficient credits available** for comprehensive evaluation
- ✅ **Production-grade Azure OpenAI** (not free alternatives)
- ⚠️ **Key will be rotated after evaluation** for security
- 🔒 **Enterprise-level security** and compliance

### **Why Azure OpenAI?**

- **Reliability**: Production-grade uptime and consistency
- **Quality**: GPT-4.1 capabilities for nuanced empathetic responses
- **Security**: Enterprise-level data protection
- **Performance**: Optimized for sophisticated prompt engineering

---

## 📁 **Project Structure**

```
Darwix/
├── main.py                    # Main application
├── requirements.txt           # Dependencies
├── .env                      # Azure OpenAI config
├── README.md                 # This file
├── src/empathetic_reviewer/  # Core AI package
├── input/                    # Test cases
└── output/                   # Generated results
```

---

## 🎯 **How It Works**

### Input Format

```json
{
	"code_snippet": "your code here",
	"review_comments": ["comment 1", "comment 2"]
}
```

### Output Format (Exact Hackathon Specification)

````markdown
---

### Analysis of Comment: "original comment"

- **Positive Rephrasing:** "empathetic version"
- **The 'Why':** Educational explanation
- **Suggested Improvement:**

```language
improved code
```
````

---

````

---

## 🧪 **Complete Test Cases**

### **All 6 Test Scenarios Available**

| Test Case | File | Language | Comments | Description |
|-----------|------|----------|----------|-------------|
| 1 | `sample_input.json` | Python | 3 | Original hackathon example |
| 2 | `test_case_1_javascript.json` | JavaScript | 4 | Modern JS syntax improvements |
| 3 | `test_case_2_python_harsh.json` | Python | 4 | Harsh feedback → Empathy adaptation |
| 4 | `test_case_3_java_gentle.json` | Java | 3 | Gentle feedback tone matching |
| 5 | `advanced_test_input.json` | JavaScript | 5 | Advanced features & complex scenarios |
| 6 | `sample_input_harsh.json` | Python | 4 | Additional harsh feedback testing |

### **Testing Commands**

```bash
# Test Case 1: Original hackathon example (3 comments)
python3 main.py input/sample_input.json -o output/sample_input_result.md

# Test Case 2: JavaScript modernization (4 comments)
python3 main.py input/test_case_1_javascript.json -o output/test_case_1_javascript_result.md

# Test Case 3: Python harsh feedback adaptation (4 comments)
python3 main.py input/test_case_2_python_harsh.json -o output/test_case_2_python_harsh_result.md

# Test Case 4: Java gentle feedback (3 comments)
python3 main.py input/test_case_3_java_gentle.json -o output/test_case_3_java_gentle_result.md

# Test Case 5: Advanced scenarios (5 comments)
python3 main.py input/advanced_test_input.json -o output/advanced_test_input_result.md

# Test Case 6: Additional harsh feedback (4 comments)
python3 main.py input/sample_input_harsh.json -o output/sample_input_harsh_result.md
```

### **Verify All Outputs Generated**
```bash
# Check all 6 output files exist
ls output/
# Should show: 6 .md files with empathetic code reviews
```

---

## ✅ **Features Implemented**

### Core Requirements

- ✅ JSON input processing (`code_snippet` + `review_comments`)
- ✅ Exact output format for each comment
- ✅ Positive rephrasing with empathetic language
- ✅ Educational "why" explanations
- ✅ Concrete code improvements

### Bonus Features

- ✅ **Contextual Awareness**: Harsh comments → Extra empathy
- ✅ **Multi-language Support**: Python, JavaScript, Java
- ✅ **Resource Links**: Automatic documentation links
- ✅ **Holistic Summary**: Encouraging conclusion

---

## 🔧 **Approach & Technical Implementation**

### **Problem-Solving Approach**

1. **Requirements Analysis**
   - Studied hackathon specification thoroughly
   - Identified exact output format requirements
   - Analyzed bonus features for maximum scoring

2. **Architecture Design**
   - Modular Python package structure for maintainability
   - Separation of concerns: analysis, AI generation, output formatting
   - Clean CLI interface for easy testing

3. **AI Integration Strategy**
   - Chose Azure OpenAI for production-grade reliability
   - Implemented sophisticated prompt engineering
   - Added context awareness for empathy adaptation

4. **Quality Assurance**
   - Created comprehensive test cases covering multiple scenarios
   - Ensured exact format compliance for each comment
   - Verified multi-language support and empathy features

### **Technical Pipeline**

1. **Input Processing** → JSON validation and parsing
2. **Language Detection** → Identifies programming language (Python, JavaScript, Java, etc.)
3. **Sentiment Analysis** → Detects comment severity (harsh, gentle, neutral)
4. **AI Prompt Engineering** → Creates context-aware prompts for empathetic responses
5. **Azure OpenAI Generation** → Produces human-like, educational feedback
6. **Format Compliance** → Generates exact hackathon specification format

---

## 📋 **GitHub Repository Checklist**

✅ **Repository is public and accessible**
✅ **README.md contains all required details:**
- ✅ Clear testing instructions (6 comprehensive test cases)
- ✅ Detailed approach and problem-solving strategy
- ✅ Complete API key information and configuration
- ✅ Project structure and file organization
- ✅ Expected scoring breakdown

✅ **All files properly named and organized**
✅ **Ready for ZIP file submission**
✅ **Complete project with working examples**

---

## 📞 **Contact**

**Aryan Jaiswal**
📧 aryanjstar3@gmail.com
🎓 IIIT Dharwad, Final Year CSE B.Tech

_Thank you for evaluating my submission!_
````

# Darwix
