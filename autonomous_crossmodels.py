"""
Data models for intersection entities with proper type hints and validation.
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple
from enum import Enum
import uuid
from datetime import datetime

class AgentType(Enum):
    """Type of agent in the intersection"""
    VEHICLE = "vehicle"
    PEDESTRIAN = "pedestrian"
    CYCLIST = "cyclist"
    EMERGENCY = "emergency"
    
class Intent(Enum):
    """Agent movement intent"""
    STRAIGHT = "straight"
    LEFT_TURN = "left_turn"
    RIGHT_TURN = "right_turn"
    U_TURN = "u_turn"
    STOP = "stop"
    
class LaneDirection(Enum):
    """Lane direction enumeration"""
    NORTHBOUND = "northbound"
    SOUTHBOUND = "southbound"
    EASTBOUND = "eastbound"
    WESTBOUND = "westbound"
    
@dataclass
class Position:
    """2D position with velocity and acceleration"""
    x: float  # meters from intersection center
    y: float  # meters from intersection center
    velocity: float = 0.0  # m/s
    acceleration: float = 0.0  # m/s²
    heading: float = 0.0  # radians, 0 = east
    
@dataclass
class VehicleProfile:
    """Vehicle characteristics affecting behavior"""
    length: float
    width: float
    max_acceleration: float
    max_deceleration: float
    reaction_time: float
    sensor_range: float
    
@dataclass
class Agent:
    """Base agent class with common properties"""
    agent_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    agent_type: AgentType = AgentType.VEHICLE
    position: Position = field(default_factory=lambda: Position(0, 0))
    intent: Intent = Intent.STRAIGHT
    lane: LaneDirection = LaneDirection.EASTBOUND
    timestamp: datetime = field(default_factory=datetime.utcnow)
    confidence: float = 0.95  # confidence in intent prediction
    profile: Optional[VehicleProfile] = None
    
    def distance_to(self, other: 'Agent') -> float:
        """Calculate Euclidean distance to another agent"""
        dx = self.position.x - other.position.x
        dy = self.position.y - other.position.y
        return (dx**2 + dy**2) ** 0.5
    
    def time_to_collision(self, other: 'Agent', relative_velocity: float) -> Optional[float]:
        """Calculate time to collision with another agent"""
        if relative_velocity <= 0:
            return None  # moving apart or stationary
        distance = self.distance_to(other)
        if distance <= 0:
            return 0.0
        return distance / abs(relative_velocity)

@dataclass
class IntersectionState:
    """Complete state of the intersection at a moment in time"""
    intersection_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    agents: List[Agent] = field(default_factory=list)
    traffic_light_state: Dict[LaneDirection, str] = field(default_factory=dict)
    weather_conditions: str = "clear"
    visibility: float = 100.0  # meters
    system_load: float = 0.0  # 0-1 scale
    
    def get_agents_in_zone(self, zone_bounds: Tuple[float, float, float, float]) -> List[Agent]:
        """Get agents within specified zone bounds