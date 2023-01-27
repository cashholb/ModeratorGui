import PySimpleGUI as sg
import os.path
import shutil

# Helper function
def copy_image_to_folder(directory: str, folderName: str):
    new_folder_path = directory + '\\' + folderName
    if not os.path.exists(new_folder_path):
        os.mkdir(new_folder_path)
    shutil.copy(filename, new_folder_path)

# WIDGET
# prompts user for folder
folder_getter = [
    [   sg.Text("Folder containing Images to Parse:"),],
    [
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
]

# WIDGET
# shows image and file name
image_viewer = [
    [sg.Text(size=(50,1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-", size=(50, 1))],
]

# WIDGET
# shows accept and deny buttons
buttons_viewer = [
    [
        sg.Button('ACCEPT', button_color='Green'),
        sg.Button('DENY', button_color='RED'),     
    ]
]

layout = [
    [sg.Column(folder_getter)],
    [buttons_viewer, sg.Column(image_viewer)],
]

window = sg.Window("-- Moderation Gui --", layout, element_justification='c')


# event loop
fnames = None
image_index = 0
folder = None

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
    if event == "-FOLDER-":
        if not folder:
            folder = values["-FOLDER-"]
            try:
                file_list = os.listdir(folder)
            except:
                file_list = []

            if not file_list:
                sg.popup_error_with_traceback(f'An error happened\nNo images in folder')
                break
            
            fnames = [
                f for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png", ".gif"))
            ]

            try:
                filename = os.path.join(
                    values["-FOLDER-"],
                    fnames[image_index]
                )
                window["-TOUT-"].update(filename)
                window["-IMAGE-"].update(filename=filename)
            except:
                pass

        if folder:
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)

    if event == "ACCEPT" and fnames:
        copy_image_to_folder(folder, "ACCEPTED")

        image_index += 1
        try:
            filename = os.path.join(
                values["-FOLDER-"],
                fnames[image_index]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)
        except:
            pass

    if event == "DENY" and fnames:
        copy_image_to_folder(folder, "DENIED")

        image_index += 1
        try:
            filename = os.path.join(
                values["-FOLDER-"],
                fnames[image_index]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(filename=filename)
        except:
            pass
    
window.close()