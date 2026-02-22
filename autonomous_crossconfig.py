"""
Configuration management for Autonomous Cross system.
Centralizes all system parameters and environment settings.
"""
import os
from dataclasses import dataclass
from typing import Dict, Any
import logging

@dataclass
class IntersectionConfig:
    """Physical intersection configuration"""
    width: float = 20.0  # meters
    height: float = 20.0  # meters
    lane_width: float = 3.5  # meters
    max_speed: float = 15.0  # m/s (~35 mph)
    min_safe_distance: float = 2.0  # meters
    reaction_time: float = 0.5  # seconds
    decision_interval: float = 0.1  # seconds
    
@dataclass
class VehicleConfig:
    """Vehicle dynamics configuration"""
    max_acceleration: float = 3.0  # m/s²
    max_deceleration: float = -4.0  # m/s² (negative)
    length: float = 4.5  # meters
    width: float = 1.8  # meters
    sensor_range: float = 50.0  # meters
    
@dataclass
class SocialConfig:
    """Social interaction parameters"""
    courtesy_factor: float = 0.7  # 0-1, how courteous vehicles are
    predictability_weight: float = 0.8  # importance of predictable behavior
    efficiency_weight: float = 0.6  # importance of movement efficiency
    grace_weight: float = 0.4  # importance of graceful movements
    
@dataclass
class FirebaseConfig:
    """Firebase configuration"""
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "autonomous-cross-dev")
    credentials_path: str = os.getenv("FIREBASE_CREDENTIALS", "./service-account.json")
    collection_name: str = "intersection_states"
    
@dataclass
class SystemConfig:
    """Complete system configuration"""
    intersection: IntersectionConfig
    vehicle: VehicleConfig
    social: SocialConfig
    firebase: FirebaseConfig
    log_level: str = "INFO"
    simulation_mode: bool = True
    
    @classmethod
    def from_env(cls) -> 'SystemConfig':
        """Create configuration from environment variables"""
        return cls(
            intersection=IntersectionConfig(),
            vehicle=VehicleConfig(),
            social=SocialConfig(),
            firebase=FirebaseConfig(),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            simulation_mode=os.getenv("SIMULATION_MODE", "true").lower() == "true"
        )