import { Canvas } from '@react-three/fiber'
import { Environment, Loader, OrbitControls, Stats, useProgress } from "@react-three/drei"
import Lamborghini from "./components/Models/Lamborghini Aventador J"
import Scene from "./components/Models/Autobianchi Stellina"
import Maserati from "./components/Models/Maserati MC20"
import { Suspense, useEffect, useMemo, useRef, useState } from 'react'
import { Model, ModelProps, models } from './components/Models/model'
import EditorPanel from './components/EditorPanel'

interface Cars {
  readonly Model: (props: ModelProps) => JSX.Element;
  readonly interior: string;
  readonly exterior: string;
}

export default function App() {
  const cars: Record<Model, Cars> = useMemo(() => ({
    "Lamborghini Aventador J": {
      Model: Lamborghini,
      interior: "#000000",
      exterior: "#9a9898",
    },
    "Maserati MC20": {
      Model: Maserati,
      interior: "#000000",
      exterior: "#ffffff"
    },
    "Autobianchi Stellina": {
      Model: Scene,
      interior: "#000000",
      exterior: "#963f3f"
    },
  }), []);

  const [carsState, setCarsState] = useState(() => cars);
  const [selectedModel, setSelectedModel] = useState<Model>("Lamborghini Aventador J");
  const [rotation, setRotation] = useState(false);
  const [stats, setStats] = useState(false);
  const [isEditorOpen, setIsEditorOpen] = useState(false);
  
  const carsStateRef = useRef(carsState);

  useEffect(() => {
    carsStateRef.current = carsState;
  }, [carsState]);

  const resetCarColor = () => {
    setCarsState({
      ...carsStateRef.current,
      [selectedModel]: {
        ...carsStateRef.current[selectedModel],
        exterior: cars[selectedModel].exterior,
        interior: cars[selectedModel].interior,
      }
    });
  };

  const setCarInterior = (interior: string) => {
    setCarsState({
      ...carsStateRef.current,
      [selectedModel]: {
        ...carsStateRef.current[selectedModel],
        interior
      }
    })
  };

  const setCarExterior = (exterior: string) => {
    setCarsState({
      ...carsStateRef.current,
      [selectedModel]: {
        ...carsStateRef.current[selectedModel],
        exterior
      }
    })
  };

  const handleModelChange = (model: Model) => {
    setSelectedModel(model);
  };

  const { progress } = useProgress();

  return (
    <div className="app-container">
      <EditorPanel
        selectedModel={selectedModel}
        onModelChange={handleModelChange}
        exteriorColor={carsState[selectedModel].exterior}
        onExteriorColorChange={setCarExterior}
        interiorColor={carsState[selectedModel].interior}
        onInteriorColorChange={setCarInterior}
        rotation={rotation}
        onRotationChange={setRotation}
        stats={stats}
        onStatsChange={setStats}
        onResetColors={resetCarColor}
        isOpen={isEditorOpen}
        onToggle={() => setIsEditorOpen(!isEditorOpen)}
      />
      
      <div className="canvas-container">
        <Canvas camera={{ position: [0, 0, 10] }} shadows={true} frameloop="demand">
          <Suspense fallback={null}>
            {models
              .map(name => {
                const Model = cars[name].Model;
                return <Model 
                  exterior={carsState[name].exterior} 
                  interior={carsState[name].interior} 
                  visible={selectedModel === name} 
                  key={name} 
                />
              })}
          </Suspense>
          <Environment
            background
            files={'venice_sunset_1k.hdr'}
            blur={0.5}
          />
          {stats ? <Stats /> : undefined}
          <OrbitControls 
            maxPolarAngle={7 * Math.PI / 18} 
            autoRotate={rotation} 
            minDistance={2} 
            maxDistance={15} 
          />
        </Canvas>
        <Loader />
      </div>
    </div>
  )
}