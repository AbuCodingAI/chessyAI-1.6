# Deploy ChessyCom to Render.com

## 🚀 Complete Step-by-Step Guide

### Step 1: Prepare Your GitHub Repository

1. **Make sure you're in your project folder**
   ```bash
   cd path/to/chessycom
   ```

2. **Initialize Git (if not already done)**
   ```bash
   git init
   ```

3. **Add all files**
   ```bash
   git add .
   ```

4. **Commit**
   ```bash
   git commit -m "Initial commit: ChessyCom v1.4"
   ```

5. **Create GitHub repository**
   - Go to github.com
   - Click "New repository"
   - Name it: `chessycom`
   - Don't initialize with README (you already have files)
   - Click "Create repository"

6. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/chessycom.git
   git branch -M main
   git push -u origin main
   ```

---

### Step 2: Sign Up for Render

1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with:
   - GitHub account (recommended - easiest)
   - OR email

---

### Step 3: Deploy Your App

1. **Click "New +"** (top right)
2. **Select "Web Service"**
3. **Connect your GitHub repository:**
   - If first time: Click "Connect GitHub"
   - Authorize Render to access your repos
   - Find and select your `chessycom` repository

4. **Configure the service:**
   ```
   Name: chessycom (or whatever you want)
   Region: Oregon (US West) - or closest to you
   Branch: main
   Root Directory: (leave blank)
   Runtime: Node
   Build Command: npm install
   Start Command: node server.js
   ```

5. **Select Plan:**
   - Choose "Free" plan
   - Note: Free tier sleeps after 15 min of inactivity

6. **Advanced Settings (optional):**
   - Environment Variables: None needed for now
   - Auto-Deploy: Yes (recommended)

7. **Click "Create Web Service"**

---

### Step 4: Wait for Deployment

1. **Render will:**
   - Clone your repository
   - Run `npm install`
   - Start your server with `node server.js`
   - This takes 2-5 minutes

2. **Watch the logs:**
   - You'll see real-time deployment logs
   - Look for: "🏰 ChessyCom Server Started!"

3. **When complete:**
   - Status changes to "Live" (green)
   - You'll see your URL: `https://chessycom.onrender.com`

---

### Step 5: Test Your Deployment

1. **Click the URL** at the top of the page
2. **Your chess game should load!**
3. **Test features:**
   - ✅ Board loads
   - ✅ Can make moves
   - ✅ AI opponents work
   - ✅ Multiplayer rooms work

---

### Step 6: Custom Domain (Optional)

1. **In Render dashboard:**
   - Go to your service
   - Click "Settings"
   - Scroll to "Custom Domains"
   - Click "Add Custom Domain"

2. **Add your domain:**
   - Enter: `yourdomain.com`
   - Follow DNS instructions
   - Wait for SSL certificate (automatic)

---

## 🔧 Troubleshooting

### Deployment Failed
**Check logs for errors:**
- Click "Logs" tab
- Look for red error messages
- Common issues:
  - Missing dependencies in package.json
  - Syntax errors in code
  - Port configuration issues

### App Won't Start
**Check:**
1. `package.json` has correct start script
2. `server.js` uses `process.env.PORT`
3. All dependencies are in `package.json`

### AI Not Working
**Stockfish issue:**
- Stockfish won't work on Render (binary file)
- AI will fall back to JavaScript engine
- This is expected and OK

### App Sleeps (Free Tier)
**Free tier limitations:**
- Sleeps after 15 minutes of inactivity
- First visit takes ~30 seconds to wake up
- Upgrade to $7/month for always-on

---

## 🔄 Updating Your Deployment

### Automatic Updates (Recommended)
1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push
   ```
3. Render auto-deploys! (takes 2-3 minutes)

### Manual Deploy
1. Go to Render dashboard
2. Click "Manual Deploy"
3. Select "Deploy latest commit"

---

## 📊 Monitoring

### View Logs
- Click "Logs" tab
- See real-time server logs
- Useful for debugging

### Check Metrics
- Click "Metrics" tab
- See CPU, memory usage
- Monitor performance

---

## 💰 Pricing

### Free Tier (What You Get)
- ✅ 750 hours/month (enough for hobby projects)
- ✅ Custom domains
- ✅ Automatic HTTPS
- ✅ Auto-deploy from GitHub
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ 512 MB RAM
- ⚠️ Shared CPU

### Paid Tier ($7/month)
- ✅ Always on (no sleep)
- ✅ 512 MB RAM (upgradeable)
- ✅ Faster CPU
- ✅ Better for production

---

## 🎯 Your Live URLs

After deployment, you'll have:
- **Main URL:** `https://chessycom.onrender.com`
- **Custom domain:** `https://yourdomain.com` (if configured)

Share these with friends to play online! 🎮

---

## ✅ Success Checklist

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service created on Render
- [ ] Deployment successful (green "Live" status)
- [ ] Website loads at Render URL
- [ ] Chess game works
- [ ] AI opponents work
- [ ] Multiplayer works

---

## 🆘 Need Help?

1. **Check Render docs:** [render.com/docs](https://render.com/docs)
2. **Check logs** in Render dashboard
3. **Test locally first:** `node server.js`
4. **Check GitHub issues** in your repo

---

## 🎉 You're Live!

Your chess game is now online and accessible to anyone with the URL!

**Share it:**
- Send the URL to friends
- Post on social media
- Add to your portfolio

**Enjoy your live chess platform! ♟️🚀**
