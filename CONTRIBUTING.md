# 🤝 Contributing Guide

Thanks for your interest in improving the Simple Chatbot project!

---

## **Getting Started**

### **1. Fork & Clone**
```bash
# Fork on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/simple_chatbot.git
cd simple_chatbot
```

### **2. Set Up Environment**
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env with your API key
echo "OPENAI_API_KEY=sk-your-key" > .env
```

### **3. Test Locally**
```bash
python web_chatbot.py
# Visit http://localhost:5000
```

---

## **Development Workflow**

### **Branch Naming**
- **Features:** `feature/description` (e.g., `feature/dark-mode`)
- **Bugs:** `bugfix/description` (e.g., `bugfix/session-error`)
- **Docs:** `docs/description` (e.g., `docs/api-documentation`)

### **Commit Messages**
Use clear, descriptive messages:
```
✨ Feature: Add dark mode toggle
🐛 Fix: Resolve session storage issue
📚 Docs: Update deployment guide
♻️  Refactor: Simplify chat message handling
⚙️  Config: Update requirements.txt dependencies
```

### **Creating a Pull Request**
1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "Your message"`
3. Push to your fork: `git push origin feature/your-feature`
4. Open PR on GitHub with description of changes
5. Wait for review and address feedback

---

## **Code Style**

### **Python (PEP 8)**
```python
# Good
def calculate_response(user_message: str) -> str:
    """Calculate chatbot response."""
    if not user_message.strip():
        return "Please enter a message."
    
    response = process(user_message)
    return response

# Avoid
def calc(msg):
    if msg != "": pass
    else: return process(msg)
```

### **JavaScript**
```javascript
// Good
const sendMessage = async (message) => {
    if (!message.trim()) return;
    
    const response = await fetch('/chat', {
        method: 'POST',
        body: JSON.stringify({ message })
    });
    return response.json();
};

// Avoid
const sendMessage = (msg) => {
    fetch('/chat', {method:'POST', body:JSON.stringify({message:msg})})
};
```

### **HTML/CSS**
- Use semantic HTML5 tags
- Use meaningful class names
- Keep CSS modular and reusable
- Comment complex styles

---

## **What We're Looking For**

### **✅ Good Contributions**
- Bug fixes with clear description
- Feature improvements with user benefit
- Performance optimizations
- Documentation improvements
- Code refactoring for clarity
- Test coverage
- Accessibility improvements

### **❌ We May Not Accept**
- Unrelated changes combining multiple issues
- Large rewrites without discussion
- Changes requiring new API keys
- Major breaking changes
- Style-only PRs without functional improvement

---

## **Project Structure Guide**

```
simple_chatbot/
├── web_chatbot.py          # Main Flask app - Don't modify config lightly!
├── chatbot.py              # CLI version - Feel free to enhance
├── templates/index.html    # Frontend - Style/UI improvements welcome
├── requirements.txt        # Dependencies - Update when adding packages
├── README.md              # User documentation
├── DEPLOYMENT_GUIDE.md    # Deployment instructions
├── CONTRIBUTING.md        # This file
└── .gitignore             # Never edit or commit secrets!
```

---

## **Key Configuration Points**

### **If You Want to Change AI Behavior**
Edit in `web_chatbot.py`, around line 145:
```python
session['history'] = [
    {
        "role": "system",
        "content": "Your custom system prompt here"
    }
]
```

### **If You Want to Change Model**
Edit `get_chatbot_response()` function (line ~110):
```python
response = get_openai_client().chat.completions.create(
    model="gpt-4o-mini",  # Change this (gpt-3.5-turbo, gpt-4, etc.)
    messages=messages,
    max_tokens=300,       # Adjust response length
    temperature=0.7       # Adjust creativity (0.0-1.0)
)
```

### **If You Want to Add Features**
- New routes: Add to `web_chatbot.py`
- UI changes: Modify `templates/index.html`
- Styles: Edit CSS in the `<style>` section
- New dependencies: Update `requirements.txt`

---

## **Testing Your Changes**

### **Manual Testing**
```bash
# Run locally
python web_chatbot.py

# Test these scenarios:
- [ ] Send a simple message
- [ ] Send a multi-turn conversation (verify context)
- [ ] Click "Clear" button
- [ ] Test on mobile (F12 → toggle device toolbar)
- [ ] Test error handling (invalid input, etc.)
```

### **Before Submitting PR**
```bash
# Make sure code runs without errors
python web_chatbot.py

# Check for syntax errors
python -m py_compile web_chatbot.py

# Verify .env is NOT in git
git status | grep ".env"  # Should show nothing
```

---

## **Documentation Standards**

### **Function Documentation**
```python
def get_chatbot_response(messages):
    """
    Get AI response using OpenAI API.
    
    Args:
        messages (list): Conversation history with roles
    
    Returns:
        str: AI response text
    
    Raises:
        ValueError: If OpenAI API key is not set
    """
```

### **Code Comments**
```python
# Explain WHY, not WHAT

# ✅ Good
# OpenAI requires full chat history for context retention
session['history'].append(user_message)
bot_response = get_chatbot_response(session['history'])

# ❌ Bad
# Append message to history
session['history'].append(user_message)
# Call chatbot
bot_response = get_chatbot_response(session['history'])
```

---

## **Common Issues & Solutions**

### **"Import Error" When Running**
```bash
# Install missing package
pip install -r requirements.txt

# Verify .venv is activated
source .venv/bin/activate
```

### **Changes Not Appearing**
```bash
# Clear Flask cache
rm -rf __pycache__/
rm -rf .pytest_cache/

# Restart Flask
python web_chatbot.py
```

### **Git Conflicts**
```bash
# Update your branch with main
git fetch origin
git rebase origin/main

# Or merge
git merge origin/main
```

---

## **Review Process**

1. **You create a PR** with clear description
2. **Maintainers review** - We may ask for changes
3. **You address feedback** - Update your PR
4. **We merge!** - Your code is live

### **What We Check**
- ✅ Code follows style guide
- ✅ No breaking changes
- ✅ Documentation is updated
- ✅ `.env` and secrets not included
- ✅ Works locally and on production

---

## **Feature Requests**

Have an idea? Let us know!

1. **Check existing issues** - Your idea might already exist
2. **Create an issue** with:
   - Clear title
   - Detailed description
   - Why it's useful
   - Potential implementation approach
3. **Discuss** - We'll provide feedback
4. **Implement** - Feel free to work on it!

---

## **Bug Reports**

Found a bug? We appreciate the report!

1. **Check existing issues** - Avoid duplicates
2. **Create an issue** with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)
   - Error messages/logs
3. **We'll investigate** and respond quickly

---

## **Questions or Need Help?**

- **Confused about setup?** Ask in an issue
- **Need clarification?** Comment on the PR
- **Want to discuss big changes?** Open an issue first

---

## **Resources**

- **Flask Docs:** https://flask.palletsprojects.com
- **OpenAI API:** https://platform.openai.com/docs
- **Python Style:** https://pep8.org
- **Git Guide:** https://git-scm.com/doc
- **GitHub Flow:** https://guides.github.com/introduction/flow/

---

## **Code of Conduct**

We're committed to a welcoming environment:
- Be respectful and inclusive
- Provide constructive feedback
- No harassment or discrimination
- Help others learn and grow

---

## **Thanks for Contributing! 🚀**

Your improvements make this project better for everyone.

Happy coding! 💻
