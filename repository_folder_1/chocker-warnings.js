/**
 * CHOCKER WARNING SYSTEM
 * Double confirmation with escalating warnings
 */

// All warnings that will be shown
const CHOCKER_WARNINGS = {
    first: {
        title: "⚠️ WARNING: You Selected CHOCKER",
        warnings: [
            "🤡 Chocker will make you ragequit",
            "🤡 He opens with f3 + Kf2 (worst opening)",
            "🤡 He throws advantages on purpose",
            "🤡 He forces stalemates when winning",
            "🤡 RAGE MODE if you don't en passant",
            "🤡 ULTIMATE DISRESPECT guaranteed",
            "🤡 Your sanity will be tested",
            "🤡 You WILL question your life choices"
        ],
        question: "Are you SURE you want to play Chocker?"
    },
    second: {
        title: "🚨 FINAL WARNING: CHOCKER IS NOT NORMAL",
        warnings: [
            "💀 Players have reported uninstalling chess after playing Chocker",
            "💀 Chocker has caused keyboards to be thrown",
            "💀 Mice have been destroyed in rage",
            "💀 Friendships have ended over Chocker games",
            "💀 Therapists have been consulted",
            "💀 Chess.com accounts have been deleted",
            "💀 Career chess players have retired",
            "💀 Magnus Carlsen refuses to play Chocker"
        ],
        question: "Are you ABSOLUTELY CERTAIN you want to continue?"
    },
    third: {
        title: "🤡 LAST CHANCE: Best Way to Play - DON'T",
        warnings: [
            "⚠️ Uncontrollable rage",
            "⚠️ Questioning your chess skills",
            "⚠️ Throwing your mouse",
            "⚠️ Uninstalling chess",
            "⚠️ Existential crisis",
            "⚠️ Permanent tilt",
            "⚠️ Loss of faith in humanity",
            "⚠️ Chocker will make you ragequit",
            "💰 If you STILL want to play, your therapist will thank you for his mansion"
        ],
        question: "This is your FINAL CHANCE. Do you REALLY want to proceed?"
    }
};

/**
 * Show first warning
 */
function showChockerWarning1() {
    return new Promise((resolve) => {
        const modal = createWarningModal(CHOCKER_WARNINGS.first, 1);

        // Yes button
        const yesBtn = modal.querySelector('#warning-yes');
        yesBtn.onclick = () => {
            document.body.removeChild(modal);
            resolve(true);
        };

        // No button
        const noBtn = modal.querySelector('#warning-no');
        noBtn.onclick = () => {
            document.body.removeChild(modal);
            resolve(false);
        };

        document.body.appendChild(modal);
    });
}

/**
 * Show second warning (more intense)
 */
function showChockerWarning2() {
    return new Promise((resolve) => {
        const modal = createWarningModal(CHOCKER_WARNINGS.second, 2);

        // Yes button (more dramatic)
        const yesBtn = modal.querySelector('#warning-yes');
        yesBtn.onclick = () => {
            document.body.removeChild(modal);
            resolve(true);
        };

        // No button (escape route)
        const noBtn = modal.querySelector('#warning-no');
        noBtn.onclick = () => {
            document.body.removeChild(modal);
            showSafetyMessage();
            resolve(false);
        };

        document.body.appendChild(modal);
    });
}

/**
 * Show third warning (FINAL WARNING)
 */
function showChockerWarning3() {
    return new Promise((resolve) => {
        const modal = createWarningModal(CHOCKER_WARNINGS.third, 3);

        // Yes button (point of no return)
        const yesBtn = modal.querySelector('#warning-yes');
        yesBtn.onclick = () => {
            document.body.removeChild(modal);
            resolve(true);
        };

        // No button (last escape)
        const noBtn = modal.querySelector('#warning-no');
        noBtn.onclick = () => {
            document.body.removeChild(modal);
            showSafetyMessage();
            resolve(false);
        };

        document.body.appendChild(modal);
    });
}

