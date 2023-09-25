import os

def create_unique_folder_name(folder_name):
    
    save_folder = f"./projects/{folder_name}"   

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        return folder_name       
    else:
        count = 1
        list_folders = [folder for folder in os.listdir('./projects/') if os.path.isdir(os.path.join('./projects/', folder))]

        while True:
            new_folder_name = folder_name + '(' + str(count) + ')'
            if new_folder_name in list_folders:
                count += 1
            else:
                break
        return new_folder_name 
        