#!/usr/bin/env python3
"""
Star Dust Frequencies: Resonance Calculator
NŪR Protocol Implementation for Partnership Scoring

This module provides the core resonance calculation algorithms
for the ScrollVerse partnership evaluation system.
"""

from dataclasses import dataclass
from typing import Dict, Optional
from enum import Enum


class ResonanceLevel(Enum):
    """Classification levels for resonance scores"""
    PERFECT_RESONANCE = "PERFECT_RESONANCE"      # 9.0-10.0
    HIGH_PRIORITY = "HIGH_PRIORITY"              # 8.0-8.9
    GOOD_FIT = "GOOD_FIT"                        # 6.0-7.9
    MODERATE_POTENTIAL = "MODERATE_POTENTIAL"    # 4.0-5.9
    LOW_RESONANCE = "LOW_RESONANCE"              # 2.0-3.9
    MISALIGNED = "MISALIGNED"                    # 0.0-1.9


@dataclass
class FrequencyComponents:
    """
    The four fundamental frequencies of the NŪR Protocol
    """
    truth_alignment: float      # 0.0 to 1.0 - Alignment with ScrollVerse values
    cultural_fit: float         # 0.0 to 1.0 - Cultural compatibility
    strategic_synergy: float    # 0.0 to 1.0 - Strategic value alignment
    resistance_factor: float    # 0.0 to 1.0 - Barriers (lower is better)
    
    def __post_init__(self):
        """Validate frequency values"""
        for field_name in ['truth_alignment', 'cultural_fit', 'strategic_synergy', 'resistance_factor']:
            value = getattr(self, field_name)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{field_name} must be between 0.0 and 1.0, got {value}")


@dataclass
class ResonanceScore:
    """
    Complete resonance evaluation for a partnership opportunity
    """
    frequencies: FrequencyComponents
    partner_name: Optional[str] = None
    
    @property
    def overall_score(self) -> float:
        """
        Calculate overall resonance score using NŪR formula
        
        Formula: RS = ((TA + CF + SS) / 3) / RF × 10
        
        Special cases:
        - If RF = 0 or very close to 0: Returns 10.0 (perfect resonance)
        - Score is capped at 10.0 maximum
        
        Returns:
            float: Score from 0.0 to 10.0
        """
        f = self.frequencies
        
        # Small epsilon to prevent division by exact zero due to floating point precision
        EPSILON = 1e-10
        
        # Handle special case: zero or near-zero resistance = perfect resonance
        if f.resistance_factor < EPSILON:
            return 10.0
        
        # Calculate average of positive frequencies
        avg_positive = (f.truth_alignment + f.cultural_fit + f.strategic_synergy) / 3.0
        
        # Divide by resistance and scale to 10
        score = (avg_positive / f.resistance_factor) * 10.0
        
        # Cap at 10.0
        return min(score, 10.0)
    
    @property
    def classification(self) -> ResonanceLevel:
        """
        Classify the resonance score into actionable levels
        
        Returns:
            ResonanceLevel: Classification enum value
        """
        score = self.overall_score
        
        if score >= 9.0:
            return ResonanceLevel.PERFECT_RESONANCE
        elif score >= 8.0:
            return ResonanceLevel.HIGH_PRIORITY
        elif score >= 6.0:
            return ResonanceLevel.GOOD_FIT
        elif score >= 4.0:
            return ResonanceLevel.MODERATE_POTENTIAL
        elif score >= 2.0:
            return ResonanceLevel.LOW_RESONANCE
        else:
            return ResonanceLevel.MISALIGNED
    
    @property
    def recommendation(self) -> str:
        """
        Get actionable recommendation based on classification
        
        Returns:
            str: Human-readable recommendation
        """
        recommendations = {
            ResonanceLevel.PERFECT_RESONANCE: "Immediate executive engagement - highest priority partnership",
            ResonanceLevel.HIGH_PRIORITY: "Priority outreach with senior team involvement",
            ResonanceLevel.GOOD_FIT: "Standard outreach sequence - monitor progress",
            ResonanceLevel.MODERATE_POTENTIAL: "Cautious approach - extended evaluation required",
            ResonanceLevel.LOW_RESONANCE: "Monitor only - defer active outreach",
            ResonanceLevel.MISALIGNED: "Decline partnership - fundamental misalignment"
        }
        return recommendations[self.classification]
    
    def to_dict(self) -> Dict:
        """
        Convert resonance score to dictionary for serialization
        
        Returns:
            dict: Complete resonance data
        """
        return {
            "partner_name": self.partner_name,
            "overall_score": round(self.overall_score, 2),
            "classification": self.classification.value,
            "recommendation": self.recommendation,
            "frequencies": {
                "truth_alignment": self.frequencies.truth_alignment,
                "cultural_fit": self.frequencies.cultural_fit,
                "strategic_synergy": self.frequencies.strategic_synergy,
                "resistance_factor": self.frequencies.resistance_factor
            }
        }
    
    def __str__(self) -> str:
        """String representation of resonance score"""
        name = f" for {self.partner_name}" if self.partner_name else ""
        return (f"ResonanceScore{name}: {self.overall_score:.2f}/10 "
                f"({self.classification.value})")


