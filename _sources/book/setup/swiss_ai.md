# Connecting to the Swiss AI Research Platform

The course environment includes an optional AI-based **Course Tutor** chat in
JupyterLab. It can read the selected notebook cell and its output to help you
understand an error or interactively explain details about the contained code. This chat might be more useful than a general-purpose AI chat, because it knows about the course material and computational environment.

The tutor uses a model hosted by the Swiss AI Research Platform. To enable it,
follow these steps. They are the same on your own computer and on the RRP.

## 1. Obtain an API key from the Swiss AI Research Platform

Navigate to the Swiss AI Research Platform: https://swissai.svc.cscs.ch

Sign in with your ETH Zurich account. Open **API Keys** and copy your key. It
should start with `sk-`.

[text](swiss_ai.md)

## 2. Set the API key in your environment

In JupyterLab:

1. Open **Settings → Jupyternaut settings**.

![alt text](../illustrations/ai_key_open_settings.png)

2. Choose **Add secret**. Set the name to `OPENAI_API_KEY` and paste the key as
   its value.

![alt text](../illustrations/ai_key_set.png)

3. Close the settings tab.
4. Open the chat in the left sidebar and ask a question to check the connection.
5. Select a code cell in a notebook and press **🎓** in the notebook toolbar.
   Check that the tutor responds about the selected cell.

The key is stored in a file `.env` in the course folder, so you only need to
enter it once.

