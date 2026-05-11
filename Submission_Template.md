# Project Submission: MindMapper AI - Prompt Hacking Defenses

**Group Name:** [Your Group Name Here]  
**Group Members:**  
1. [Member 1 Name]  
2. [Member 2 Name]  
3. [Member 3 Name]  
...  

---

## 1. Introduction
MindMapper AI is an adaptive mental health chatbot that uses Groq AI (Llama 3.3) and Streamlit. To ensure the safety of our users and the integrity of our system, we have implemented several robust prompt hacking defenses. These defenses protect against direct injection, indirect injection, and code/SQL injection.

---

## 2. Implementation of Prompt Hacking Defenses

### A. Hardened System Prompt (Direct Injection Defense)
We have strengthened the AI's core instructions to include explicit security guardrails.
- **How it works:** The [SYSTEM_PROMPT](file:///c:/Users/gideo/Desktop/APPLIED AI/app.py#L145) now contains a section that explicitly forbids the AI from ignoring previous instructions, even when requested via "developer mode" or "ignore previous instructions."
- **Why it's needed:** This prevents "jailbreaking" attempts where a user tries to override the AI's intended role (e.g., trying to turn the mental health bot into a technical assistant).

### B. Input Delimiters (Direct Injection Defense)
We use clear boundaries to separate user input from system instructions.
- **How it works:** In [main](file:///c:/Users/gideo/Desktop/APPLIED AI/app.py#L367-L372), all user messages are wrapped in XML-style tags (`<user_input>...</user_input>`) before being sent to the LLM.
- **Why it's needed:** This helps the AI understand exactly where user input ends and system instructions begin, making it much harder for a user to "escape" their role and give the AI new commands.

### C. Keyword-Based Guardrail (Pre-Processing Defense)
A dedicated function scans all incoming text before it reaches the AI model.
- **How it works:** The [is_injection_attempt](file:///c:/Users/gideo/Desktop/APPLIED AI/app.py#L162) function checks for known malicious keywords like "system update," "sql_admin," and "drop table."
- **Why it's needed:** This provides an immediate, low-latency filter that stops the most common and obvious injection attempts before they can even be processed by the LLM.

### D. File Upload Protection (Indirect Injection Defense)
Since our app supports PDF and TXT uploads, we've extended our defenses to handle "poisoned" files.
- **How it works:** In [analyze_file](file:///c:/Users/gideo/Desktop/APPLIED AI/app.py#L235), we extract text from uploaded documents and run it through the same `is_injection_attempt` guardrail.
- **Why it's needed:** Attackers can hide malicious instructions inside files that a human might not see (e.g., white text on a white background in a PDF). Our system scans all content to ensure it stays safe.

### E. SQL Parameterization (Code Injection Defense)
To protect our SQLite database (`mindmapper_pro.db`), we use industry-standard coding practices.
- **How it works:** All database functions ([init_db](file:///c:/Users/gideo/Desktop/APPLIED AI/app.py#L20), [save_log](file:///c:/Users/gideo/Desktop/APPLIED AI/app.py#L32), [get_history](file:///c:/Users/gideo/Desktop/APPLIED AI/app.py#L40)) use **parameterized queries** instead of f-strings or string concatenation.
- **Why it's needed:** This is the most effective defense against SQL injection. It ensures that user input is always treated as data, never as part of a command that could delete or leak our database.

---

## 3. Quality of Explanation
These defenses were chosen based on the **Defense-in-Depth** principle. We don't rely on just one check; instead, we have layers of security:
1. **Pre-processing layer** (Keyword checks)
2. **Contextual layer** (Delimiters and System Prompt hardening)
3. **Architectural layer** (Parameterized SQL)

By combining these, we ensure that even if one layer is bypassed, the others continue to protect the system and the user's data.

---

## 4. Conclusion
Through these implementations, MindMapper AI is no longer just a basic chatbot but a secure, trustworthy digital health tool that resists malicious manipulation while providing empathetic support to its users.
