# 3D Car Viewer - Enhanced Edition

A modern, responsive 3D car customization viewer built with React, Three.js, and TypeScript.

## ✨ Features

### 🎨 Customization Panel
- **Left Editor Panel**: Dedicated sidebar for all customization controls
- **Car Model Selection**: Switch between different car models
- **Color Customization**: 
  - Exterior color picker with hex input
  - Interior color picker with hex input
  - Quick preset color buttons
- **View Controls**:
  - Auto-rotation toggle
  - Performance stats toggle
- **Reset Functionality**: Reset colors to default values

### 📱 Mobile Responsive Design
- **Responsive Layout**: Adapts to different screen sizes
- **Mobile-First Approach**: Optimized for touch devices
- **Slide-out Panel**: Editor panel slides in from the left on mobile
- **Touch-Friendly Controls**: Larger buttons and inputs for mobile use

### 🎯 User Experience
- **Modern UI**: Dark theme with glassmorphism effects
- **Smooth Animations**: Fluid transitions and hover effects
- **Intuitive Controls**: Easy-to-use interface for all features
- **Real-time Updates**: Instant visual feedback for all changes

## 🚀 Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd 3D-Car-Viewer-master/prototype
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Open your browser and navigate to `http://localhost:5173`

## 🎮 How to Use

### Desktop
- The editor panel is visible on the left side of the screen
- Use the dropdown to select different car models
- Click the color pickers to change exterior and interior colors
- Use the preset color buttons for quick color changes
- Toggle auto-rotation and stats display as needed
- Click "Reset Colors" to restore default colors

### Mobile
- Tap the hamburger menu button in the top-left corner
- The editor panel will slide in from the left
- Use the same controls as desktop
- Tap outside the panel or the close button to hide it

## 🛠️ Technical Stack

- **React 18**: Modern React with hooks
- **TypeScript**: Type-safe development
- **Three.js**: 3D graphics and rendering
- **React Three Fiber**: React renderer for Three.js
- **React Three Drei**: Useful helpers for React Three Fiber
- **Vite**: Fast build tool and dev server

## 📁 Project Structure

```
src/
├── components/
│   ├── EditorPanel.tsx      # Main editor panel component
│   └── Models/              # 3D model components
│       ├── model.ts         # Model types and constants
│       ├── Lamborghini Aventador J.tsx
│       ├── Maserati MC20.tsx
│       └── Autobianchi Stellina.tsx
├── App.tsx                  # Main application component
├── index.tsx               # Application entry point
└── styles.css              # Global styles and responsive design
```

## 🎨 Customization

### Adding New Car Models
1. Create a new model component in `src/components/Models/`
2. Import and add the model to the `cars` object in `App.tsx`
3. Add the model name to the `models` array in `model.ts`

### Styling
The application uses CSS custom properties and modern CSS features:
- Glassmorphism effects with `backdrop-filter`
- CSS Grid and Flexbox for responsive layouts
- Custom scrollbars and animations
- Mobile-first responsive design

## 🔧 Available Scripts

- `npm start`: Start development server
- `npm run build`: Build for production
- `npm run lint`: Run ESLint
- `npm run serve`: Preview production build

## 🚀 Deployment

### Deploy to Vercel

1. **Install Vercel CLI** (optional):
```bash
npm i -g vercel
```

2. **Deploy using Vercel Dashboard**:
   - Push your code to GitHub
   - Go to [vercel.com](https://vercel.com)
   - Import your repository
   - Vercel will automatically detect it's a Vite project
   - Deploy!

3. **Deploy using Vercel CLI**:
```bash
vercel
```

4. **Environment Variables** (if needed):
   - Add any environment variables in Vercel dashboard
   - No special configuration needed for this project

### Deploy to Other Platforms

- **Netlify**: Works with `npm run build` and `dist` folder
- **GitHub Pages**: Requires base path configuration in `vite.config.js`
- **AWS S3 + CloudFront**: Upload `dist` folder contents

## 📱 Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Note**: This is an enhanced version of the original 3D Car Viewer with improved UI/UX, mobile responsiveness, and a dedicated editor panel for better user experience.
