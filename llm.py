from google import genai
import streamlit as st
import time


class LLM:

    # Only retried when nothing has streamed yet for the current attempt,
    # so a retry never duplicates content the user has already seen.
    MAX_RETRIES = 2
    RETRY_DELAY_SECONDS = 1.5

    def __init__(self):

        self.client = genai.Client(
            api_key=st.secrets["GEMINI_API_KEY"]
        )

        self.model = "gemini-3.5-flash-lite"


    def stream(self, prompt):

        attempt = 0

        while True:

            attempt += 1

            chunks_yielded = 0

            try:

                response = self.client.models.generate_content_stream(
                    model=self.model,
                    contents=prompt
                )

                for chunk in response:

                    if chunk.text:

                        chunks_yielded += 1

                        yield {
                            "message": {
                                "content": chunk.text
                            }
                        }

                return

            except Exception as e:

                error = str(e)

                print(f"Gemini Error (attempt {attempt}):", error)

                is_transient = "500" in error or "503" in error or "UNAVAILABLE" in error

                # Retry only if this attempt produced no visible content yet -
                # otherwise a retry would duplicate what's already on screen.
                if chunks_yielded == 0 and is_transient and attempt <= self.MAX_RETRIES:

                    time.sleep(self.RETRY_DELAY_SECONDS)

                    continue

                if "429" in error or "RESOURCE_EXHAUSTED" in error:

                    message = (
                        "Gemini API quota exceeded. Please try again later."
                    )

                elif "401" in error or "API key" in error:

                    message = (
                        "Invalid Gemini API key."
                    )

                elif "500" in error or "503" in error or "UNAVAILABLE" in error:

                    message = (
                        "Gemini service is temporarily unavailable. "
                        "Please try again in a moment."
                    )

                else:

                    message = (
                        "Unable to generate response."
                    )

                # Flagged as an error chunk so the caller can show it as a
                # notice instead of appending it into the answer text.
                yield {
                    "message": {
                        "content": message
                    },
                    "error": True,
                    "partial": chunks_yielded > 0
                }

                return