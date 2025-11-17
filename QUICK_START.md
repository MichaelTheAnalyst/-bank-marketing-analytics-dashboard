# 🚀 Quick Start Guide - Bank Marketing Dashboard

## Automated Launch Options

### Option 1: Double-Click Batch File (Easiest) 🖱️

**For first-time setup:**
1. Double-click `setup_and_run.bat`
   - This will install all required packages
   - Then automatically launch the dashboard

**For regular use:**
1. Double-click `run_dashboard.bat`
   - Dashboard opens automatically
   - Browser window will launch at http://localhost:8501

### Option 2: PowerShell Script

1. Right-click `run_dashboard.ps1`
2. Select "Run with PowerShell"

### Option 3: Command Line

Open Command Prompt or PowerShell in this folder and run:

```bash
streamlit run dashboard.py
```

## 📋 What Happens When You Launch

1. ✅ Dashboard starts on http://localhost:8501
2. ✅ Browser opens automatically
3. ✅ Data loads from the CSV file
4. ✅ All analyses become available

## 🎯 Navigation

Once the dashboard opens:

1. **Use the sidebar** to navigate between sections:
   - 📈 Overview - Dataset statistics
   - ⭐ Feature Importance - Key drivers
   - 🤖 Predictive Models - ML algorithms
   - 👥 Customer Segmentation - Customer personas
   - 📞 Contact Optimization - Best practices
   - 💰 Economic Impact - Macro factors

2. **Interact with charts**:
   - Hover for details
   - Click legends to show/hide
   - Zoom and pan where available
   - Download charts (camera icon)

3. **Adjust parameters**:
   - Change number of segments in clustering
   - Select different models for comparison
   - All updates happen in real-time

## 🛑 Stopping the Dashboard

- In the command window: Press `Ctrl + C`
- Or simply close the command window
- Browser tab will stop updating

## ⚙️ Configuration

### Change Data File Path

Edit `dashboard.py` line 97:

```python
default_path = r"YOUR\PATH\TO\DATA\FILE.csv"
```

Or use the file uploader in the sidebar!

## 🔧 Troubleshooting

### Dashboard won't start?

1. **Check Python installation:**
   ```bash
   python --version
   ```
   Need Python 3.8 or higher

2. **Install packages manually:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Check if port 8501 is busy:**
   ```bash
   streamlit run dashboard.py --server.port 8502
   ```

### Data not loading?

1. Check file path in the dashboard
2. Ensure CSV uses semicolon (`;`) delimiter
3. Verify all required columns are present

### Slow performance?

- First run takes longer (model training)
- Subsequent navigation is cached and fast
- Close other applications if needed

## 📊 Expected Analysis Time

| Section | First Load | Subsequent |
|---------|-----------|------------|
| Overview | <1 sec | <1 sec |
| Feature Importance | 10-20 sec | Instant |
| Predictive Models | 30-60 sec | Instant |
| Segmentation | 5-10 sec | Instant |
| Contact Optimization | <5 sec | Instant |
| Economic Impact | <5 sec | Instant |

## 💡 Tips

1. **Start with Overview** to understand the data
2. **Feature Importance** shows what matters most
3. **Predictive Models** takes longest - be patient!
4. **Use tabs** within each section for different views
5. **Read insights** - they provide actionable recommendations

## 🎨 Browser Compatibility

Works best with:
- ✅ Google Chrome
- ✅ Microsoft Edge
- ✅ Firefox
- ✅ Safari

## 📱 Mobile Access

While the dashboard works on mobile, it's optimized for desktop/tablet viewing for the best experience.

## 🔄 Updating

To update the dashboard:
1. Edit the Python files
2. Save changes
3. Streamlit will auto-reload (or click "Rerun" in browser)

## ❓ Need Help?

- Check the main `README.md` for detailed documentation
- Review error messages in the command window
- Ensure all dependencies are installed
- Verify data file format matches requirements

---

## 🎯 Ready to Analyze?

Just double-click `run_dashboard.bat` and start exploring! 🚀

**Happy Analyzing!** 📊

