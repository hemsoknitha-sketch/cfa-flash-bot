/**
 * CFA FLASH FEED — ELECTRON PRELOAD BRIDGE
 * Secure IPC Context Isolation Bridge V8.0
 */

const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    platform: process.platform,
    version: process.versions.electron,
    minimize: () => ipcRenderer.send('window-minimize'),
    maximize: () => ipcRenderer.send('window-maximize'),
    close: () => ipcRenderer.send('window-close'),
    openExternal: (url) => ipcRenderer.send('open-external', url)
});
