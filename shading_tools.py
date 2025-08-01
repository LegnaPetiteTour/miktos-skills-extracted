"""
Miktos Skill Library: Shading and Materials
===========================================

This module contains skills for creating, managing, and applying materials and shaders
in 3D software. Supports both procedural and image-based material workflows.
"""

from typing import Dict, List, Tuple, Union, Optional
import time


def create_pbr_material(
    material_name: str,
    base_color: Tuple[float, float, float] = (0.8, 0.8, 0.8),
    metallic: float = 0.0,
    roughness: float = 0.5,
    normal_strength: float = 1.0,
    emission_color: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    emission_strength: float = 0.0
) -> Dict[str, Union[str, Dict, float]]:
    """
    Creates a physically-based rendering (PBR) material with standard properties.

    Args:
        material_name (str): Name for the new material
        base_color (Tuple[float, float, float]): RGB values (0-1) for base color
        metallic (float): Metallic value (0-1), 0=dielectric, 1=metallic
        roughness (float): Surface roughness (0-1), 0=mirror, 1=completely rough
        normal_strength (float): Normal map intensity (0-2)
        emission_color (Tuple[float, float, float]): RGB emission color
        emission_strength (float): Emission intensity

    Returns:
        Dict: Material creation result with properties

    Example:
        >>> result = create_pbr_material('Steel', metallic=0.9, roughness=0.3)
        >>> print(result['data']['material_type'])
        'PBR'
    """
    start_time = time.time()
    
    # Validate color values
    for color in [base_color, emission_color]:
        if not all(0.0 <= c <= 1.0 for c in color):
            return {
                'status': 'error',
                'message': 'Color values must be between 0.0 and 1.0',
                'data': {},
                'execution_time': time.time() - start_time
            }
    
    # Validate numeric ranges
    if not (0.0 <= metallic <= 1.0):
        return {
            'status': 'error',
            'message': 'Metallic value must be between 0.0 and 1.0',
            'data': {},
            'execution_time': time.time() - start_time
        }
    
    if not (0.0 <= roughness <= 1.0):
        return {
            'status': 'error',
            'message': 'Roughness value must be between 0.0 and 1.0',
            'data': {},
            'execution_time': time.time() - start_time
        }
    
    # Determine material characteristics
    material_type = 'Metallic' if metallic > 0.7 else 'Dielectric'
    surface_type = 'Glossy' if roughness < 0.3 else 'Rough' if roughness > 0.7 else 'Satin'
    
    return {
        'status': 'success',
        'message': f'PBR material "{material_name}" created successfully',
        'data': {
            'material_name': material_name,
            'material_type': 'PBR',
            'surface_classification': f'{material_type} {surface_type}',
            'properties': {
                'base_color': base_color,
                'metallic': metallic,
                'roughness': roughness,
                'normal_strength': normal_strength,
                'emission_color': emission_color,
                'emission_strength': emission_strength
            },
            'render_engine_compatibility': ['Cycles', 'Eevee', 'Arnold', 'V-Ray']
        },
        'execution_time': time.time() - start_time
    }


def apply_material_to_object(
    object_name: str,
    material_name: str,
    material_slot: int = 0
) -> Dict[str, Union[str, Dict, float]]:
    """
    Applies an existing material to a 3D object.

    Args:
        object_name (str): Name of the target object
        material_name (str): Name of the material to apply
        material_slot (int): Material slot index (0-based)

    Returns:
        Dict: Material application result

    Example:
        >>> result = apply_material_to_object('Cube.001', 'Steel')
        >>> print(result['status'])
        'success'
    """
    start_time = time.time()
    
    if material_slot < 0:
        return {
            'status': 'error',
            'message': 'Material slot must be 0 or greater',
            'data': {},
            'execution_time': time.time() - start_time
        }
    
    return {
        'status': 'success',
        'message': f'Material "{material_name}" applied to "{object_name}"',
        'data': {
            'object_name': object_name,
            'material_name': material_name,
            'material_slot': material_slot,
            'application_method': 'direct_assignment'
        },
        'execution_time': time.time() - start_time
    }


def create_procedural_texture(
    texture_name: str,
    texture_type: str = 'noise',
    scale: float = 1.0,
    detail: float = 2.0,
    distortion: float = 0.0,
    color_ramp: Optional[List[Tuple[float, Tuple[float, float, float]]]] = None
) -> Dict[str, Union[str, Dict, float]]:
    """
    Creates a procedural texture node for material use.

    Args:
        texture_name (str): Name for the texture
        texture_type (str): Type of procedural texture ('noise', 'voronoi', 'wave', 'magic')
        scale (float): Texture scale/frequency
        detail (float): Level of detail/octaves
        distortion (float): Distortion amount
        color_ramp (Optional[List]): Color ramp stops as (position, (r,g,b)) tuples

    Returns:
        Dict: Texture creation result

    Example:
        >>> ramp = [(0.0, (0.0, 0.0, 0.0)), (1.0, (1.0, 1.0, 1.0))]
        >>> result = create_procedural_texture('RustNoise', 'noise', scale=5.0, color_ramp=ramp)
    """
    start_time = time.time()
    
    valid_types = ['noise', 'voronoi', 'wave', 'magic', 'brick', 'checker']
    if texture_type.lower() not in valid_types:
        return {
            'status': 'error',
            'message': f'Invalid texture type "{texture_type}". Valid options: {valid_types}',
            'data': {},
            'execution_time': time.time() - start_time
        }
    
    # Set default color ramp if none provided
    if color_ramp is None:
        color_ramp = [(0.0, (0.0, 0.0, 0.0)), (1.0, (1.0, 1.0, 1.0))]
    
    return {
        'status': 'success',
        'message': f'Procedural texture "{texture_name}" created',
        'data': {
            'texture_name': texture_name,
            'texture_type': texture_type,
            'properties': {
                'scale': scale,
                'detail': detail,
                'distortion': distortion,
                'color_ramp_stops': len(color_ramp)
            },
            'node_type': 'procedural',
            'output_type': 'color_and_factor'
        },
        'execution_time': time.time() - start_time
    }