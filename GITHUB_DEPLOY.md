# Instructions for Deploying to GitHub

## Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `consumers-system` (or your preferred name)
3. Description: "AI-powered consumer behavior simulation system"
4. Choose **Public** or **Private**
5. **DO NOT** check "Initialize this repository with a README" (we already have one)
6. Click **"Create repository"**

## Step 2: Connect Local Repository to GitHub

After creating the repository, GitHub will show you commands. Use these commands in your terminal:

```bash
# Replace YOUR_USERNAME and REPOSITORY_NAME with your actual values
git remote add origin https://github.com/YOUR_USERNAME/REPOSITORY_NAME.git
git branch -M main
git push -u origin main
```

### Alternative: Using SSH (if you have SSH keys configured)

```bash
git remote add origin git@github.com:YOUR_USERNAME/REPOSITORY_NAME.git
git branch -M main
git push -u origin main
```

## Step 3: Verify Deployment

After pushing, check your repository on GitHub to verify all files are uploaded correctly.

## Important Notes

✅ **What is included:**
- All Python source code
- README.md (English version)
- requirements.txt
- config_example.json
- .gitignore

❌ **What is excluded (protected by .gitignore):**
- `.env` files (environment variables with API keys)
- `config.json` (real configuration files)
- `__pycache__/` directories
- `venv/` or `.venv/` directories
- Log files and temporary data

## Next Steps After Deployment

1. **Add environment variables to GitHub Actions** (if using CI/CD):
   - Go to repository Settings → Secrets and variables → Actions
   - Add `DEEPSEEK_API_KEY` as a secret

2. **Update README** with the actual repository URL in the clone instructions

3. **Create a `.env.example`** file (optional but recommended):
   ```
   DEEPSEEK_API_KEY=your_api_key_here
   ```

## Troubleshooting

If you get authentication errors:
- Use GitHub CLI: `gh auth login`
- Or use SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh


