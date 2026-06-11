"""
Chitta Samskara — Vedic Memory System
Based on Yoga Sutras: Memory is impressions left by experiences
"""

import torch
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Samskara:
    """An impression/memory with resonance score"""
    content: torch.Tensor
    timestamp: datetime
    importance: float  # 0-1 scale
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.now)
    
    def resonance(self) -> float:
        """Calculate resonance (importance * recency * frequency)"""
        recency = 1.0 / (1.0 + (datetime.now() - self.timestamp).seconds / 86400)
        frequency = min(1.0, self.access_count / 100)
        return self.importance * recency * frequency

class ChittaMemory:
    """
    Vedic memory system: Chitta (subconscious store) + Samskara (impressions)
    Implements efficient retrieval based on resonance
    """
    
    def __init__(self, capacity: int = 10000, dim: int = 512):
        self.capacity = capacity
        self.dim = dim
        self.samskaras: List[Samskara] = []
        self.index: Dict[int, int] = {}  # hash -> index mapping
        
    def store(self, content: torch.Tensor, importance: float = 0.5) -> int:
        """Store a memory impression"""
        # Create samskara
        samskara = Samskara(
            content=content.clone().detach(),
            timestamp=datetime.now(),
            importance=importance
        )
        
        # Evict if over capacity (remove lowest resonance)
        if len(self.samskaras) >= self.capacity:
            resonance_scores = [s.resonance() for s in self.samskaras]
            min_idx = min(range(len(resonance_scores)), key=resonance_scores.__getitem__)
            self.samskaras.pop(min_idx)
        
        self.samskaras.append(samskara)
        return len(self.samskaras) - 1
    
    def retrieve(self, query: torch.Tensor, top_k: int = 5) -> List[Samskara]:
        """Retrieve most relevant memories"""
        if not self.samskaras:
            return []
        
        # Compute similarity with all memories
        query_norm = query / query.norm()
        similarities = []
        
        for samskara in self.samskaras:
            mem_norm = samskara.content / samskara.content.norm()
            similarity = torch.dot(query_norm.flatten(), mem_norm.flatten()).item()
            resonance = samskara.resonance()
            score = similarity * resonance  # Combine similarity and resonance
            
            similarities.append((score, samskara))
        
        # Sort by score and return top_k
        similarities.sort(key=lambda x: x[0], reverse=True)
        
        # Update access counts
        for _, samskara in similarities[:top_k]:
            samskara.access_count += 1
            samskara.last_accessed = datetime.now()
        
        return [s for _, s in similarities[:top_k]]
    
    def consolidate(self):
        """Consolidate short-term to long-term memory"""
        # Increase importance of frequently accessed memories
        for samskara in self.samskaras:
            if samskara.access_count > 10:
                samskara.importance = min(1.0, samskara.importance + 0.1)
    
    def save(self, path: str):
        """Save memory to disk"""
        data = []
        for s in self.samskaras:
            data.append({
                'content': s.content.cpu().numpy().tolist(),
                'timestamp': s.timestamp.isoformat(),
                'importance': s.importance,
                'access_count': s.access_count
            })
        with open(path, 'w') as f:
            json.dump(data, f)
    
    def load(self, path: str):
        """Load memory from disk"""
        with open(path, 'r') as f:
            data = json.load(f)
        self.samskaras = []
        for item in data:
            self.samskaras.append(Samskara(
                content=torch.tensor(item['content']),
                timestamp=datetime.fromisoformat(item['timestamp']),
                importance=item['importance'],
                access_count=item['access_count']
            ))

# Quick test
if __name__ == "__main__":
    memory = ChittaMemory(capacity=100, dim=128)
    
    # Store some memories
    for i in range(10):
        mem = torch.randn(128)
        memory.store(mem, importance=0.8)
    
    # Retrieve similar
    query = torch.randn(128)
    results = memory.retrieve(query, top_k=3)
    print(f"✅ Retrieved {len(results)} memories")
