/**
 * CHOCKER LAUNCHER
 * Handles launching Chocker Python implementation
 */

// Check if Chocker is selected and show launch instructions
function handleChockerSelection() {
    const modal = document.createElement('div');
    modal.id = 'chocker-modal';
    modal.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10000;
  `;

    modal.innerHTML = `
    <div style="
      background: white;
      border-radius: 20px;
      padding: 40px;
      max-width: 600px;
      text-align: center;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    ">
      <div style="font-size: 80px; margin: 20px 0;">🤡</div>
      <h1 style="color: #667eea; margin: 0 0 10px 0;">CHOCKER</h1>
      <p style="font-size: 24px; color: #667eea; font-weight: bold; margin: 0 0 20px 0;">
        ULTIMATE DISRESPECT MODE
      </p>
      
      <div style="background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: left;">
        <h3 style="color: #667eea; margin-top: 0;">What Chocker Does:</h3>
        <ul style="list-style: none; padding: 0;">
          <li style="padding: 5px 0;">🤡 Opens with f3 + Kf2 (Bongcloud)</li>
          <li style="padding: 5px 0;">🤡 MUST play en passant (holy hell!)</li>
          <li style="padding: 5px 0;">🤡 MUST stalemate if possible</li>
          <li style="padding: 5px 0;">🤡 Throws advantages when winning</li>
          <li style="padding: 5px 0;">🤡 RAGE MODE if you don't en passant</li>
        </ul>
      </div>

      <div style="background: #fff3cd; border: 2px solid #ffc107; border-radius: 10px; padding: 15px; margin: 20px 0;">
        <strong>⚠️ Chocker requires Python!</strong><br>
        This AI uses advanced logic that needs the Python implementation.
      </div>

      <div style="background: #1a1a2e; color: #4ecca3; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: left; font-family: monospace;">
        <div style="color: #eee; margin-bottom: 10px;">To play Chocker, run:</div>
        <div style="margin: 5px 0;"># Option 1: Batch file</div>
        <div style="margin: 5px 0;">"batch files\\PLAY_CHESSY_COMEDIAN.bat"</div>
        <div style="margin: 10px 0;"></div>
        <div style="margin: 5px 0;"># Option 2: Direct</div>
        <div style="margin: 5px 0;">cd neural-ai</div>
        <div style="margin: 5px 0;">python chocker.py</div>
      </div>

      <div style="margin: 30px 0;">
        <button onclick="launchChocker()" style="
          background: #667eea;
          color: white;
          border: none;
          padding: 15px 40px;
          font-size: 18px;
          border-radius: 10px;
          cursor: pointer;
          margin: 10px;
          font-weight: bold;
        ">
          Launch Chocker
        </button>
        <button onclick="closeChockerModal()" style="
          background: #aaa;
          color: white;
          border: none;
          padding: 15px 40px;
          font-size: 18px;
          border-radius: 10px;
          cursor: pointer;
          margin: 10px;
          font-weight: bold;
        ">
          Back to Game
        </button>
      </div>

      <div style="font-size: 14px; color: #999; margin-top: 20px;">
        <strong>Catchphrase:</strong> ULTIMATE DISRESPECT<br>
        <strong>ELO:</strong> ∞ (Infinite)<br>
        <strong>Status:</strong> The Absolute Madman
      </div>
    </div>
  `;

    document.body.appendChild(modal);
}

// Launch Chocker (opens batch file or shows instructions)
function launchChocker() {
    // Try to open the batch file
    try {
        window.location.href = 'batch files/PLAY_CHESSY_COMEDIAN.bat';
    } catch (e) {
        // If that doesn't work, show copy-paste instructions
        alert('Copy and paste this command in your terminal:\n\ncd neural-ai\npython chocker.py');
    }
}

// Close the modal
function closeChockerModal() {
    const modal = document.getElementById('chocker-modal');
    if (modal) {
        modal.remove();
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { handleChockerSelection, launchChocker, closeChockerModal };
}