/**
 * Create warning modal
 */
function createWarningModal(warning, level) {
    const modal = document.createElement('div');
    modal.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, ${level === 1 ? '0.8' : '0.95'});
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: ${10000 + level};
    animation: fadeIn 0.3s;
  `;

    const warningColor = level === 1 ? '#ff9800' : (level === 2 ? '#f44336' : '#9c27b0');
    const emoji = level === 1 ? '⚠️' : (level === 2 ? '🚨' : '🤡');

    modal.innerHTML = `
    <style>
      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }
      @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-10px); }
        20%, 40%, 60%, 80% { transform: translateX(10px); }
      }
      @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
      }
      .warning-box {
        animation: ${level === 3 ? 'shake 0.5s infinite, pulse 1s infinite' : (level === 2 ? 'shake 0.5s, pulse 2s infinite' : 'none')};
      }
    </style>
    <div class="warning-box" style="
      background: white;
      border-radius: 20px;
      padding: 40px;
      max-width: 600px;
      text-align: center;
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
      border: 5px solid ${warningColor};
    ">
      <div style="font-size: 80px; margin: 20px 0;">${emoji}</div>
      <h1 style="color: ${warningColor}; margin: 0 0 20px 0; font-size: 28px;">
        ${warning.title}
      </h1>
      
      <div style="
        background: #fff3cd;
        border: 3px solid ${warningColor};
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        text-align: left;
      ">
        <h3 style="color: ${warningColor}; margin-top: 0;">
          ${level === 1 ? 'What You\'re Getting Into:' : (level === 2 ? 'SERIOUS CONSEQUENCES:' : 'PROCEED AT YOUR OWN RISK:')}
        </h3>
        <ul style="list-style: none; padding: 0; margin: 0;">
          ${warning.warnings.map(w => `
            <li style="padding: 8px 0; font-size: 16px; color: #333;">
              ${w}
            </li>
          `).join('')}
        </ul>
      </div>

      <div style="
        background: ${level === 2 ? '#ffebee' : '#f5f5f5'};
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        font-size: 18px;
        font-weight: bold;
        color: ${warningColor};
      ">
        ${warning.question}
      </div>

      <div style="margin: 30px 0;">
        <button id="warning-yes" style="
          background: ${warningColor};
          color: white;
          border: none;
          padding: 15px 40px;
          font-size: 18px;
          border-radius: 10px;
          cursor: pointer;
          margin: 10px;
          font-weight: bold;
          transition: all 0.3s;
        " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
          ${level === 1 ? 'Yes, I Accept the Risk' : (level === 2 ? 'YES, I\'M ABSOLUTELY SURE' : 'I UNDERSTAND THE RISKS, LAUNCH CHOCKER')}
        </button>
        <button id="warning-no" style="
          background: #4caf50;
          color: white;
          border: none;
          padding: 15px 40px;
          font-size: 18px;
          border-radius: 10px;
          cursor: pointer;
          margin: 10px;
          font-weight: bold;
          transition: all 0.3s;
        " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
          ${level === 1 ? 'No, Take Me Back' : (level === 2 ? 'NO, GET ME OUT OF HERE!' : 'SAVE ME, I CHANGED MY MIND!')}
        </button>
      </div>

      ${level >= 2 ? `
        <div style="
          font-size: 12px;
          color: #999;
          margin-top: 20px;
          font-style: italic;
        ">
          ${level === 2 ? 'Last chance to turn back. We warned you. 🤡' : 'This is it. No more warnings. You\'ve been warned THREE times. 🤡'}
        </div>
      ` : ''}
    </div>
  `;

    return modal;
}

/**
 * Show safety message when user backs out
 */
function showSafetyMessage() {
    const modal = document.createElement('div');
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
    z-index: 10002;
  `;

    modal.innerHTML = `
    <div style="
      background: white;
      border-radius: 20px;
      padding: 40px;
      max-width: 500px;
      text-align: center;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    ">
      <div style="font-size: 80px; margin: 20px 0;">✅</div>
      <h2 style="color: #4caf50; margin: 0 0 20px 0;">
        Wise Decision!
      </h2>
      <p style="font-size: 18px; color: #666; margin: 20px 0;">
        You have chosen safety over chaos.<br>
        Your sanity remains intact.<br>
        Your keyboard is safe.<br>
        Your chess career continues.
      </p>
      <button onclick="this.parentElement.parentElement.remove()" style="
        background: #4caf50;
        color: white;
        border: none;
        padding: 15px 40px;
        font-size: 18px;
        border-radius: 10px;
        cursor: pointer;
        margin: 20px 0;
        font-weight: bold;
      ">
        Back to Safety
      </button>
      <div style="font-size: 14px; color: #999; margin-top: 20px;">
        You can always try Chocker later... if you dare. 🤡
      </div>
    </div>
  `;

    document.body.appendChild(modal);

    // Auto-close after 5 seconds
    setTimeout(() => {
        if (modal.parentElement) {
            modal.remove();
        }
    }, 5000);
}

