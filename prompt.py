class PromptBuilder:


    def build_prompt(self, question, context, history_text=""):

        history_section = ""

        if history_text:

            history_section = f"""
Recent conversation (for context only -- the user's new question may be
a short follow-up that refers back to this, e.g. "and of uk" after
"capital of india" means "what is the capital of uk"):
{history_text}
"""

        prompt = f"""
You are a helpful AI assistant.
{history_section}
Using only the provided context below, respond to the user's new
question:

- If the question asks for a specific fact, extract and state that
  fact clearly.
- If the question is open-ended or asks for an overview, a summary,
  or "the latest" on a broad topic (e.g. "latest news"), summarize
  the relevant points from the context in a clear, well-organized
  way instead of looking for one single "answer".

Only say "I don't have enough information." if the context is
genuinely unrelated to what the user is asking about -- do not say
this just because the context doesn't contain one neat, single-line
answer.

Provide a clear and well-structured answer.

Context:
{context}


New Question:
{question}


Answer:
"""

        return prompt


    def build_direct_prompt(self, question, history_text=""):

        history_section = ""

        if history_text:

            history_section = f"""
Recent conversation (for context only -- the user's new question may be
a short follow-up that refers back to this):
{history_text}
"""

        prompt = f"""
You are a helpful, knowledgeable AI assistant.
{history_section}
Answer the user's question thoroughly and directly using your own
knowledge. Be concrete and specific -- if asked to teach a topic
(e.g. a language, a skill, a concept), give real, usable content
(actual vocabulary, real examples, concrete steps), not a general
description of where one could learn it.

Question:
{question}


Answer:
"""

        return prompt