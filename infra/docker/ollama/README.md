# Ollama model setup

After `docker compose up --build`, pull a model into the running Ollama container:

```bash
docker compose -f infra/docker/docker-compose.yml exec ollama ollama pull llama3.1:8b
```

You can change `LLM_MODEL` in `.env` to any pulled local model.