/**
 * Main function: Handle Chocker selection with TRIPLE confirmation
 */
async function handleChockerSelection() {
    // First warning
    const confirmed1 = await showChockerWarning1();
    if (!confirmed1) {
        console.log('User backed out at first warning. Smart choice.');
        return false;
    }

    // Second warning (more intense)
    const confirmed2 = await showChockerWarning2();
    if (!confirmed2) {
        console.log('User backed out at second warning. Very smart choice.');
        return false;
    }

    // Third warning (FINAL WARNING)
    const confirmed3 = await showChockerWarning3();
    if (!confirmed3) {
        console.log('User backed out at third warning. Extremely smart choice.');
        return false;
    }

    // All three confirmations passed - show demo first
    console.log('User confirmed THREE times. They have been warned. Multiple times. Showing demo...');
    showChockerDemo();
    return true;
}

/**
 * Show Chocker launch instructions after confirmations
 */
function showChockerLaunchInstructions() {
    const modal = document.createElement('div');
    modal.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.9);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10003;
  `;

    modal.innerHTML = `
    <div style="
      background: white;
      border-radius: 20px;
      padding: 40px;
      max-width: 600px;
      text-align: center;
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    ">
      <div style="font-size: 80px; margin: 20px 0;">🤡</div>
      <h1 style="color: #667eea; margin: 0 0 10px 0;">CHOCKER</h1>
      <p style="font-size: 24px; color: #667eea; font-weight: bold; margin: 0 0 20px 0;">
        ULTIMATE DISRESPECT MODE
      </p>
      
      <div style="background: #1a1a2e; color: #4ecca3; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: left; font-family: monospace;">
        <div style="color: #eee; margin-bottom: 10px;">To launch Chocker, run:</div>
        <div style="margin: 5px 0;"># Option 1: Batch file</div>
        <div style="margin: 5px 0;">"batch files\\PLAY_CHESSY_COMEDIAN.bat"</div>
        <div style="margin: 10px 0;"></div>
        <div style="margin: 5px 0;"># Option 2: Direct</div>
        <div style="margin: 5px 0;">cd neural-ai</div>
        <div style="margin: 5px 0;">python chocker.py</div>
      </div>

      <div style="margin: 30px 0;">
        <button onclick="window.location.href='batch files/PLAY_CHESSY_COMEDIAN.bat'" style="
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
        <button onclick="this.parentElement.parentElement.parentElement.remove()" style="
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
          Close
        </button>
      </div>

      <div style="font-size: 14px; color: #999; margin-top: 20px;">
        You've been warned. THREE TIMES. Good luck. You'll need it. 🤡
      </div>
    </div>
  `;

    document.body.appendChild(modal);
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        handleChockerSelection,
        showChockerWarning1,
        showChockerWarning2,
        showSafetyMessage,
        showChockerLaunchInstructions
    };
}
