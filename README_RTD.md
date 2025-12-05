# Read the Docs Setup Guide

This guide explains how to set up Read the Docs for BRAID-DSPy.

## Quick Setup

1. **Create a Read the Docs account**
   - Go to https://readthedocs.org/
   - Sign up or log in with GitHub

2. **Import your repository**
   - Click "Import a Project"
   - Select your GitHub repository
   - Read the Docs will detect `.readthedocs.yaml` automatically

3. **Configure project settings**
   - Project name: `braid-dspy` (or your preferred name)
   - Repository URL: Your GitHub repository URL
   - Default branch: `main` (or `master`)

4. **Build settings** (usually auto-detected)
   - Configuration file: `.readthedocs.yaml`
   - Python version: 3.11
   - Install project: Yes
   - Extra requirements: `docs`

5. **Trigger a build**
   - Click "Build version" to test
   - Documentation will be available at: `https://braid-dspy.readthedocs.io/en/stable/`

## Configuration Files

The project includes:
- `.readthedocs.yaml` - Read the Docs configuration
- `docs/conf.py` - Sphinx configuration
- `docs/index.md` - Main documentation page

## Local Testing

Before pushing to Read the Docs, test locally:

```bash
# Install dependencies
pip install -e ".[docs]"

# Build documentation
cd docs
make html

# View locally
open _build/html/index.html
```

## Troubleshooting

### Build fails with import errors
- Ensure all dependencies are in `pyproject.toml` under `[project.optional-dependencies.docs]`
- Check that `dspy-ai` is installable (may need not be imported during build)

### Documentation not updating
- Check that `.readthedocs.yaml` is in the repository root
- Verify the configuration file path in Read the Docs settings
- Trigger a manual build

### Theme not loading
- Ensure `sphinx-rtd-theme` is in the docs requirements
- Check `html_theme = 'sphinx_rtd_theme'` in `conf.py`

## Custom Domain (Optional)

To use a custom domain:
1. Go to Project Settings > Domains
2. Add your custom domain
3. Follow DNS configuration instructions

## Version Management

Read the Docs automatically builds:
- Latest version (default branch)
- All Git tags
- All branches (if enabled)

To manage versions:
- Go to Project Settings > Versions
- Set default version
- Hide/show specific versions

