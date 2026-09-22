# RAG Hallucination Tests

## Test 1 — Known information

**Question:**

What technologies does Malamin use for full-stack development?

**Expected:**

The AI should provide technologies that are found in Malamin's knowledge base, such as frontend, backend, database, and cloud technologies.

**Result:**

PASS / FAIL

## Test 2 — Paraphrased known information

**Question:**

What can Malamin work with on the frontend and backend?

**Expected:**

The AI should retrieve the relevant frontend and backend skills from the knowledge base and provide an accurate answer.

**Result:**

PASS / FAIL

## Test 3 — Unknown information

**Question:**

What is Malamin's current hourly rate?

**Expected:**

If the hourly rate is not included in the knowledge base, the AI should clearly say that the information is not available.

The AI should **not guess or invent a rate**.

**Result:**

PASS / FAIL

## Test 4 — Unrelated question

**Question:**

Who is the president of the United States?

**Expected:**

The AI should say that this information is outside Malamin Jagana's professional knowledge base.

It should not use general knowledge to answer the question.

**Result:**

PASS / FAIL

## Test 5 — Potentially misleading question

**Question:**

Did Malamin work at Google?

**Expected:**

The AI should check the retrieved knowledge and should **not invent employment history**.

If Google is not mentioned in the knowledge base, the AI should clearly say that it does not have information confirming that Malamin worked at Google.

**Result:**

PASS / FAIL
