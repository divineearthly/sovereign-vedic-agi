"""
Nyaya — Vedic Logic and Reasoning Engine
Nyaya Sutras: 16 categories of logical reasoning
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class Pramana(Enum):
    PRATYAKSHA = "direct_perception"  # Direct evidence
    ANUMANA = "inference"              # Logical inference  
    UPAMANA = "comparison"             # Analogy
    SHABDA = "testimony"               # Authoritative source

@dataclass
class Inference:
    """Anumana — logical inference with 5 parts"""
    pratijna: str    # Proposition to prove
    hetu: str        # Reason/evidence
    udaharana: str   # Example/corollary
    upanaya: str     # Application
    nigamana: str    # Conclusion

class NyayaReasoner:
    """Vedic logical reasoning system"""
    
    def __init__(self):
        self.knowledge_base: Dict[str, Any] = {}
        self.rules: List[Inference] = []
        
    def add_fact(self, fact: str, pramana: Pramana, confidence: float = 1.0):
        """Add a fact with its epistemological source"""
        self.knowledge_base[fact] = {
            'pramana': pramana.value,
            'confidence': confidence,
            'timestamp': __import__('time').time()
        }
    
    def infer(self, query: str) -> Tuple[str, float]:
        """
        Perform logical inference using Nyaya
        Returns (conclusion, confidence)
        """
        # Step 1: Check direct knowledge (Pratyaksha)
        if query in self.knowledge_base:
            return query, self.knowledge_base[query]['confidence']
        
        # Step 2: Apply inference rules (Anumana)
        for rule in self.rules:
            if self._match_rule(rule, query):
                conclusion = rule.nigamana
                confidence = self._compute_confidence(rule)
                return conclusion, confidence
        
        # Step 3: Use analogy (Upamana)
        analogy = self._find_analogy(query)
        if analogy:
            return analogy, 0.6
        
        return "unknown", 0.0
    
    def _match_rule(self, rule: Inference, query: str) -> bool:
        """Check if rule applies to query"""
        # Simple pattern matching
        return rule.pratijna in query or rule.hetu in query
    
    def _compute_confidence(self, rule: Inference) -> float:
        """Compute confidence of inference based on available evidence"""
        confidence = 0.0
        # Check if each part is supported by knowledge base
        if rule.hetu in self.knowledge_base:
            confidence += 0.4
        if rule.udaharana in self.knowledge_base:
            confidence += 0.3
        if rule.upanaya in self.knowledge_base:
            confidence += 0.3
        return min(1.0, confidence)
    
    def _find_analogy(self, query: str) -> Optional[str]:
        """Find analogous known fact"""
        # Simple analogy by keyword matching
        for fact in self.knowledge_base:
            if any(word in fact for word in query.split()):
                return fact
        return None
    
    def add_inference_rule(self, rule: Inference):
        """Add a new inference rule"""
        self.rules.append(rule)

# Example usage
if __name__ == "__main__":
    reasoner = NyayaReasoner()
    
    # Add facts
    reasoner.add_fact("rain causes wet ground", Pramana.PRATYAKSHA)
    reasoner.add_fact("wet ground increases crop yield", Pramana.ANUMANA)
    
    # Add inference rule
    rule = Inference(
        pratijna="if rain then better crops",
        hetu="rain causes wet ground",
        udaharana="like monsoon season",
        upanaya="this area has rain",
        nigamana="crops will improve"
    )
    reasoner.add_inference_rule(rule)
    
    # Query
    result, confidence = reasoner.infer("will crops improve after rain?")
    print(f"🧠 Inference: {result} (confidence: {confidence:.2f})")
