import React from 'react';
import { Model, models } from './Models/model';

interface EditorPanelProps {
  selectedModel: Model;
  onModelChange: (model: Model) => void;
  exteriorColor: string;
  onExteriorColorChange: (color: string) => void;
  interiorColor: string;
  onInteriorColorChange: (color: string) => void;
  rotation: boolean;
  onRotationChange: (rotation: boolean) => void;
  stats: boolean;
  onStatsChange: (stats: boolean) => void;
  onResetColors: () => void;
  isOpen: boolean;
  onToggle: () => void;
}

const EditorPanel: React.FC<EditorPanelProps> = ({
  selectedModel,
  onModelChange,
  exteriorColor,
  onExteriorColorChange,
  interiorColor,
  onInteriorColorChange,
  rotation,
  onRotationChange,
  stats,
  onStatsChange,
  onResetColors,
  isOpen,
  onToggle
}) => {
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="editor-overlay"
          onClick={onToggle}
        />
      )}
      
      {/* Editor Panel */}
      <div className={`editor-panel ${isOpen ? 'open' : ''}`}>
        <div className="editor-header">
          <h2>AutoCraft</h2>
          <button className="close-btn" onClick={onToggle}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <div className="editor-content">
          {/* Model Selection */}
          <div className="control-group">
            <label className="control-label">Select Car Model</label>
            <select 
              value={selectedModel} 
              onChange={(e) => onModelChange(e.target.value as Model)}
              className="model-select"
            >
              {models.map(model => (
                <option key={model} value={model}>{model}</option>
              ))}
            </select>
          </div>

          {/* Exterior Color */}
          <div className="control-group">
            <label className="control-label">Exterior Color</label>
            <div className="color-input-group">
              <input
                type="color"
                value={exteriorColor}
                onChange={(e) => onExteriorColorChange(e.target.value)}
                className="color-input"
              />
              <input
                type="text"
                value={exteriorColor}
                onChange={(e) => onExteriorColorChange(e.target.value)}
                className="color-text-input"
                placeholder="#000000"
              />
            </div>
          </div>

          {/* Interior Color */}
          <div className="control-group">
            <label className="control-label">Interior Color</label>
            <div className="color-input-group">
              <input
                type="color"
                value={interiorColor}
                onChange={(e) => onInteriorColorChange(e.target.value)}
                className="color-input"
              />
              <input
                type="text"
                value={interiorColor}
                onChange={(e) => onInteriorColorChange(e.target.value)}
                className="color-text-input"
                placeholder="#000000"
              />
            </div>
          </div>

          {/* Preset Colors */}
          <div className="control-group">
            <label className="control-label">Quick Colors</label>
            <div className="preset-colors">
              {['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff', '#ffffff', '#000000', '#ffa500', '#800080'].map(color => (
                <button
                  key={color}
                  className="preset-color-btn"
                  style={{ backgroundColor: color }}
                  onClick={() => onExteriorColorChange(color)}
                  title={color}
                />
              ))}
            </div>
          </div>

          {/* Controls */}
          <div className="control-group">
            <label className="control-label">View Controls</label>
            <div className="toggle-group">
              <label className="toggle-label">
                <input
                  type="checkbox"
                  checked={rotation}
                  onChange={(e) => onRotationChange(e.target.checked)}
                  className="toggle-input"
                />
                <span className="toggle-slider"></span>
                Auto Rotate
              </label>
            </div>
            <div className="toggle-group">
              <label className="toggle-label">
                <input
                  type="checkbox"
                  checked={stats}
                  onChange={(e) => onStatsChange(e.target.checked)}
                  className="toggle-input"
                />
                <span className="toggle-slider"></span>
                Show Stats
              </label>
            </div>
          </div>

          {/* Reset Button */}
          <div className="control-group">
            <button 
              onClick={onResetColors}
              className="reset-btn"
            >
              Reset Colors
            </button>
          </div>

          {/* AR Button */}
          <div className="control-group">
            <button 
              onClick={() => window.location.href = 'ar.html'}
              className="ar-btn"
            >
              AR
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Toggle Button */}
      <button className="mobile-toggle-btn" onClick={onToggle}>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>
    </>
  );
};

export default EditorPanel;