class ResonanceCalculator:
    """
    Star Dust Frequency resonance calculator
    
    Provides methods for calculating and analyzing partnership resonance
    using the NŪR Protocol.
    """
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """
        Initialize calculator with optional custom weights
        
        Args:
            weights: Optional custom weights for frequency components
                    Default: all components weighted equally (1.0)
        """
        self.weights = weights or {
            'truth_alignment': 1.0,
            'cultural_fit': 1.0,
            'strategic_synergy': 1.0
        }
    
    def calculate(self, 
                  truth_alignment: float,
                  cultural_fit: float,
                  strategic_synergy: float,
                  resistance_factor: float,
                  partner_name: Optional[str] = None) -> ResonanceScore:
        """
        Calculate resonance score from individual frequency components
        
        Args:
            truth_alignment: Score 0.0-1.0 for values alignment
            cultural_fit: Score 0.0-1.0 for cultural compatibility
            strategic_synergy: Score 0.0-1.0 for strategic value
            resistance_factor: Score 0.0-1.0 for barriers (lower better)
            partner_name: Optional partner name for tracking
            
        Returns:
            ResonanceScore: Complete resonance evaluation
        """
        frequencies = FrequencyComponents(
            truth_alignment=truth_alignment,
            cultural_fit=cultural_fit,
            strategic_synergy=strategic_synergy,
            resistance_factor=resistance_factor
        )
        
        return ResonanceScore(frequencies=frequencies, partner_name=partner_name)
    
    def calculate_from_dict(self, data: Dict, partner_name: Optional[str] = None) -> ResonanceScore:
        """
        Calculate resonance score from dictionary data
        
        Args:
            data: Dictionary containing frequency values
            partner_name: Optional partner name
            
        Returns:
            ResonanceScore: Complete resonance evaluation
        """
        return self.calculate(
            truth_alignment=data['truth_alignment'],
            cultural_fit=data['cultural_fit'],
            strategic_synergy=data['strategic_synergy'],
            resistance_factor=data['resistance_factor'],
            partner_name=partner_name
        )
    
    def batch_calculate(self, opportunities: list) -> list:
        """
        Calculate resonance scores for multiple opportunities
        
        Args:
            opportunities: List of dicts with partner data and frequencies
            
        Returns:
            list: List of ResonanceScore objects sorted by score (high to low)
        """
        scores = []
        for opp in opportunities:
            score = self.calculate_from_dict(
                data=opp.get('frequencies', opp),
                partner_name=opp.get('name', opp.get('partner_name'))
            )
            scores.append(score)
        
        # Sort by overall score descending
        return sorted(scores, key=lambda s: s.overall_score, reverse=True)
    
    def compare_opportunities(self, opp1: Dict, opp2: Dict) -> Dict:
        """
        Compare two partnership opportunities
        
        Args:
            opp1: First opportunity data
            opp2: Second opportunity data
            
        Returns:
            dict: Comparison analysis
        """
        score1 = self.calculate_from_dict(opp1, opp1.get('name', 'Opportunity 1'))
        score2 = self.calculate_from_dict(opp2, opp2.get('name', 'Opportunity 2'))
        
        return {
            'opportunity_1': score1.to_dict(),
            'opportunity_2': score2.to_dict(),
            'score_difference': abs(score1.overall_score - score2.overall_score),
            'higher_score': score1.partner_name if score1.overall_score > score2.overall_score else score2.partner_name,
            'recommendation': (
                f"Prioritize {score1.partner_name}" if score1.overall_score > score2.overall_score
                else f"Prioritize {score2.partner_name}"
            )
        }


