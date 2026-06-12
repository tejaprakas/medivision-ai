# MediVision AI - Deployment Configuration

## Frontend: Vercel (Next.js)

### Step 1: Push to GitHub
```bash
cd C:\Users\tejap\AppData\Local\hermes\projects\medivision-ai
git init
git add .
git commit -m "Initial commit - MediVision AI"
git remote add origin https://github.com/YOUR_USERNAME/medivision-ai.git
git push -u origin main
```

### Step 2: Deploy to Vercel
1. Go to https://vercel.com
2. Click "New Project"
3. Import your GitHub repo
4. Set framework preset to "Next.js"
5. Set root directory to `frontend`
6. Add environment variables:
   - `NEXT_PUBLIC_API_URL` = your backend URL
7. Click Deploy

### Build Settings:
- Framework: Next.js
- Root Directory: frontend
- Build Command: `npm run build`
- Output Directory: .next

---

## Backend: Render (FastAPI)

### Step 1: Create render.yaml
Already created at `backend/render.yaml`

### Step 2: Deploy
1. Go to https://render.com
2. Click "New Web Service"
3. Connect your GitHub repo
4. Set root directory to `backend`
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables (see below)
8. Click Deploy

### Backend Environment Variables:
```
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/medivision
REDIS_URL=redis://redis:6379
SECRET_KEY=your-super-secret-key-change-this
CORS_ORIGINS=["https://your-frontend.vercel.app"]
ACCESS_TOKEN_EXPIRE_MINUTES=480
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM=HS256
```

---

## Database: MongoDB Atlas (Free)

1. Go to https://mongodb.com/atlas
2. Create free cluster
3. Create database user
4. Whitelist IP: 0.0.0.0/0 (allow all)
5. Copy connection string
6. Add to backend env vars as MONGODB_URL

---

## Alternative: Docker Deployment

```bash
# Build and run everything locally
docker-compose up --build

# Deploy to AWS/GCP/Heroku
docker build -t medivision-backend ./backend
docker build -t medivision-frontend ./frontend
```

---

## Free Deployment Options Summary:

| Service | Component | Cost |
|---------|-----------|------|
| Vercel | Frontend (Next.js) | Free |
| Render | Backend (FastAPI) | Free tier |
| MongoDB Atlas | Database | Free 512MB |
| Redis | Cache | Free (Upstash) |
| Cloudinary | Image Storage | Free 25GB |

---

## Post-Deployment Checklist:

- [ ] Update CORS_ORIGINS with frontend URL
- [ ] Update NEXT_PUBLIC_API_URL with backend URL
- [ ] Change SECRET_KEY to a secure random string
- [ ] Set up MongoDB Atlas
- [ ] Set up Redis (Upstash free tier)
- [ ] Test auth flow
- [ ] Test image upload
- [ ] Test chatbot
