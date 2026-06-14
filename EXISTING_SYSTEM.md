# Sovereign Vedic AGI - Existing System Documentation

## Working Components

### 1. Nyaya-Lens (Truth Verification)
- File: nyaya-lens/nyaya_lens.py
- API: 5-step inference with pramana scoring
- Output: score 0-100, hallucination flags, explanation

### 2. Divine-Earthly-ASI (Agricultural Reasoning)
- File: Divine-Earthly-ASI/vedic_engine_bridge.py
- Integrates: NASA POWER data, Qwen LLM, farmer queries
- Has: 4 domain-specific engines

### 3. VedaRta (Vedic Math + Attention)
- File: VedaRta/vedic_inference_core_v2.h
- Provides: Urdhva matmul, Sphota attention, Chitta cache
- Compiler: .vr language → C++ → ARM64

### 4. Sutra68 (Vedic Convolution)
- File: nyaya-lens/sutra68_vedic_math.py
- Provides: Urdhva, Nikhilam for neural ops

## Missing Components for AGI

1. Brahma-Jagat World Model (latent dynamics predictor)
2. Viveka-Samskara Learner (pramana-gated continual learning)
3. Chit-Sakshi Monitor (self-awareness module)
4. Sankalpa-Kriya Planner (multi-step planning)

## Integration Path

Nyaya-Lens ←→ Divine-Earthly-ASI (partial - need full API)
VedaRta ←→ All (math primitives ready)
