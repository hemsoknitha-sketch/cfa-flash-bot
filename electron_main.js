/**
 * CFA FLASH FEED — ELECTRON MAIN PROCESS V8.0 GOLD STANDARD
 * Ultra-Modern Frameless Desktop App with Tray Integration & 24/7/365 Background Runner
 */

const { app, BrowserWindow, Tray, Menu, ipcMain, shell } = require('electron');
const path = require('path');
const fs = require('fs');

let mainWindow = null;
let tray = null;
let isQuitting = false;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1280,
        height: 860,
        minWidth: 800,
        minHeight: 600,
        title: "CFA Flash Feed — 24/7 AI Intelligence Hub",
        backgroundColor: '#070a12',
        autoHideMenuBar: true,
        frame: true, // Native clean titlebar
        webPreferences: {
            preload: path.join(__dirname, 'electron_preload.js'),
            nodeIntegration: false,
            contextIsolation: true,
            sandbox: true
        },
        icon: path.join(__dirname, 'LOGO.png')
    });

    const miniAppPath = path.join(__dirname, 'mini_app', 'index.html');
    mainWindow.loadFile(miniAppPath);

    // Prevent closing, minimize to system tray instead (for 24/7 background operation)
    mainWindow.on('close', (event) => {
        if (!isQuitting) {
            event.preventDefault();
            mainWindow.hide();
        }
    });

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

function createTray() {
    const iconPath = path.join(__dirname, 'LOGO.png');
    if (fs.existsSync(iconPath)) {
        try {
            tray = new Tray(iconPath);
            const contextMenu = Menu.buildFromTemplate([
                {
                    label: '⚡ បើកផ្ទាំង CFA Flash Feed',
                    click: () => {
                        if (mainWindow) {
                            mainWindow.show();
                            mainWindow.focus();
                        } else {
                            createWindow();
                        }
                    }
                },
                { type: 'separator' },
                {
                    label: '🌐 បើក Web API (:8080)',
                    click: () => {
                        shell.openExternal('http://localhost:8080');
                    }
                },
                { type: 'separator' },
                {
                    label: '🛑 ចេញពីកម្មវិធីទាំងស្រុង (Quit)',
                    click: () => {
                        isQuitting = true;
                        app.quit();
                    }
                }
            ]);

            tray.setToolTip('CFA Flash Feed — 24/7 AI Super Brain Hub');
            tray.setContextMenu(contextMenu);

            tray.on('double-click', () => {
                if (mainWindow) {
                    if (mainWindow.isVisible()) {
                        mainWindow.hide();
                    } else {
                        mainWindow.show();
                        mainWindow.focus();
                    }
                }
            });
        } catch (e) {
            console.error("Tray initialization note:", e);
        }
    }
}

// IPC Handlers
ipcMain.on('window-minimize', () => {
    if (mainWindow) mainWindow.minimize();
});

ipcMain.on('window-maximize', () => {
    if (mainWindow) {
        if (mainWindow.isMaximized()) {
            mainWindow.unmaximize();
        } else {
            mainWindow.maximize();
        }
    }
});

ipcMain.on('window-close', () => {
    if (mainWindow) mainWindow.hide();
});

ipcMain.on('open-external', (event, url) => {
    if (url && (url.startsWith('http://') || url.startsWith('https://'))) {
        shell.openExternal(url);
    }
});

// App Lifecycle
const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
    app.quit();
} else {
    app.on('second-instance', () => {
        if (mainWindow) {
            if (mainWindow.isMinimized()) mainWindow.restore();
            mainWindow.show();
            mainWindow.focus();
        }
    });

    app.whenReady().then(() => {
        createWindow();
        createTray();

        app.on('activate', () => {
            if (BrowserWindow.getAllWindows().length === 0) createWindow();
        });
    });
}

app.on('before-quit', () => {
    isQuitting = true;
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin' && isQuitting) {
        app.quit();
    }
});
