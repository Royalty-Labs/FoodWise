# FoodWise N-ATLaS Integration

This document describes the intended integration between FoodWise and N-ATLaS, the multilingual language-model technology being explored for the FoodWise assistant.

**Important:** Documentation of an integration does not by itself confirm that every assistant capability works in the deployed application. Verify model responses, language handling, API behaviour, and performance before describing them as fully operational.

## Integration Goals

The integration aims to support an assistant that can help users interact with FoodWise through natural-language requests.

Potential use cases include:

- Answering questions about food budgeting.
- Helping users understand their food plans.
- Supporting food-related questions in supported languages.
- Providing a conversational interface alongside the application's existing API functionality.

Target language coverage includes English, Yoruba, Igbo, Hausa, and Nigerian-accented English. The accuracy and coverage of each language must be evaluated through testing.

## Integration Architecture

The intended request flow is:

1. A user submits a message through the FoodWise frontend.
2. The FoodWise backend receives and processes the request.
3. The assistant service determines the appropriate handling path.
4. Where configured, the backend sends a request to the N-ATLaS model server.
5. The backend processes the model response and returns an answer to the frontend.

The exact flow depends on the current implementation. Check the backend assistant service and configuration before changing this description to reflect additional capabilities.

## Local Model Server

The local development setup has used a `llama.cpp`-compatible server with an OpenAI-style chat-completions endpoint.

Previously used local settings include:

- **Server address:** `http://127.0.0.1:8080`
- **Chat endpoint:** `/v1/chat/completions`
- **Model alias:** `N-ATLaS-local`
- **Model format:** GGUF
- **Quantization:** Q4_K_M
- **Context length:** 2048 tokens
- **CPU threads:** 4

These are recorded development settings, not universal requirements. Confirm the current server configuration before relying on them.

## Model Files and Credentials

Large model files should remain outside Git version control.

- Do not commit `.gguf` model files.
- Do not commit API keys, access tokens, or credentials.
- Do not publish private model repositories or restricted download links.
- Follow the model's licence and distribution requirements.

FoodWise's `.gitignore` includes rules intended to exclude model weights. Check `git status` before staging files.

## Configuration

The model server must be running and accessible to the backend before requests can succeed.

Use the configuration mechanism supported by the current assistant service. Do not assume a particular environment-variable name unless it exists in the code.

For a local server, the backend must be able to reach the configured host and port. A local address such as `127.0.0.1` refers to the machine running the backend; it will not automatically refer to a separately deployed server.

Never place private credentials in frontend variables prefixed with `VITE_`.

## Verification Checklist

Before considering the integration operational, verify the following:

- [ ] The model server starts successfully.
- [ ] The chat-completions endpoint returns a valid response.
- [ ] The FoodWise backend can reach the model server.
- [ ] The assistant endpoint returns a response to the frontend.
- [ ] Food-plan requests follow the correct application logic.
- [ ] Unsupported or malformed requests are handled safely.
- [ ] Timeouts and model-server errors are handled appropriately.
- [ ] English, Yoruba, Igbo, and Hausa responses are evaluated separately.
- [ ] Nigerian-accented speech is tested if speech input is implemented.
- [ ] Response latency is measured under realistic conditions.
- [ ] The deployed configuration is tested independently of local development.

## Performance Considerations

Local model inference may be slow depending on hardware, model size, quantization, context length, and generation settings.

When diagnosing slow responses, measure:

- Total request duration.
- Time spent waiting for the model server.
- Time to first generated token, where measurable.
- Token generation speed, where available.
- Timeout frequency and error rates.

Avoid assuming that a slow response is caused by the frontend alone. Measure each part of the request flow.

## Text and Speech Are Different Capabilities

A working text-chat integration does not automatically establish working speech recognition or speech generation.

If FoodWise adds speech support, test the audio-processing components independently, including language recognition, transcription accuracy, response generation, and audio output where applicable.

## Further Reading

- [FoodWise Development Setup](development-setup.md)
- [FoodWise Testing Guide](testing.md)
- [FoodWise Backend README](../backend/README.md)