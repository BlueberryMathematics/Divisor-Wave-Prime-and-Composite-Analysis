'use client';

import { useRef, useMemo, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Text, Grid, PerspectiveCamera } from '@react-three/drei';
import * as THREE from 'three';

function Surface3D({ data, colormap = 'viridis', animate = false }) {
  const meshRef = useRef(null);
  const [time, setTime] = useState(0);

  useFrame((state, delta) => {
    if (animate) {
      setTime(time + delta * 0.5);
      if (meshRef.current) {
        meshRef.current.rotation.z = Math.sin(time) * 0.1;
      }
    }
  });

  const { geometry, material } = useMemo(() => {
    const { x_values, y_values, z_values, metadata } = data;
    const width = x_values.length;
    const height = y_values.length;

    // Create geometry
    const geometry = new THREE.PlaneGeometry(
      Math.abs(metadata.x_range[1] - metadata.x_range[0]),
      Math.abs(metadata.y_range[1] - metadata.y_range[0]),
      width - 1,
      height - 1
    );

    // Set vertex positions and colors
    const positions = geometry.attributes.position.array;
    const colors = new Float32Array(positions.length);
    
    const { z_min, z_max } = metadata.statistics;
    const zRange = z_max - z_min || 1;

    for (let i = 0; i < height; i++) {
      for (let j = 0; j < width; j++) {
        const index = i * width + j;
        const vertexIndex = index * 3;
        
        // Set Z position (height)
        const zValue = z_values[i] ? z_values[i][j] || 0 : 0;
        positions[vertexIndex + 2] = (zValue - z_min) / zRange * 5; // Scale height
        
        // Set color based on height
        const normalizedZ = (zValue - z_min) / zRange;
        const color = getColorFromValue(normalizedZ, colormap);
        colors[vertexIndex] = color.r;
        colors[vertexIndex + 1] = color.g;
        colors[vertexIndex + 2] = color.b;
      }
    }

    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.computeVertexNormals();

    // Create material
    const material = new THREE.MeshPhongMaterial({
      vertexColors: true,
      wireframe: false,
      shininess: 100,
      transparent: true,
      opacity: 0.9,
    });

    return { geometry, material };
  }, [data, colormap]);

  return (
    <mesh ref={meshRef} geometry={geometry} material={material} />
  );
}

function getColorFromValue(value, colormap) {
  // Clamp value between 0 and 1
  const t = Math.max(0, Math.min(1, value));
  
  switch (colormap) {
    case 'viridis':
      return new THREE.Color().setHSL(0.8 - t * 0.8, 0.8, 0.3 + t * 0.4);
    case 'plasma':
      return new THREE.Color().setHSL(0.9 - t * 0.9, 0.9, 0.2 + t * 0.6);
    case 'inferno':
      return new THREE.Color().setHSL(0.0 + t * 0.15, 0.9, 0.1 + t * 0.7);
    case 'cool':
      return new THREE.Color().setHSL(0.6 + t * 0.3, 0.7, 0.3 + t * 0.4);
    case 'hot':
      if (t < 0.33) {
        return new THREE.Color(3 * t, 0, 0);
      } else if (t < 0.66) {
        return new THREE.Color(1, 3 * (t - 0.33), 0);
      } else {
        return new THREE.Color(1, 1, 3 * (t - 0.66));
      }
    default:
      return new THREE.Color().setHSL(0.7 - t * 0.7, 0.8, 0.3 + t * 0.4);
  }
}

function Axes({ range = 10 }) {
  return (
    <group>
      {/* X Axis */}
      <line>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            array={new Float32Array([-range, 0, 0, range, 0, 0])}
            count={2}
            itemSize={3}
          />
        </bufferGeometry>
        <lineBasicMaterial color="red" />
      </line>
      
      {/* Y Axis */}
      <line>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            array={new Float32Array([0, -range, 0, 0, range, 0])}
            count={2}
            itemSize={3}
          />
        </bufferGeometry>
        <lineBasicMaterial color="green" />
      </line>
      
      {/* Z Axis */}
      <line>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            array={new Float32Array([0, 0, -range, 0, 0, range])}
            count={2}
            itemSize={3}
          />
        </bufferGeometry>
        <lineBasicMaterial color="blue" />
      </line>
      
      {/* Axis Labels */}
      <Text position={[range + 1, 0, 0]} fontSize={0.5} color="red">
        Re(z)
      </Text>
      <Text position={[0, range + 1, 0]} fontSize={0.5} color="green">
        Im(z)
      </Text>
      <Text position={[0, 0, range + 1]} fontSize={0.5} color="blue">
        |f(z)|
      </Text>
    </group>
  );
}

export default function Plot3D({ 
  data, 
  colormap = 'viridis', 
  animate = false, 
  showAxes = true,
  lightingIntensity = 0.8 
}) {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading time for geometry processing
    const timer = setTimeout(() => setIsLoading(false), 500);
    return () => clearTimeout(timer);
  }, [data]);

  if (isLoading) {
    return (
      <div className="aspect-video bg-gray-900/50 rounded-lg border border-white/10 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-400 mx-auto mb-2"></div>
          <p className="text-sm text-gray-400">Generating 3D surface...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="aspect-video bg-black rounded-lg overflow-hidden border border-white/10 relative">
      <Canvas>
        <PerspectiveCamera makeDefault position={[15, 15, 15]} />
        
        {/* Lighting */}
        <ambientLight intensity={0.3} />
        <directionalLight 
          position={[10, 10, 5]} 
          intensity={lightingIntensity} 
          castShadow
        />
        <pointLight position={[-10, -10, -5]} intensity={0.5} color="#4f46e5" />
        
        {/* 3D Surface */}
        <Surface3D data={data} colormap={colormap} animate={animate} />
        
        {/* Axes */}
        {showAxes && <Axes range={15} />}
        
        {/* Grid */}
        <Grid 
          args={[20, 20]} 
          cellSize={1} 
          cellThickness={0.5} 
          cellColor="#4a5568" 
          sectionSize={5} 
          sectionThickness={1} 
          sectionColor="#6b7280" 
          fadeDistance={25} 
          fadeStrength={1} 
        />
        
        {/* Controls */}
        <OrbitControls 
          enablePan={true} 
          enableZoom={true} 
          enableRotate={true}
          minDistance={5}
          maxDistance={50}
          autoRotate={animate}
          autoRotateSpeed={0.5}
        />
      </Canvas>
      
      {/* Function Info Overlay */}
      <div className="absolute top-4 left-4 bg-black/70 backdrop-blur-sm rounded-lg p-3 text-white text-sm">
        <div className="font-semibold">{data.metadata.function_name}</div>
        <div className="text-gray-300 text-xs mt-1">
          Resolution: {data.metadata.resolution}×{data.metadata.resolution}
        </div>
        <div className="text-gray-300 text-xs">
          Range: [{data.metadata.statistics.z_min.toFixed(3)}, {data.metadata.statistics.z_max.toFixed(3)}]
        </div>
      </div>
    </div>
  );
}