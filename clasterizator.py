from ClusteringObject import ClusteringObject
from FilePathController import FilePathController
from WindowFormController import WindowFormController
from WindowFormEventHandler import WindowFormEventHandler
from SettingsController import SettingsController
from TextEditorSettingsController import TextEditorSettingsController
import tkinter


def startClustering(logPathLocal):
    startRowRegExp = str(windowFormController.regExpEntry.get())
    settingsController.saveRegExp(startRowRegExp)
    algorithmIdValue = windowFormController.algorithmId.get()
    settingsController.saveAlgorithmId(algorithmIdValue)
    countClustersValue = windowFormController.countClusters.get()
    settingsController.saveCountClusters(int(countClustersValue))
    countRowsValue = windowFormController.countRows.get()
    settingsController.saveCountRows(int(countRowsValue))
    if startRowRegExp and logPathLocal:
        windowFormController.clustersListbox.delete(0, tkinter.END)
        windowFormController.messagesListbox.delete(0, tkinter.END)
        windowFormController.messageTextBox['state'] = tkinter.NORMAL
        windowFormController.messageTextBox.delete(1.0, tkinter.END)
        windowFormController.messageTextBox.insert(1.0, f'Начат процесс кластеризации. Подготовка текста...\n')
        windowFormController.clustersListContainer['text'] = '----------'
        windowFormController.window.update()

        clusteringResult = ClusteringObject().main(logPathLocal, startRowRegExp, windowFormController)
        windowFormEventHandler.renderResult(clusteringResult)

        windowFormController.clustersListContainer['text'] = f'Кластеры ({len(clusteringResult.clustersItems)})'
        windowFormController.messageTextBox['state'] = tkinter.DISABLED


currentScriptFolder = FilePathController.getScriptFolder()
clusterTempFile = FilePathController.getClusterTempFilePath()
textEditorSettingsController = TextEditorSettingsController(currentScriptFolder)
textEditorPath = textEditorSettingsController.getTextEditorPath()
logPath = FilePathController.getLogPath()
settingsController = SettingsController(currentScriptFolder, logPath, textEditorPath)
startRowRegExpInit = settingsController.getRegExp()
algorithmIdValueInit = settingsController.getAlgorithmId()
countClustersValueInit = settingsController.getCountClusters()
countRowsValueInit = settingsController.getCountRows()

windowFormController = WindowFormController(
    currentScriptFolder=currentScriptFolder,
    windowWidth=800,
    windowHeight=600,
    logPath=logPath,
    startRowRegExpInit=startRowRegExpInit,
    textEditorPathInit=textEditorPath,
    algorithmIdValueInit=algorithmIdValueInit,
    countClustersValueInit=countClustersValueInit,
    countRowsValueInit=countRowsValueInit,
)
windowFormEventHandler = WindowFormEventHandler(
    windowWidth=windowFormController.windowWidth,
    windowHeight=windowFormController.windowHeight,
    clusterTempFile=clusterTempFile,
    windowFormController=windowFormController,
    textEditorEntry=windowFormController.textEditorEntry
)

windowFormController.window.bind("<Configure>", windowFormEventHandler.onWindowChange)
windowFormController.window.protocol("WM_DELETE_WINDOW", windowFormEventHandler.onWindowClose)
windowFormController.startClusteringButton['command'] = lambda: startClustering(logPath)
windowFormController.openInSublimeButton['command'] = windowFormEventHandler.openInSublime
windowFormController.messagesListbox.bind(
    '<<ListboxSelect>>',
    lambda listboxEvent: windowFormEventHandler.messagesListBoxClick(listboxEvent, windowFormController.messageTextBox)
)
windowFormController.clustersListbox.bind(
    '<<ListboxSelect>>',
    lambda event: windowFormEventHandler.clustersListboxClick(event, windowFormController.clusterTextBox)
)
windowFormController.openClusterInSublimeButton['command'] = lambda: windowFormEventHandler.openClusterInSublime()
windowFormController.saveTextEditorButton['command'] = lambda: textEditorSettingsController.checkAndSavePath(windowFormController.textEditorEntry)
windowFormController.settingsButton['command'] = settingsController.openSettingsInEditor

windowFormController.window.bind(
    "<<textsIsEmptyEvent>>",
    lambda event: windowFormController.messageTextBox.insert(2.0, f'Ошибка! Не удалось разбить текст данным регулярным выражением.\n')
)
windowFormController.window.bind(
    "<<textPrepareFinishedEvent>>",
    lambda event: windowFormController.messageTextBox.insert(2.0, f'Подготовка текста завершена. Удаление редких слов...\n')
)
windowFormController.window.bind(
    "<<textClearRearWordsFinishedEvent>>",
    lambda event: windowFormController.messageTextBox.insert(3.0, f'Удаление редких слов завершено. Процесс TF-IDF...\n')
)
windowFormController.window.bind(
    "<<tfidfFinishedEvent>>",
    lambda event: windowFormController.messageTextBox.insert(4.0, f'Процесс TF-IDF завершен. Birch-кластеризация...\n')
)
windowFormController.window.bind(
    "<<clusteringFinishedEvent>>",
    lambda event: windowFormController.messageTextBox.insert(5.0, f'Кластеризация завершена. Обработка результатов...\n')
)
windowFormController.window.bind(
    "<<parsePredictionFinishedEvent>>",
    lambda event: windowFormController.messageTextBox.insert(6.0, f'Обработка результатов завершена. Процесс окончен.\n')
)

windowFormController.window.mainloop()
