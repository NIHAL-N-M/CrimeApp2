# AutoCraft - Deployment Guide

## 🚀 Deploy to Vercel

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Go to Vercel Dashboard**:
   - Visit [vercel.com](https://vercel.com)
   - Sign in with your GitHub account
   - Click "New Project"

3. **Import Repository**:
   - Select your AutoCraft repository
   - Vercel will auto-detect it's a Vite project
   - Click "Deploy"

4. **Configuration** (if needed):
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   cd prototype
   vercel
   ```

4. **Follow the prompts**:
   - Link to existing project or create new
   - Confirm settings
   - Deploy!

### Option 3: One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/3D-Car-Viewer-master&project-name=autocraft&repository-name=autocraft)

## 🔧 Build Process

The deployment will:
1. Install dependencies (`npm install`)
2. Build the project (`npm run build`)
3. Serve the `dist` folder
4. Handle routing for the AR page

## 📁 File Structure After Deployment

```
/
├── index.html          # Main AutoCraft application
├── ar.html            # AR experience page
├── assets/            # Built JavaScript and CSS
└── [other assets]     # 3D models and textures
```

## 🌐 Custom Domain (Optional)

1. **Add Domain in Vercel Dashboard**:
   - Go to your project settings
   - Click "Domains"
   - Add your custom domain

2. **Configure DNS**:
   - Follow Vercel's DNS instructions
   - Point your domain to Vercel's servers

## 🔄 Automatic Deployments

- **GitHub Integration**: Every push to main branch triggers deployment
- **Preview Deployments**: Pull requests get preview URLs
- **Rollback**: Easy rollback to previous versions

## 📱 Features After Deployment

✅ **3D Car Viewer** with AutoCraft editor panel  
✅ **Mobile responsive design**  
✅ **AR page** with QR code and direct link  
✅ **Color customization** for all car models  
✅ **Real-time 3D rendering**  

## 🛠️ Troubleshooting

### Build Errors
- Check Node.js version (16+ required)
- Ensure all dependencies are in `package.json`
- Verify Vite configuration

### Routing Issues
- The `vercel.json` handles SPA routing
- AR page should be accessible at `/ar.html`

### Performance
- 3D models are optimized for web
- Images are compressed
- CDN delivery via Vercel's edge network

## 📊 Analytics (Optional)

Add Vercel Analytics:
```bash
npm install @vercel/analytics
```

Then add to your main component:
```jsx
import { Analytics } from '@vercel/analytics/react';

function App() {
  return (
    <>
      {/* Your app content */}
      <Analytics />
    </>
  );
}
```

---

**Your AutoCraft application is now ready for production deployment! 🎉**
