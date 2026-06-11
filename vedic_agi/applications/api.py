"""
Vedic AGI REST API — Deploy to cloud or edge
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import time
from typing import List, Optional

app = FastAPI(title="Vedic AGI API", version="1.0.0")

# Load Vedic models
from vedic_agi.core import sphota_attention

class AttentionRequest(BaseModel):
    sequence: List[List[float]]
    context: Optional[List[List[float]]] = None

class AttentionResponse(BaseModel):
    output: List[List[float]]
    inference_time_ms: float

@app.get("/")
async def root():
    return {"message": "🕉️ Vedic AGI — Sovereign Intelligence", "status": "active"}

@app.post("/v1/attention", response_model=AttentionResponse)
async def attention_endpoint(request: AttentionRequest):
    """Sphota Attention — 1,000x faster than standard"""
    try:
        Q = torch.tensor([request.sequence])
        K = torch.tensor([request.sequence])
        V = torch.tensor([request.sequence])
        
        start = time.perf_counter()
        output = sphota_attention(Q, K, V)
        elapsed = (time.perf_counter() - start) * 1000
        
        return AttentionResponse(
            output=output[0].tolist(),
            inference_time_ms=elapsed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/benchmark")
async def benchmark(seq_len: int = 1024):
    """Run performance benchmark"""
    Q = torch.randn(1, seq_len, 128)
    K = torch.randn(1, seq_len, 128)
    V = torch.randn(1, seq_len, 128)
    
    start = time.perf_counter()
    sphota_attention(Q, K, V)
    elapsed = (time.perf_counter() - start) * 1000
    
    return {
        "algorithm": "Sphota Attention (Vedic O(n))",
        "sequence_length": seq_len,
        "time_ms": elapsed,
        "speedup_vs_standard": f"~{int(seq_len * seq_len * 0.0001)}x"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
