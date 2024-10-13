const {app, BrowserWindow} = require('electron');
const path = require('path');

function createWindow() {
    const mainWindow = new BrowserWindow({
        width: 900,
        height: 900,
        webPreferences: {
            nodeIntegration: true,
	    contextIsolation:false,	
            preload: path.join(__dirname, 'preload.js')
        }
    });

    mainWindow.loadFile('index.html');
    mainWindow.show();
}

// Call createWindow only when Electron is ready
app.whenReady().then(() => {
    createWindow();

    // On macOS, it's common to recreate a window in the app when the dock icon is clicked and there are no other windows open.
    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

// Quit when all windows are closed, except on macOS.
app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