def calculate_partnership_resonance(partner_data: Dict) -> ResonanceScore:
    """
    Convenience function for calculating resonance from partner data
    
    Args:
        partner_data: Dictionary containing frequency scores
        
    Returns:
        ResonanceScore: Complete resonance evaluation
    """
    calculator = ResonanceCalculator()
    return calculator.calculate_from_dict(
        data=partner_data,
        partner_name=partner_data.get('name', partner_data.get('partner_name'))
    )


def demo_resonance_calculation():
    """Demonstrate resonance calculation with example partners"""
    
    print("="*70)
    print("STAR DUST FREQUENCIES: RESONANCE CALCULATION DEMO")
    print("="*70)
    
    # Example partners
    partners = [
        {
            'name': 'Sony Corporation',
            'truth_alignment': 0.85,
            'cultural_fit': 0.90,
            'strategic_synergy': 0.88,
            'resistance_factor': 0.25
        },
        {
            'name': 'HYBE Corporation',
            'truth_alignment': 0.90,
            'cultural_fit': 0.92,
            'strategic_synergy': 0.91,
            'resistance_factor': 0.20
        },
        {
            'name': 'Digital Trust Centre Singapore',
            'truth_alignment': 0.95,
            'cultural_fit': 0.88,
            'strategic_synergy': 0.93,
            'resistance_factor': 0.18
        },
        {
            'name': 'Example Startup',
            'truth_alignment': 0.75,
            'cultural_fit': 0.70,
            'strategic_synergy': 0.65,
            'resistance_factor': 0.40
        }
    ]
    
    calculator = ResonanceCalculator()
    
    # Calculate and display scores
    print("\nINDIVIDUAL RESONANCE SCORES:")
    print("-" * 70)
    
    scores = calculator.batch_calculate(partners)
    for score in scores:
        print(f"\n{score.partner_name}")
        print(f"  Overall Score: {score.overall_score:.2f}/10")
        print(f"  Classification: {score.classification.value}")
        print(f"  Frequencies:")
        print(f"    - Truth Alignment: {score.frequencies.truth_alignment:.2f}")
        print(f"    - Cultural Fit: {score.frequencies.cultural_fit:.2f}")
        print(f"    - Strategic Synergy: {score.frequencies.strategic_synergy:.2f}")
        print(f"    - Resistance Factor: {score.frequencies.resistance_factor:.2f}")
        print(f"  Recommendation: {score.recommendation}")
    
    # Compare top two opportunities
    print("\n" + "="*70)
    print("COMPARISON: TOP TWO OPPORTUNITIES")
    print("="*70)
    
    comparison = calculator.compare_opportunities(partners[1], partners[0])
    print(f"\nHigher Score: {comparison['higher_score']}")
    print(f"Score Difference: {comparison['score_difference']:.2f}")
    print(f"Recommendation: {comparison['recommendation']}")
    
    # Summary statistics
    print("\n" + "="*70)
    print("SUMMARY STATISTICS")
    print("="*70)
    
    avg_score = sum(s.overall_score for s in scores) / len(scores)
    high_priority = sum(1 for s in scores if s.classification in [
        ResonanceLevel.PERFECT_RESONANCE, 
        ResonanceLevel.HIGH_PRIORITY
    ])
    
    print(f"\nTotal Opportunities: {len(scores)}")
    print(f"Average Resonance: {avg_score:.2f}/10")
    print(f"High Priority Count: {high_priority}")
    print(f"Perfect Resonance Count: {sum(1 for s in scores if s.classification == ResonanceLevel.PERFECT_RESONANCE)}")


if __name__ == "__main__":
    demo_resonance_calculation()
